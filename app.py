import streamlit as st
import pandas as pd # Nécessaire pour la carte
import time
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Campused Up",
    page_icon="🤝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS CUSTOM ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* FORCE LE FOND BLANC */
    .stApp { background-color: white; color: black; }
    [data-testid="stHeader"] { background-color: white; }
    
    /* BOUTONS */
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
    
    /* CARTES */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #eee;
    }

    /* TEXTE NOIR */
    h1, h2, h3, p, span, div, small, label { color: #333333 !important; }
    button div, button p { color: white !important; }
    
    .accent-text { color: #417DAB !important; font-weight: bold; }
    .student-tag { color: #666 !important; font-size: 0.85rem; }
    
    /* INPUTS */
    input { color: black !important; background-color: #f0f2f6 !important; }
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if 'contacts_pris' not in st.session_state:
    st.session_state.contacts_pris = []
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"
if 'geo_active' not in st.session_state:
    st.session_state.geo_active = False

# --- DONNÉES AVEC COORDONNÉES GPS ---
# J'ai séparé le lieu (texte) de la distance (chiffre) et ajouté lat/lon
articles = [
    {
        "id": 1, "type": "objet", "titre": "Micro-ondes (Bon état)", 
        "echange_contre": "Aide révisions Maths L1", 
        "img": "https://img.icons8.com/color/96/microwave.png", 
        "lieu": "Résidence A", "distance": "200m", 
        "lat": 48.8566, "lon": 2.3522, # Coordonnées fictives (Paris)
        "student": "Sophie L."
    },
    {
        "id": 4, "type": "objet", "titre": "Kit Vaisselle complet", 
        "echange_contre": "Relecture rapport stage", 
        "img": "https://img.icons8.com/color/96/kitchen.png", 
        "lieu": "Rue des étudiants", "distance": "1.2km", 
        "lat": 48.8600, "lon": 2.3400,
        "student": "Karim B."
    },
    {
        "id": 2, "type": "tutorat", "titre": "Tutorat Anglais (C1)", 
        "detail": "Dispo pour oraux.", 
        "img": "https://img.icons8.com/color/96/learning.png", 
        "lieu": "Campus Central", "distance": "500m", 
        "lat": 48.8584, "lon": 2.3488,
        "student": "Thomas W."
    },
    {
        "id": 3, "type": "tutorat", "titre": "Aide Python", 
        "detail": "Je débloque vos projets.", 
        "img": "https://img.icons8.com/dusk/96/python.png", 
        "lieu": "Biblio B.U.", "distance": "50m", 
        "lat": 48.8550, "lon": 2.3500,
        "student": "Amina D."
    },
]

# --- FONCTIONS ---
def simuler_contact(nom_etudiant, titre_annonce):
    with st.spinner(f"Envoi..."):
        time.sleep(0.5)
    st.toast(f"✅ Demande envoyée à {nom_etudiant} !", icon="💬")
    st.session_state.contacts_pris.append(f"Contacté {nom_etudiant} pour : {titre_annonce}")
    time.sleep(0.5)
    st.rerun()

# --- HEADER ---
col_logo, col_titre = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", width=80) 
    elif os.path.exists("logo.png"): st.image("logo.png", width=80)
    else: st.write("🎓") 
with col_titre:
    st.markdown("<h1 style='text-align: left; padding-top: 10px; font-size: 2rem;'>Campused Up</h1>", unsafe_allow_html=True)

st.write("") 
c1, c2 = st.columns(2)
if c1.button("🏠 Fil d'actu"): st.session_state.page = "Accueil"
if c2.button("💬 Mes Messages"): st.session_state.page = "Messages"

st.divider()

# --- PAGE ACCUEIL ---
if st.session_state.page == "Accueil":
    
    # CASE RGPD
    st.session_state.geo_active = st.checkbox("📍 Activer la carte & distances précises", value=st.session_state.geo_active)
    
    # --- CARTE INTERACTIVE (S'affiche seulement si coché) ---
    if st.session_state.geo_active:
        st.success("✅ Mode proximité activé.")
        # Création d'un tableau de données pour la carte
        df_map = pd.DataFrame(articles)
        # Affichage de la carte
        st.map(df_map, latitude='lat', longitude='lon', size=20, color='#9F2B2B', zoom=13)
        st.write("") # Espace
    else:
        st.info("ℹ️ Localisation approximative uniquement (Confidentialité).")
    
    st.text_input("🔍 Rechercher...", placeholder="Ex: Soutien compta...")
    st.write("")

    # BOUCLE D'AFFICHAGE DES CARTES
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

                # --- LOGIQUE D'AFFICHAGE LIEU / DISTANCE ---
                if st.session_state.geo_active:
                    # Cas 1 : Geo Active -> Lieu + Distance colorée
                    info_loc = f"📍 {item['lieu']} • <b style='color:#E91E63'>{item['distance']}</b>"
                else:
                    # Cas 2 : Geo Désactivée -> Lieu uniquement (Pas de distance)
                    info_loc = f"📍 {item['lieu']}"
                
                # Affichage de la ligne localisation
                st.markdown(f"<p class='student-tag'>👤 {item['student']} • {info_loc}</p>", unsafe_allow_html=True)
                
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
