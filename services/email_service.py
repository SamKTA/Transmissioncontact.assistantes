import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.constants import EMAIL_CONFIG, EMAILS_CONSEILLERS

def get_email_template(data):
    """
    Génère le contenu de l'email à partir des données du formulaire
    selon le template défini
    """
    return f"""Bonjour {data['destinataire'].split()[0]},

Un contact {data['type_contact'].lower()} souhaite que tu le recontactes ou que tu confirmes un rendez-vous avec lui (à vérifier dans les commentaires). Justement, voici le commentaire !

{data['commentaire']}

Voici les coordonnées du client :

{data['nom_client']} 
{data['email_client']}
{data['telephone_client']}

Bon appel & bonne journée à toi
"""

def get_email_subject(data):
    """Génère le sujet de l'email à partir des données du formulaire"""
    return f"{EMAIL_CONFIG['subject_prefix']}{data['nom_client']} - {data['type_contact'].upper()}"

def send_email(data):
    """
    Envoie un email au conseiller destinataire avec les informations du contact
    """
    try:
        # Récupérer l'adresse email du destinataire
        destinataire_email = EMAILS_CONSEILLERS.get(data['destinataire'], "")
        if not destinataire_email:
            st.error(f"Adresse email introuvable pour {data['destinataire']}")
            return False
        
        # Configuration du serveur SMTP
        smtp_server = EMAIL_CONFIG['smtp_server']
        port = EMAIL_CONFIG['port']
        sender_email = EMAIL_CONFIG['sender']
        
        # Récupérer le mot de passe à partir des secrets Streamlit
        password = st.secrets["email_password"]
        
        # Préparer le message
        message = MIMEMultipart()
        message["From"] = f"{EMAIL_CONFIG['sender_name']} <{sender_email}>"
        message["To"] = destinataire_email
        message["Subject"] = get_email_subject(data)
        
        # Ajouter le corps du message
        email_content = get_email_template(data)
        message.attach(MIMEText(email_content, "plain"))
        
        # Connexion et envoi
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, destinataire_email, message.as_string())
        
        return True
    
    except smtplib.SMTPAuthenticationError:
        st.error("Erreur d'authentification SMTP. Vérifiez les identifiants.")
        return False
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email: {e}")
        return False
