import streamlit as st
import pandas as pd
from datetime import datetime
from utils.ui import header, animated_button, card, notification, load_material_icons
from utils.session import change_page
from utils.constants import CONSEILLERS, ROULEMENTS
from services.sheets_service import read_rotations, add_unavailability
from services.rotation_service import get_next_counselor, handle_skip, is_available

def show():
    """Affiche la page de gestion des roulements"""
    # Charger les icônes Material Design
    load_material_icons()
    
    # En-tête de la page
    header(
        "Système de Roulement",
        "Attribution automatique des contacts selon les règles définies"
    )
    
    # Bouton de retour à l'accueil
    col_back, _ = st.columns([1, 5])
    with col_back:
        animated_button("← Retour à l'accueil", key="btn_back_to_home", on_click=change_page, args=("accueil",), color="#888")
    
    # Lire l'état actuel des roulements
    etat_df, indispo_df = read_rotations()
    
    # Styliser les titres de section
    st.markdown(
        """
        <h2 style="background-color: #FFC107; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            Étape 1 : Sélectionner le type de contact
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    # Afficher les trois options de roulement avec animation
    st.markdown(
        """
        <style>
        .rotation-card {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .rotation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Créer trois colonnes pour les types de roulement
    col1, col2, col3 = st.columns(3)
    
    # Fonction pour créer une carte de roulement
    def create_rotation_card(column, rotation_type, color):
    with column:
        # Trouver le dernier conseiller et déterminer le prochain
        rotation_data = etat_df[etat_df["Type"] == rotation_type]
        last_counselor = rotation_data["Dernier_Conseiller"].values[0] if not rotation_data.empty else ""
        
        # Créer une clé de session spécifique à ce type de roulement pour stocker le conseiller actuel
        current_counselor_key = f"current_counselor_{rotation_type}"
        
        # Initialiser le conseiller actuel s'il n'existe pas dans la session
        if current_counselor_key not in st.session_state:
            st.session_state[current_counselor_key] = get_next_counselor(rotation_type, last_counselor, indispo_df)
        
        # Afficher la carte
        st.markdown(
            f"""
            <div class="rotation-card" style="background-color: white; border-radius: 10px; padding: 1rem; 
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 5px solid {color};">
                <h3 style="color: {color};">{rotation_type}</h3>
                <p><strong>Dernier contact attribué à:</strong> {last_counselor or "Aucun"}</p>
                <p><strong>Conseiller suivant recommandé:</strong> {st.session_state[current_counselor_key] or "Non déterminé"}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Boutons d'action
        col_select, col_skip = st.columns(2)
        
        with col_select:
            if st.button(f"Sélectionner", key=f"btn_select_{rotation_type}"):
                # Si sélectionné, on envoie vers le formulaire avec ce conseiller
                st.session_state.type_roulement = rotation_type
                st.session_state.conseiller_selectionne = CONSEILLERS.get(
                    st.session_state[current_counselor_key], 
                    st.session_state[current_counselor_key]
                )
                change_page("formulaire")
        
        with col_skip:
            if st.button(f"Suivant", key=f"btn_skip_{rotation_type}"):
                # Si "Suivant" est cliqué, on passe simplement au conseiller suivant
                skipped_key = f"skipped_{rotation_type}"
                if skipped_key not in st.session_state:
                    st.session_state[skipped_key] = []
                
                # Ajouter le conseiller actuel à la liste des sautés
                if st.session_state[current_counselor_key]:
                    st.session_state[skipped_key].append(st.session_state[current_counselor_key])
                
                # Obtenir le prochain conseiller
                st.session_state[current_counselor_key] = get_next_counselor(
                    rotation_type, 
                    last_counselor, 
                    indispo_df, 
                    st.session_state[skipped_key]
                )
                
                # Notification pour indiquer que le conseiller a été sauté
                st.warning(f"Conseiller {st.session_state[current_counselor_key]} proposé pour le prochain contact.")
                
                # Forcer le rechargement de la page pour montrer le changement
                st.experimental_rerun()
    
    # Afficher les cartes de roulement
    create_rotation_card(col1, "VENDEURS PAS DE PROJET", "#E91E63")
    create_rotation_card(col2, "VENDEURS PROJET VENTE", "#9C27B0")
    create_rotation_card(col3, "ACQUÉREURS", "#3F51B5")
    
    # Section pour la gestion des indisponibilités
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <h2 style="background-color: #607D8B; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            Gestion des indisponibilités
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    # Afficher les indisponibilités actuelles
    with st.expander("Voir les indisponibilités actuelles", expanded=False):
        if not indispo_df.empty:
            # Filtrer pour ne montrer que les indisponibilités actuelles ou futures
            today = datetime.now().date()
            
            # Convertir les dates et filtrer
            valid_indispo = []
            for _, row in indispo_df.iterrows():
                try:
                    end_date = datetime.strptime(row["Fin"], "%d/%m/%Y").date()
                    if end_date >= today:
                        valid_indispo.append(row)
                except (ValueError, TypeError):
                    continue
            
            if valid_indispo:
                valid_df = pd.DataFrame(valid_indispo)
                st.dataframe(valid_df, use_container_width=True)
            else:
                st.info("Aucune indisponibilité active ou future.")
        else:
            st.info("Aucune indisponibilité enregistrée.")
    
    # Formulaire pour ajouter une indisponibilité
    with st.expander("Ajouter une nouvelle indisponibilité", expanded=False):
        with st.form("form_indisponibilite"):
            col_conseiller, col_raison = st.columns(2)
            
            with col_conseiller:
                conseiller = st.selectbox(
                    "Conseiller",
                    options=list(CONSEILLERS.keys())
                )
            
            with col_raison:
                raison = st.text_input("Raison de l'indisponibilité", placeholder="Ex: Congés, Formation, etc.")
            
            col_debut, col_fin = st.columns(2)
            
            with col_debut:
                date_debut = st.date_input("Date de début", min_value=datetime.now().date())
            
            with col_fin:
                date_fin = st.date_input("Date de fin", min_value=date_debut)
            
            # Bouton de soumission
            submitted = st.form_submit_button("Ajouter l'indisponibilité")
            
            if submitted:
                if date_fin < date_debut:
                    st.error("La date de fin doit être postérieure à la date de début.")
                else:
                    # Ajouter l'indisponibilité
                    success = add_unavailability(conseiller, date_debut, date_fin, raison)
                    if success:
                        st.success(f"Indisponibilité ajoutée pour {conseiller} du {date_debut.strftime('%d/%m/%Y')} au {date_fin.strftime('%d/%m/%Y')}")
                        st.experimental_rerun()
    
    # Rappel des ordres de roulement
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Rappel des ordres de roulement", expanded=False):
        for rotation_type, order in ROULEMENTS.items():
            st.subheader(rotation_type)
            order_str = " → ".join(order)
            st.markdown(f"<div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px;'>{order_str}</div>", unsafe_allow_html=True)
