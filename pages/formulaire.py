import streamlit as st
from datetime import datetime
from utils.ui import header, animated_button, notification, load_material_icons
from utils.session import change_page
from utils.constants import CONSEILLERS, SOURCES, CANAUX, TYPES_CONTACT, ASSISTANTES, EMAILS_CONSEILLERS
from services.sheets_service import save_contact, update_rotation
from services.email_service import send_email

def show():
    """Affiche la page du formulaire de contact"""
    # Charger les icônes Material Design
    load_material_icons()
    
    # En-tête de la page avec un sous-titre adapté au contexte
    subtitle = "Transmission d'un contact via le système de roulement" if st.session_state.type_roulement else "Transmission directe d'un contact"
    header(
        "Formulaire de Transmission",
        subtitle
    )
    
    # Bouton de retour au choix précédent
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.session_state.type_roulement:
            animated_button("← Retour au roulement", key="btn_back_to_rotation", on_click=change_page, args=("roulement",), color="#888")
        else:
            animated_button("← Retour au choix du type", key="btn_back_to_hors_roulement", on_click=change_page, args=("hors_roulement",), color="#888")
    
    # Date du jour (automatique)
    date_aujourdhui = datetime.now().strftime("%d/%m/%Y")
    st.markdown(f"**Date :** {date_aujourdhui}")
    
    # Afficher un formulaire attrayant
    st.markdown(
        """
        <style>
        .form-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .form-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #FF5A5F;
            border-bottom: 2px solid #FF5A5F;
            padding-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Formulaire encadré
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-header">Informations du contact</div>', unsafe_allow_html=True)
    
    with st.form("formulaire_contact"):
        # Première ligne: Assistante, Conseiller
        col1, col2 = st.columns(2)
        with col1:
            assistante = st.selectbox(
                "Assistante *",
                options=ASSISTANTES
            )
        
        with col2:
            # Liste des conseillers pour le selectbox
            conseillers_list = list(EMAILS_CONSEILLERS.keys())
            
            # Index par défaut si un conseiller est déjà sélectionné
            default_index = 0
            if st.session_state.conseiller_selectionne:
                try:
                    default_index = conseillers_list.index(st.session_state.conseiller_selectionne)
                except ValueError:
                    default_index = 0
            
            destinataire = st.selectbox(
                "Conseiller destinataire *",
                options=conseillers_list,
                index=default_index
            )
        
        # Deuxième ligne: Source, Canal
        col3, col4 = st.columns(2)
        with col3:
            source = st.selectbox(
                "Source du contact *",
                options=SOURCES
            )
        
        with col4:
            canal = st.selectbox(
                "Canal de communication *",
                options=CANAUX
            )
        
        # Troisième ligne: Type de contact
        type_contact_options = TYPES_CONTACT
        
        # Préselection du type de contact si venant de hors_roulement
        default_type_index = 0
        if st.session_state.type_contact_hors_roulement:
            matching_types = [i for i, t in enumerate(type_contact_options) if st.session_state.type_contact_hors_roulement in t]
            if matching_types:
                default_type_index = matching_types[0]
        
        type_contact = st.selectbox(
            "Type de contact *",
            options=type_contact_options,
            index=default_type_index
        )
        
        # Quatrième ligne: Coordonnées du client
        st.markdown('<div class="form-header">Coordonnées du client</div>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        with col5:
            nom_client = st.text_input(
                "Nom complet du client *",
                placeholder="Prénom et Nom du client"
            )
        
        with col6:
            telephone_client = st.text_input(
                "Téléphone du client *",
                placeholder="Numéro de téléphone"
            )
        
        email_client = st.text_input(
            "Adresse e-mail du client",
            placeholder="Email du client (optionnel)"
        )
        
        # Cinquième ligne: Commentaire
        st.markdown('<div class="form-header">Informations complémentaires</div>', unsafe_allow_html=True)
        
        commentaire = st.text_area(
            "Commentaire",
            placeholder="Informations supplémentaires, demande spécifique, etc."
        )
        
        # Bouton de soumission
        submitted = st.form_submit_button("Transmettre le contact")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Traitement du formulaire après soumission
    if submitted:
        # Vérification des champs obligatoires
        if not nom_client or not telephone_client:
            notification("Veuillez remplir tous les champs obligatoires (*)", "error")
        else:
            # Préparer les données à sauvegarder
            donnees = {
                "date": date_aujourdhui,
                "assistante": assistante,
                "destinataire": destinataire,
                "source": source,
                "canal": canal,
                "type_contact": type_contact,
                "nom_client": nom_client,
                "email_client": email_client,
                "telephone_client": telephone_client,
                "commentaire": commentaire
            }
            
            # 1. Sauvegarder dans Google Sheets
            save_success = save_contact(donnees)
            
            if save_success:
                # 2. Envoyer l'email au conseiller
                email_success = send_email(donnees)
                
                if email_success:
                    # 3. Si on vient du roulement, mettre à jour l'état du roulement
                    if st.session_state.type_roulement:
                        # Récupérer le prénom du conseiller à partir du nom complet
                        prenom_conseiller = destinataire.split()[0]
                        
                        # Chercher la clé correspondant au prénom (pour être sûr d'avoir le bon format)
                        for key, value in CONSEILLERS.items():
                            if value == destinataire or key == prenom_conseiller:
                                prenom_conseiller = key
                                break
                        
                        # Mettre à jour le roulement
                        update_rotation(st.session_state.type_roulement, prenom_conseiller)
                    
                    # 4. Afficher un message de succès
                    st.success(f"✅ Contact transmis avec succès à {destinataire}!")
                    
                    # 5. Ajouter un récapitulatif des actions effectuées
                    st.markdown(
                        f"""
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <h4>Récapitulatif des actions :</h4>
                            <ul>
                                <li>Contact de {nom_client} enregistré ✓</li>
                                <li>Email envoyé à {destinataire} ✓</li>
                                {"<li>Mise à jour du roulement ✓</li>" if st.session_state.type_roulement else ""}
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # 6. Proposer des actions suivantes
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### Que souhaitez-vous faire maintenant ?")
                    
                    col_next1, col_next2, col_next3 = st.columns(3)
                    
                    with col_next1:
                        if st.button("Revenir à l'accueil", key="btn_next_home"):
                            # Réinitialiser les variables de session
                            st.session_state.type_roulement = None
                            st.session_state.conseiller_selectionne = None
                            st.session_state.type_contact_hors_roulement = None
                            change_page("accueil")
                    
                    with col_next2:
                        if st.button("Nouveau contact (même type)", key="btn_next_same"):
                            # Garder le même contexte mais vider le formulaire
                            st.experimental_rerun()
                    
                    with col_next3:
                        if st.session_state.type_roulement:
                            if st.button("Retour au roulement", key="btn_next_rotation"):
                                st.session_state.conseiller_selectionne = None
                                change_page("roulement")
                        else:
                            if st.button("Nouveau type de contact", key="btn_next_type"):
                                st.session_state.conseiller_selectionne = None
                                st.session_state.type_contact_hors_roulement = None
                                change_page("hors_roulement")
                
                else:
                    notification("Le contact a été enregistré mais l'email n'a pas pu être envoyé. Veuillez vérifier la configuration email.", "warning")
            
            else:
                notification("Une erreur est survenue lors de l'enregistrement du contact.", "error")
