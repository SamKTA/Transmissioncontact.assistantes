import streamlit as st
from pages import accueil, roulement, hors_roulement, formulaire
from utils.session import init_session_state

# Configuration de la page
st.set_page_config(
    page_title="Gestion Contacts ORPI Arcades",
    page_icon="🏠",
    initial_sidebar_state="collapsed",
    layout="wide"
)

# Custom CSS pour améliorer l'apparence
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton button {
        background-color: #FF5A5F;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #FF3B3F;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #484848;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-1r6slb0 {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stSelectbox label, .stTextInput label {
        color: #484848;
        font-weight: 500;
    }
    /* Style pour le message de chargement */
    .stSpinner {
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialisation des variables de session
    init_session_state()
    
    # Affichage du logo ORPI
    col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("assets/logo-orpi.jpeg", width=100)

with col_title:
    st.markdown("<h1 style='margin-top: 25px;'>Gestion des Contacts ORPI Arcades</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 1.2em;'>Outil de transmission des contacts entrants</p>", unsafe_allow_html=True)

    
    # Navigation en fonction de la page actuelle
    if st.session_state.page == "accueil":
        accueil.show()
    elif st.session_state.page == "roulement":
        roulement.show()
    elif st.session_state.page == "hors_roulement":
        hors_roulement.show()
    elif st.session_state.page == "formulaire":
        formulaire.show()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888; font-size: 0.8rem;">
            © 2025 ORPI Arcades | Application de gestion des contacts
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
