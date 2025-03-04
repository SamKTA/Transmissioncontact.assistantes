import streamlit as st

def header(title, subtitle=None, icon=None):
    """Affiche un en-tête stylisé avec titre, sous-titre et icône optionnels"""
    if icon:
        st.markdown(f"<h1><i class='material-icons'>{icon}</i> {title}</h1>", unsafe_allow_html=True)
    else:
        st.title(title)
    
    if subtitle:
        st.markdown(f"<h3 style='color: #888;'>{subtitle}</h3>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

def card(title, content, color="#FF5A5F", footer=None):
    """Affiche une carte stylisée avec titre, contenu et pied de page optionnel"""
    st.markdown(
        f"""
        <div style="background-color: white; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid {color};">
            <h3 style="color: {color};">{title}</h3>
            <div>{content}</div>
            {f'<div style="border-top: 1px solid #eee; margin-top: 0.5rem; padding-top: 0.5rem; color: #888;">{footer}</div>' if footer else ''}
        </div>
        """,
        unsafe_allow_html=True
    )

def notification(message, type="info"):
    """Affiche une notification stylisée (info, success, warning, error)"""
    colors = {
        "info": "#2196F3",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336"
    }
    icons = {
        "info": "info",
        "success": "check_circle",
        "warning": "warning",
        "error": "error"
    }
    
    st.markdown(
        f"""
        <div style="background-color: {colors[type]}20; border-left: 5px solid {colors[type]}; border-radius: 5px; padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center;">
                <i class="material-icons" style="color: {colors[type]}; margin-right: 0.5rem;">{icons[type]}</i>
                <span>{message}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def loading_animation():
    """Affiche une animation de chargement élégante"""
    st.markdown(
        """
        <div class="loading-container">
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Chargement en cours...</p>
            </div>
        </div>
        
        <style>
        .loading-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            backdrop-filter: blur(5px);
        }
        
        .loading-spinner {
            text-align: center;
        }
        
        .spinner {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #FF5A5F;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def animated_button(label, key, on_click=None, args=None, color="#FF5A5F"):
    """Bouton animé avec effet de survol"""
    st.markdown(
        f"""
        <style>
        div[data-testid="stButton"] > button:first-child {{
            background-color: {color};
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        div[data-testid="stButton"] > button:first-child:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background-color: {color}dd;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    return st.button(label, key=key, on_click=on_click, args=args)

def load_material_icons():
    """Charge la bibliothèque d'icônes Material Design"""
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )
