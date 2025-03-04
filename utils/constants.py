# ID de la feuille Google Sheets
SHEET_ID = "1f0x47zQrmCdo9GwF_q2wTOiP9jxEvMmLevY7xmDOp4A"

# Liste des conseillers et leurs noms complets
CONSEILLERS = {
    "Clément": "Clément VIREUX",
    "Pascal": "Pascal BOFFERON",
    "Angélique": "Angélique CHENERAILLES",
    "Bertrand": "Bertrand FOURNIER",
    "Joshua": "Joshua BESSE",
    "Irina": "Irina GALOYAN",
    "Arnaud": "Arnaud SELLAM",
    "Benoît": "Benoît COUSTEAUD",
    "Orianne": "Orianne BOULESTEIX",
    "Cyril": "Cyril REINICHE",
    "Sam.test": "Sam.test"
}

# Liste des emails des conseillers
EMAILS_CONSEILLERS = {
    "Clément VIREUX": "clement.vigreux@orpi.com",
    "Pascal BOFFERON": "pascal.bofferon@orpi.com",
    "Angélique CHENERAILLES": "angélique.chenerailles@orpi.com",
    "Bertrand FOURNIER": "bertrand.fournier.agencedesarcades@orpi.com",
    "Joshua BESSE": "joshua.besse@orpi.com",
    "Irina GALOYAN": "irina@orpi.com",
    "Arnaud SELLAM": "arnaud.sellam@orpi.com",
    "Benoît COUSTEAUD": "benoît.cousteaud@orpi.com",
    "Orianne BOULESTEIX": "orianne@orpi.com",
    "Cyril REINICHE": "cyrilreiniche@orpi.com",
    "Sam.test": "skita@orpi.com"
}

# Définition des ordres de roulement pour chaque type
ROULEMENTS = {
    "VENDEURS PROJET VENTE": [
        "Joshua", "Arnaud", "Pascal", "Cyril", "Orianne", 
        "Angélique", "Clément", "Irina", "Benoît", "Sam.test", "Bertrand"
    ],
    "ACQUÉREURS": [
        "Orianne", "Clément", "Benoît", "Irina", "Joshua", 
        "Sam.test", "Cyril", "Pascal", "Bertrand", "Angélique", "Arnaud"
    ],
    "VENDEURS PAS DE PROJET": [
        "Sam.test", "Joshua", "Pascal", "Clément", "Angélique", 
        "Irina", "Bertrand", "Benoît", "Cyril", "Arnaud", "Orianne"
    ]
}

# Options pour les formulaires
SOURCES = ["LBC", "SeLoger", "SAO", "Prospection", "Notoriété", "Recommandation", "Réseaux sociaux"]
CANAUX = ["Appel téléphonique", "Passage agence", "E-mail"]
TYPES_CONTACT = ["Acheteur bien", "Acheteur", "Vendeur projet", "Vendeur pas de projet"]
ASSISTANTES = ["Laura", "Léonor", "Autre"]

# Configuration pour l'envoi d'emails
EMAIL_CONFIG = {
    "sender": "contactpro.skdigital@gmail.com",
    "smtp_server": "smtp.gmail.com",
    "port": 587,
    "subject_prefix": "🔔 +1 CONTACT : ",
    "sender_name": "Transmission Contact ORPI Arcades"
}
