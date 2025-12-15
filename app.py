import streamlit as st
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Campused Up",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS CUSTOM (CORRECTIF COULEURS) ---
st.markdown("""
<style>
    /* Masquer le menu standard Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 1. FORCE LE TITRE EN VIOLET */
    h1 {
        color: #4F46E5 !important;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        padding-bottom: 20px;
    }

    /* 2. STYLE DES BOUTONS */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #4F46E5;
        color: white !important; /* Texte bouton toujours blanc */
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 3. STYLE DES CARTES (Fond blanc + Texte NOIR forcé) */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        border: 1px solid #eee;
    }

    /* 4. FORCER LA COULEUR DU TEXTE DANS LES CARTES */
    /* Cela cible les titres (h3), le texte (p) et les petits textes (small/caption) */
    h3, p, span, div {
        color: #333333 !important; /* Gris très foncé pour être lisible */
    }
    
    /* Exception : Remettre le texte des boutons en blanc car la règle 4 les impacte parfois */
    button div {
        color: white !important;
    }
    
    /* Style pour les prix/distances */
    .info-tag {
        font-weight: bold;
        color: #4F46E5 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- STATE (Mémoire) ---
if 'solde' not in st.session_state:
    st.session_state.solde = 45
if 'panier' not in st.session_state:
    st.session_state.panier = []
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

# --- DONNÉES ---
articles = [
    {"id": 1, "titre": "Micro-ondes (Troc)", "prix": 0, "desc": "Contre aide déménagement", "img": "https://img.icons8.com/color/96/microwave.png", "dist": "200m"},
    {"id": 2, "titre": "Soutien Anglais", "prix": 10, "desc": "Niveau C1 - 1h", "img": "https://img.icons8.com/color/96/learning.png", "dist": "Campus B"},
    {"id": 3, "titre": "Covoit' Supermarché", "prix": 2, "desc": "Départ 18h résidence", "img": "https://img.icons8.com/color/96/fiat-500.png", "dist": "Parking"},
    {"id": 4, "titre": "Kit Vaisselle", "prix": 15, "desc": "Assiettes + couverts", "img": "https://img.icons8.com/color/96/plates.png", "dist": "1.2km"},
]

# --- FONCTIONS ---
def installer_app():
    with st.spinner("Installation..."):
        time.sleep(1.5)
    st.balloons()
    st.toast("✅ App installée sur l'écran d'accueil !")

# --- HEADER & MENU ---
st.title("🚀 Campused Up")

# Menu de navigation
c1, c2, c3 = st.columns(3)
if c1.button("🏠 Accueil"): st.session_state.page = "Accueil"
if c2.button("🎒 Profil"): st.session_state.page = "Profil"
if c3.button("📲 Installer"): installer_app()

st.divider()

# --- PAGE ACCUEIL ---
if st.session_state.page == "Accueil":
    # On force la couleur ici aussi pour être sûr
    st.markdown(f"<div style='color: #333;'>📍 Géolocalisation active • Solde : <b style='color:#4F46E5'>{st.session_state.solde} €</b></div>", unsafe_allow_html=True)
    
    st.text_input("🔍 Rechercher...", placeholder="Ex: Cours de maths...")

    st.write("") # Petit espace

    # Affichage des articles
    for item in articles:
        with st.container():
            col_img, col_txt = st.columns([1, 3])
            
            with col_img:
                st.image(item['img'], width=70)
            
            with col_txt:
                # Utilisation de HTML direct pour garantir la couleur
                st.markdown(f"<h3 style='margin:0; padding:0; font-size:1.2rem; color:black;'>{item['titre']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0; color:#666; font-size:0.9rem;'>{item['desc']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin:0; color:#4F46E5; font-size:0.8rem; font-weight:bold;'>📍 {item['dist']}</p>", unsafe_allow_html=True)

                if item['prix'] == 0:
                    btn_label = "🤝 Proposer Troc"
                else:
                    btn_label = f"Acheter ({item['prix']} €)"

                if st.button(btn_label, key=item['id']):
                    if st.session_state.solde >= item['prix']:
                        st.session_state.solde -= item['prix']
                        st.session_state.panier.append(item['titre'])
                        st.toast("✅ Deal validé !")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Pas assez d'argent !")

# --- PAGE PROFIL ---
elif st.session_state.page == "Profil":
    st.markdown("<h2 style='color:black;'>Mon Espace</h2>", unsafe_allow_html=True)
    st.info(f"💰 Solde actuel : {st.session_state.solde} €")
    
    st.markdown("<h3 style='color:black;'>🎒 Mes Deals</h3>", unsafe_allow_html=True)
    
    if not st.session_state.panier:
        st.markdown("<p style='color:#666;'>Aucun historique.</p>", unsafe_allow_html=True)
    else:
        for p in st.session_state.panier:
            st.markdown(f"<div style='padding:10px; background:white; margin-bottom:5px; border-radius:5px; color:black;'>✅ {p}</div>", unsafe_allow_html=True)
