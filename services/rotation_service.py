import streamlit as st
import pandas as pd
from datetime import datetime
from utils.constants import ROULEMENTS

def is_available(counselor, unavailability_df):
    """
    Vérifie si un conseiller est disponible à la date actuelle
    en se basant sur la feuille des indisponibilités
    """
    if unavailability_df.empty:
        return True
    
    # Date du jour
    today = datetime.now().date()
    
    # Filtrer les lignes qui concernent ce conseiller
    counselor_unavailability = unavailability_df[unavailability_df["Conseiller"] == counselor]
    
    # Si pas d'indisponibilité pour ce conseiller, il est disponible
    if counselor_unavailability.empty:
        return True
    
    # Vérifier chaque période d'indisponibilité
    for _, row in counselor_unavailability.iterrows():
        try:
            start_date = datetime.strptime(row["Début"], "%d/%m/%Y").date()
            end_date = datetime.strptime(row["Fin"], "%d/%m/%Y").date()
            
            # Si la date actuelle est comprise dans la période d'indisponibilité
            if start_date <= today <= end_date:
                return False
        except (ValueError, TypeError):
            # Si erreur de format de date, on ignore cette ligne
            continue
    
    return True

def get_next_counselor(rotation_type, last_counselor, unavailability_df, skip_list=None):
    """
    Détermine le prochain conseiller dans le roulement
    en tenant compte des indisponibilités et des sauts (skip)
    """
    # Si pas de skip_list fournie, initialiser une liste vide
    if skip_list is None:
        skip_list = []
    
    # Récupérer l'ordre de roulement pour ce type
    rotation_order = ROULEMENTS.get(rotation_type, [])
    if not rotation_order:
        return None
    
    # Si pas de dernier conseiller ou si le dernier n'est pas dans l'ordre
    if not last_counselor or last_counselor not in rotation_order:
        idx = 0
    else:
        # Trouver l'index du dernier conseiller
        idx = rotation_order.index(last_counselor)
        # Passer au suivant
        idx = (idx + 1) % len(rotation_order)
    
    # Parcourir la liste pour trouver le prochain conseiller disponible
    start_idx = idx
    while True:
        counselor = rotation_order[idx]
        
        # Vérifier si le conseiller est disponible et pas dans la liste des sauts
        if is_available(counselor, unavailability_df) and counselor not in skip_list:
            return counselor
        
        # Passer au conseiller suivant
        idx = (idx + 1) % len(rotation_order)
        
        # Si on a fait un tour complet, retourner le premier disponible
        # même s'il est dans la liste des sauts
        if idx == start_idx:
            # Nouveau tour pour trouver un conseiller disponible
            while True:
                counselor = rotation_order[idx]
                if is_available(counselor, unavailability_df):
                    return counselor
                idx = (idx + 1) % len(rotation_order)

def handle_skip(rotation_type, last_counselor, unavailability_df):
    """
    Gère le bouton "Suivant" qui permet de sauter un conseiller dans le roulement
    """
    # Récupérer les conseillers déjà sautés pour ce type de roulement
    skipped_key = f"skipped_{rotation_type}"
    if skipped_key not in st.session_state:
        st.session_state[skipped_key] = []
    
    # Déterminer le conseiller actuel (celui qu'on va sauter)
    current_counselor = get_next_counselor(rotation_type, last_counselor, unavailability_df, st.session_state[skipped_key])
    
    # Ajouter le conseiller actuel à la liste des sautés
    if current_counselor:
        st.session_state[skipped_key].append(current_counselor)
    
    # Obtenir le prochain conseiller (après le saut)
    next_counselor = get_next_counselor(rotation_type, last_counselor, unavailability_df, st.session_state[skipped_key])
    
    return next_counselor

def prioritize_previously_skipped(rotation_type, etat_df):
    """
    Vérifie s'il y a des conseillers qui ont été sautés précédemment
    et qui doivent être prioritaires pour ce type de roulement
    """
    skipped_key = f"skipped_{rotation_type}"
    
    # Si aucun conseiller n'a été sauté, pas besoin de priorisation
    if skipped_key not in st.session_state or not st.session_state[skipped_key]:
        return None
    
    # Retourner le premier conseiller de la liste des sautés
    return st.session_state[skipped_key].pop(0) if st.session_state[skipped_key] else None
