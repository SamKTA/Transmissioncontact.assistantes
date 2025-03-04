import streamlit as st
from utils.ui import header, animated_button, card, notification, load_material_icons
from utils.session import change_page

def show():
    """Affiche la page d'accueil"""
    # Charger les icônes Material Design
    load_material_icons()
    
    # En-tête de la page
    header(
        "Gestion des Contacts ORPI Arcades",
        "Outil de transmission des contacts entrants"
    )
    
    # Animation d'introduction (avec CSS)
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .fadeIn {
            animation: fadeIn 0.8s ease-out forwards;
        }
        </style>
        <div class="fadeIn" style="text-align: center; padding: 20px;">
            <h2>Bienvenue sur l'application de gestion des contacts</h2>
            <p>Sélectionnez le type de transmission que vous souhaitez effectuer.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Espacement
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Deux cartes pour les choix principaux
    col1, col2 = st.columns(2)
    
    with col1:
        card(
            "Roulement",
            """
            <p>Utilisez ce mode pour suivre la rotation automatique des contacts entre les conseillers.</p>
            <p>3 types de roulements disponibles :</p>
            <ul>
                <li>Vendeur pas de projet</li>
                <li>Vendeur projet de vente</li>
                <li>Acquéreur</li>
            </ul>
            """,
            color="#4CAF50",
            footer="Le système proposera automatiquement un conseiller selon les règles définies."
        )
        animated_button("Système de Roulement", key="btn_roulement", on_click=change_page, args=("roulement",), color="#4CAF50")
    
    with col2:
        card(
            "Hors Roulement",
            """
            <p>Utilisez ce mode pour attribuer directement un contact à un conseiller spécifique.</p>
            <p>2 types de contacts disponibles :</p>
            <ul>
                <li>Vendeur Secteur</li>
                <li>Acquéreur bien</li>
            </ul>
            """,
            color="#2196F3",
            footer="Vous choisirez manuellement le conseiller qui recevra le contact."
        )
        animated_button("Contact Direct", key="btn_hors_roulement", on_click=change_page, args=("hors_roulement",), color="#2196F3")
    
    # Pied de page avec statistiques
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;">
            <h4>L'application permet de :</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="margin: 10px;">
                    <i class="material-icons" style="font-size: 2rem; color: #FF5A5F;">person_add</i>
                    <p>Attribuer les contacts</p>
                </div>
                <div style="margin: 10px;">
                    <i class="material-icons" style="font-size: 2rem; color: #FF5A5F;">email</i>
                    <p>Envoyer des notifications</p>
                </div>
                <div style="margin: 10px;">
                    <i class="material-icons" style="font-size: 2rem; color: #FF5A5F;">history</i>
                    <p>Gérer les roulements</p>
                </div>
                <div style="margin: 10px;">
                    <i class="material-icons" style="font-size: 2rem; color: #FF5A5F;">event_busy</i>
                    <p>Gérer les indisponibilités</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
