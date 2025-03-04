import streamlit as st
import time

def change_page(page):
    """Change la page actuelle avec un effet de chargement"""
    # Sauvegarder la page précédente
    previous_page = st.session_state.page
    
    # Afficher un spinner pendant 0.5 seconde pour simuler un chargement
    with st.spinner("Chargement en cours..."):
        # Changer la page
        st.session_state.page = page
        
        # Ajouter un petit délai pour que le spinner soit visible
        time.sleep(0.5)
    
    # Réinitialiser certaines variables selon les transitions
    if previous_page == "roulement" and page == "accueil":
        st.session_state.type_roulement = None
        st.session_state.conseiller_selectionne = None
    
    if previous_page == "hors_roulement" and page == "accueil":
        st.session_state.from_hors_roulement = False
    
    if page == "hors_roulement":
        st.session_state.from_hors_roulement = True
    
    # Forcer le rechargement de la page
    st.experimental_rerun()

def init_session_state():
    """Initialise les variables de session si elles n'existent pas déjà"""
    
    # Page actuelle (pour la navigation)
    if "page" not in st.session_state:
        st.session_state.page = "accueil"
    
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
