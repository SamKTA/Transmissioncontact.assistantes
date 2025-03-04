import streamlit as st
from utils.ui import header, animated_button, card, notification, load_material_icons
from utils.session import change_page_with_loading
from utils.constants import CONSEILLERS, EMAILS_CONSEILLERS

def show():
    """Affiche la page pour les contacts hors roulement"""
    # Charger les icônes Material Design
    load_material_icons()
    
    # En-tête de la page
    header(
        "Contacts Hors Roulement",
        "Attribution directe des contacts à un conseiller spécifique"
    )
    
    # Bouton de retour à l'accueil
    col_back, _ = st.columns([1, 5])
    with col_back:
        animated_button("← Retour à l'accueil", key="btn_back_to_home", on_click=change_page_with_loading, args=("accueil",), color="#888")
    
    # Styliser le titre de section
    st.markdown(
        """
        <h2 style="background-color: #2196F3; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            2 Roulements disponibles
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    # Créer deux colonnes pour les types de contacts
    col1, col2 = st.columns(2)
    
    # Type de contact sélectionné
    contact_type = None
    
    # Carte pour Vendeur Secteur
    with col1:
        st.markdown(
            """
            <div style="background-color: white; border-radius: 10px; padding: 1rem; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 5px solid #FFC107;
                    transition: all 0.3s ease; height: 150px; display: flex; flex-direction: column; justify-content: center;">
                <h3 style="color: #FFC107; text-align: center;">Vendeur Secteur</h3>
                <p style="text-align: center;">Pour les clients vendeurs liés à un secteur géographique spécifique</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Sélectionner Vendeur Secteur", key="btn_vendeur_secteur"):
            contact_type = "Vendeur secteur"
    
    # Carte pour Acquéreur Bien
    with col2:
        st.markdown(
            """
            <div style="background-color: white; border-radius: 10px; padding: 1rem; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 5px solid #4CAF50;
                    transition: all 0.3s ease; height: 150px; display: flex; flex-direction: column; justify-content: center;">
                <h3 style="color: #4CAF50; text-align: center;">Acquéreur Bien</h3>
                <p style="text-align: center;">Pour les clients intéressés par un bien immobilier spécifique</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Sélectionner Acquéreur Bien", key="btn_acquereur_bien"):
            contact_type = "Acquéreur bien"
    
    # Si un type de contact a été sélectionné
    if contact_type:
        st.session_state.type_contact_hors_roulement = "Acheteur bien" if contact_type == "Acquéreur bien" else "Vendeur"
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <h3 style="background-color: #FF9800; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                Sélectionner un conseiller
            </h3>
            """,
            unsafe_allow_html=True
        )
        
        # Afficher la liste des conseillers avec leurs photos (placeholders)
        conseillers_cols = st.columns(4)
        
        # Liste des conseillers pour l'affichage
        conseillers_list = list(EMAILS_CONSEILLERS.keys())
        
        # Diviser la liste en groupes pour l'affichage en grille
        for i, conseiller in enumerate(conseillers_list):
            with conseillers_cols[i % 4]:
                st.markdown(
                    f"""
                    <div style="background-color: white; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; cursor: pointer;
                            transition: all 0.3s ease;">
                        <div style="width: 80px; height: 80px; border-radius: 50%; background-color: #f0f0f0; 
                                margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                            <i class="material-icons" style="font-size: 40px; color: #888;">person</i>
                        </div>
                        <h4>{conseiller}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button(f"Sélectionner {conseiller.split()[0]}", key=f"btn_select_{i}"):
                    st.session_state.conseiller_selectionne = conseiller
                    change_page("formulaire")
    else:
        # Si aucun type n'est encore sélectionné, afficher un message d'instruction
        st.markdown("<br>", unsafe_allow_html=True)
        notification("Veuillez sélectionner un type de contact ci-dessus pour continuer.", "info")
