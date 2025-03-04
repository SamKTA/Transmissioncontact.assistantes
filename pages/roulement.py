import streamlit as st
import pandas as pd
from datetime import datetime
from utils.ui import header, animated_button, card, notification, load_material_icons
from utils.session import change_page
from utils.constants import CONSEILLERS, ROULEMENTS
from services.sheets_service import read_rotations, add_unavailability
from services.rotation_service import get_next_counselor, is_available

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
    
    # Initialiser les paramètres de session pour les conseillers courants
    for rotation_type in ROULEMENTS:
        current_key = f"current_{rotation_type}"
        if current_key not in st.session_state:
            # Obtenir le dernier conseiller pour ce type
            rotation_data = etat_df[etat_df["Type"] == rotation_type]
            last_counselor = rotation_data["Dernier_Conseiller"].values[0] if not rotation_data.empty else ""
            
            # Initialiser avec le conseiller suivant
            order = ROULEMENTS[rotation_type]
            if last_counselor in order:
                idx = order.index(last_counselor)
                next_idx = (idx + 1) % len(order)
                st.session_state[current_key] = order[next_idx]
            else:
                st.session_state[current_key] = order[0]
    
    # Gérer les actions des boutons Suivant
    for rotation_type in ROULEMENTS:
        skip_button = f"skip_{rotation_type}"
        if skip_button in st.session_state and st.session_state[skip_button]:
            # Obtenir le conseiller suivant
            current_key = f"current_{rotation_type}"
            current_counselor = st.session_state[current_key]
            order = ROULEMENTS[rotation_type]
            
            if current_counselor in order:
                idx = order.index(current_counselor)
                next_idx = (idx + 1) % len(order)
                next_counselor = order[next_idx]
                
                # Vérifier si le conseiller est disponible
                while not is_available(next_counselor, indispo_df):
                    next_idx = (next_idx + 1) % len(order)
                    next_counselor = order[next_idx]
                    if next_idx == idx:  # Éviter la boucle infinie
                        break
                
                # Mettre à jour le conseiller
                st.session_state[current_key] = next_counselor
                
                # Réinitialiser le bouton
                st.session_state[skip_button] = False
    
    # Créer trois colonnes pour les types de roulement
    col1, col2, col3 = st.columns(3)
    
    # Afficher les cartes de roulement pour chaque type
    create_rotation_card(col1, "VENDEURS PAS DE PROJET", "#E91E63", etat_df, indispo_df)
    create_rotation_card(col2, "VENDEURS PROJET VENTE", "#9C27B0", etat_df, indispo_df)
    create_rotation_card(col3, "ACQUÉREURS", "#3F51B5", etat_df, indispo_df)
    
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


def create_rotation_card(column, rotation_type, color, etat_df, indispo_df):
    with column:
        # Clé de session pour le conseiller actuel
        current_key = f"current_{rotation_type}"
        
        # Trouver le dernier conseiller attribué
        rotation_data = etat_df[etat_df["Type"] == rotation_type]
        last_counselor = rotation_data["Dernier_Conseiller"].values[0] if not rotation_data.empty else ""
        
        # Afficher la carte
        st.markdown(
            f"""
            <div class="rotation-card" style="background-color: white; border-radius: 10px; padding: 1rem; 
                       box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 5px solid {color};">
                <h3 style="color: {color};">{rotation_type}</h3>
                <p><strong>Dernier contact attribué à:</strong> {last_counselor or "Aucun"}</p>
                <p><strong>Conseiller suivant recommandé:</strong> {st.session_state[current_key]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Boutons d'action
        col_select, col_skip = st.columns(2)
        
        with col_select:
            # Solution directe pour le bouton Sélectionner
            if st.button(f"Sélectionner", key=f"btn_select_{rotation_type}"):
                # Préparer les variables nécessaires pour le formulaire
                st.session_state.type_roulement = rotation_type
                st.session_state.conseiller_selectionne = CONSEILLERS.get(
                    st.session_state[current_key], 
                    st.session_state[current_key]
                )
                
                # Redirection directe avec JavaScript (plus fiable que change_page)
                js = f"""
                <script>
                    window.parent.location.href = window.parent.location.origin + "?page=formulaire";
                </script>
                """
                st.markdown(js, unsafe_allow_html=True)
        
        with col_skip:
            # Utiliser un callback pour le bouton Suivant
            st.button(
                f"Suivant", 
                key=f"btn_skip_{rotation_type}", 
                on_click=activate_skip, 
                args=(rotation_type,)
            )

def activate_skip(rotation_type):
    """Active le drapeau de saut pour ce type de roulement"""
    skip_button = f"skip_{rotation_type}"
    st.session_state[skip_button] = True
    
    # Ajouter un message pour l'utilisateur
    current_key = f"current_{rotation_type}"
    current_counselor = st.session_state[current_key]
    
    # Obtenir le prochain conseiller (pour l'affichage uniquement)
    order = ROULEMENTS[rotation_type]
    idx = order.index(current_counselor) if current_counselor in order else 0
    next_idx = (idx + 1) % len(order)
    next_counselor = order[next_idx]
    
    # Stocker le message
    st.session_state.message = f"Passage de {current_counselor} à {next_counselor}."
