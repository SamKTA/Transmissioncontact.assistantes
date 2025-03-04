import streamlit as st

def change_page_with_loading(page):
    """Change la page avec un indicateur de chargement"""
    # Activer l'état de chargement
    st.session_state.is_loading = True
    
    # Changer la page
    st.session_state.page = page

# Mise à jour de la fonction init_session_state
def init_session_state():
    """Initialise les variables de session si elles n'existent pas déjà"""
    
    # Page actuelle (pour la navigation)
    if "page" not in st.session_state:
        st.session_state.page = "accueil"
    
    # État de chargement
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False
    
    # Conseiller sélectionné (pour le formulaire)
    if "conseiller_selectionne" not in st.session_state:
        st.session_state.conseiller_selectionne = None
    
    # Type de roulement sélectionné
    if "type_roulement" not in st.session_state:
        st.session_state.type_roulement = None
    
    # État du formulaire
    if "formulaire_soumis" not in st.session_state:
        st.session_state.formulaire_soumis = False
    
    # Stockage temporaire pour les données du formulaire
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    
    # Pour la gestion du bouton "Suivant" dans les roulements
    if "skip_count" not in st.session_state:
        st.session_state.skip_count = 0
    
    # Pour suivre les conseillers indisponibles
    if "indisponibles" not in st.session_state:
        st.session_state.indisponibles = []
    
    # Pour savoir si nous venons de la page Hors Roulement
    if "from_hors_roulement" not in st.session_state:
        st.session_state.from_hors_roulement = False
    
    # Type de contact présélectionné (pour hors roulement)
    if "type_contact_hors_roulement" not in st.session_state:
        st.session_state.type_contact_hors_roulement = None
