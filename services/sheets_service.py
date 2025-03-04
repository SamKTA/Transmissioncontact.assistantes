import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from utils.constants import SHEET_ID

def get_sheets_client():
    """Établit une connexion avec l'API Google Sheets en utilisant les secrets Streamlit"""
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Utiliser les secrets Streamlit pour les identifiants
    creds_dict = st.secrets["google_credentials"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    return gspread.authorize(creds)

def read_sheet_to_df(sheet_name):
    """Lit une feuille Google Sheets et la convertit en DataFrame pandas"""
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(SHEET_ID).worksheet(sheet_name)
        data = sheet.get_all_records()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors de la lecture de la feuille '{sheet_name}': {e}")
        return pd.DataFrame()

def append_to_sheet(sheet_name, row_data):
    """Ajoute une ligne de données à une feuille Google Sheets"""
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(SHEET_ID).worksheet(sheet_name)
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'ajout à la feuille '{sheet_name}': {e}")
        return False

def read_rotations():
    """Lit l'état actuel des roulements depuis Google Sheets"""
    try:
        # Lire la feuille État
        etat_df = read_sheet_to_df("État")
        
        # Lire la feuille Indisponibilités
        try:
            indispo_df = read_sheet_to_df("Indisponibilités")
        except:
            indispo_df = pd.DataFrame(columns=["Conseiller", "Début", "Fin", "Raison"])
        
        return etat_df, indispo_df
    except Exception as e:
        st.error(f"Erreur lors de la lecture des roulements: {e}")
        # Créer des données par défaut en cas d'erreur
        default_etat = pd.DataFrame({
            "Type": ["VENDEURS PROJET VENTE", "ACQUÉREURS", "VENDEURS PAS DE PROJET"],
            "Dernier_Conseiller": ["", "", ""]
        })
        default_indispo = pd.DataFrame(columns=["Conseiller", "Début", "Fin", "Raison"])
        return default_etat, default_indispo

def save_contact(donnees):
    """
    Sauvegarde les données du contact dans les feuilles Google Sheets appropriées
    - Feuille 'All': tous les contacts
    - Feuille du conseiller: contacts spécifiques à ce conseiller
    """
    # Préparer la ligne de données pour Google Sheets
    row_data = [
        donnees["date"],               # Date
        donnees["assistante"],         # Assistante
        donnees["destinataire"],       # Conseiller
        donnees["source"],             # Source
        donnees["canal"],              # Canal
        donnees["type_contact"],       # Type contact
        donnees["nom_client"],         # Nom complet client
        donnees["email_client"],       # Email client
        donnees["telephone_client"],   # Téléphone client
        donnees["commentaire"]         # Commentaire
    ]
    
    # 1. Sauvegarder dans la feuille 'All'
    all_success = append_to_sheet("All", row_data)
    
    # 2. Sauvegarder dans la feuille du conseiller (uniquement le prénom)
    conseiller_prenom = donnees["destinataire"].split()[0]
    conseiller_success = append_to_sheet(conseiller_prenom, row_data)
    
    # Si les deux opérations ont réussi
    return all_success and conseiller_success

def update_rotation(type_roulement, conseiller):
    """
    Met à jour l'état du roulement après attribution d'un contact
    - Met à jour la feuille État avec le dernier conseiller
    - Ajoute une entrée dans l'historique
    """
    try:
        client = get_sheets_client()
        doc = client.open_by_key(SHEET_ID)
        
        # 1. Mettre à jour la feuille État
        etat_sheet = doc.worksheet("État")
        
        # Trouver la ligne correspondant au type de roulement
        cellule = etat_sheet.find(type_roulement)
        if cellule:
            # Mettre à jour le dernier conseiller (colonne B)
            etat_sheet.update_cell(cellule.row, 2, conseiller)
        
        # 2. Ajouter dans l'historique
        historique_sheet = doc.worksheet("Historique")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        historique_sheet.append_row([now, type_roulement, conseiller])
        
        return True
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour du roulement: {e}")
        return False

def add_unavailability(conseiller, date_debut, date_fin, raison):
    """Ajoute une indisponibilité pour un conseiller"""
    try:
        # Formatage des dates
        debut_str = date_debut.strftime("%d/%m/%Y")
        fin_str = date_fin.strftime("%d/%m/%Y")
        
        # Ajout dans la feuille Indisponibilités
        row_data = [conseiller, debut_str, fin_str, raison]
        return append_to_sheet("Indisponibilités", row_data)
    except Exception as e:
        st.error(f"Erreur lors de l'ajout de l'indisponibilité: {e}")
        return False
