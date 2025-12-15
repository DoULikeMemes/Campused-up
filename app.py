import streamlit as st
import time
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Campused Up",
    page_icon="🤝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS CUSTOM (CORRIGÉ POUR FORCER LE FOND BLANC) ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* --- 1. FORCE LE FOND BLANC (Fixe le problème de contraste) --- */
    .stApp {
        background-color: white;
        color: black;
    }
    [data-testid="stHeader"] {
        background-color: white;
    }
    
    /* --- 2. STYLE DES BOUTONS --- */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #9F2B2B;
        color: white !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 3px 5px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
         background-color: #7A2121;
         transform: scale(1.01);
    }
    
    /* --- 3. STYLE DES CARTES --- */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background-color: #F8F9FA; /* Gris très clair pour détacher du fond blanc */
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #eee;
    }

    /* --- 4. TEXTE --- */
    h1, h2, h3, p, span, div, small, label {
        color: #333333 !important;
    }
    /* Exception pour le texte dans les boutons (blanc) */
    button div { color: white !important; }
    button p { color: white !important; }
    
    .accent-text { color: #417DAB !important; font-weight: bold; }
    .student-tag { color: #666 !important; font-size: 0.85rem; }
    
    /* Force la couleur du champ de recherche */
    input {
        color: black !important;
        background-color: #f0f2f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if 'contacts_pris' not in st.session_state:
    st.session_state.contacts_pris = []
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

# --- DONNÉES ---
articles = [
    {
        "id": 1, 
        "type": "objet", 
        "titre": "Micro-ondes (Bon état)", 
        "echange_contre": "Aide révisions partiels Maths L1", 
        "img": "https://img.icons8.com/color/96/microwave.png", 
        "dist": "Résidence A", 
        "student": "Sophie L."
    },
    {
        "id": 4, 
        "type": "objet", 
        "titre": "Kit Vaisselle complet", 
        "echange_contre": "Relecture rapport de stage", 
        "img": "https://img.icons8.com/color/96/kitchen.png", 
        "dist": "1.2km", 
        "student": "Karim B."
    },
    {
        "id": 2, 
        "type": "tutorat", 
        "titre": "Tutorat Anglais (Niveau C1)", 
        "detail": "Dispo pour préparer les oraux.", 
        "img": "https://img.icons8.com/color/96/learning.png", 
        "dist": "Campus Central", 
        "student": "Thomas W."
    },
    {
        "id": 3, 
        "type": "tutorat", 
        "titre": "Aide Programmation Python", 
        "detail": "Je débloque vos projets débutants.", 
        "img": "https://img.icons8.com/dusk/96/python.png", 
        "dist": "Biblio B.U.", 
        "student": "Amina D."
    },
]

# --- FONCTIONS ---
def simuler_contact(nom_etudiant, titre_annonce):
    with st.spinner(f"Envoi du message à {nom_etudiant}..."):
        time.sleep(0.8)
    st.toast(f"✅ Demande envoyée à {nom_etudiant} !", icon="💬")
    st.session_state.contacts_pris.append(f"Contacté {nom_etudiant} pour : {titre_annonce}")
    time.sleep(0.5)
    st.rerun()

# --- HEADER & MENU ---
col_logo, col_titre = st.columns([1, 4])

with col_logo:
    # Affiche le logo s'il existe
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=80) 
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.write("🎓") 

with col_titre:
    # Titre aligné avec le logo
    st.markdown("<h1 style='text-align: left; padding-top: 10px; font-size: 2rem;'>Campused Up</h1>", unsafe_allow_html=True)

st.write("") 

c1, c2 = st.columns(2)
if c1.button("🏠 Fil d'actu"): st.session_state.page = "Accueil"
if c2.button("💬 Mes Messages"): st.session_state.page = "Messages"

st.divider()

# --- PAGE ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<div style='text-align:center; margin-bottom:15px; color:#666;'>📍 Géolocalisation active</div>", unsafe_allow_html=True)
    st.text_input("🔍 Rechercher...", placeholder="Ex: Soutien compta...")
    st.write("")

    for item in articles:
        with st.container():
            col_img, col_txt = st.columns([1, 3])
            with col_img:
                st.image(item['img'], width=70)
            with col_txt:
                if item['type'] == 'objet':
                    st.markdown(f"<h3 style='margin:0; font-size:1.2rem;'>📦 {item['titre']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:5px 0;'><span class='accent-text'>🔄 Contre :</span> {item['echange_contre']}</p>", unsafe_allow_html=True)
                elif item['type'] == 'tutorat':
                    st.markdown(f"<h3 style='margin:0; font-size:1.2rem;'>🎓 {item['titre']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin:5px 0;'>{item['detail']}</p>", unsafe_allow_html=True)

                st.markdown(f"<p class='student-tag'>👤 {item['student']} • 📍 {item['dist']}</p>", unsafe_allow_html=True)
                
                prenom = item['student'].split()[0]
                if st.button(f"💬 Contacter {prenom}", key=f"btn_{item['id']}"):
                    simuler_contact(item['student'], item['titre'])

# --- PAGE MESSAGES ---
elif st.session_state.page == "Messages":
    st.markdown("<h2>📬 Mes contacts</h2>", unsafe_allow_html=True)
    if not st.session_state.contacts_pris:
        st.info("Aucun message envoyé.")
    else:
        for contact in reversed(st.session_state.contacts_pris):
            st.markdown(f"<div style='padding:15px; background:#F8F9FA; margin-bottom:10px; border-radius:10px; border-left: 5px solid #9F2B2B;'>{contact} <br/><small style='color:#888'>En attente...</small></div>", unsafe_allow_html=True)
