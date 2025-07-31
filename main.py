#7. main.py
import streamlit as st
from datetime import datetime, date
import time
import os

# Import modules with error handling
try:
    from api_client import FootballAPI
    from data_processor import DataProcessor
    from ui_components import UIComponents
    from config import POPULAR_LEAGUES
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please check that all required files are present and properly configured.")
    st.stop()

# Configuration de la page
try:
    st.set_page_config(
        page_title="⚽ Football Prédictions",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    # Fallback if page config fails
    pass

# CSS personnalisé pour mobile
st.markdown("""
<style>
    /* Mobile optimizations */
    .main > div {
        padding-top: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* Compact metrics */
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 0.3rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Compact expander */
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main > div {
            padding-left: 0.2rem;
            padding-right: 0.2rem;
        }
        
        /* Smaller images on mobile */
        img {
            max-width: 30px !important;
            height: auto !important;
        }
        
        /* Compact text */
        .stMarkdown h1 {
            font-size: 1.5rem !important;
        }
        
        .stMarkdown h2 {
            font-size: 1.2rem !important;
        }
        
        .stMarkdown h3 {
            font-size: 1rem !important;
        }
    }
    
    /* Liste compacte des matchs */
    .streamlit-expanderContent {
        padding: 0.5rem !important;
    }
    
    /* Boutons plus compacts */
    .stButton button {
        padding: 0.3rem 0.6rem !important;
        font-size: 0.8rem !important;
    }
</style>""", unsafe_allow_html=True)

def main():
    # Titre principal
    st.title("⚽ Football Prédictions & Matchs")
    st.markdown("---")
    
    # Health check pour diagnostiquer les problèmes
    with st.expander("🔧 Diagnostic du système", expanded=False):
        st.write("**Status des composants:**")
        
        # Vérification de la clé API
        from config import API_KEY
        if API_KEY:
            st.success(f"✅ Clé API configurée: {API_KEY[:10]}...{API_KEY[-5:]}")
        else:
            st.error("❌ Clé API manquante")
            
        # Test d'import des modules
        try:
            from config import POPULAR_LEAGUES
            st.success(f"✅ Configuration chargée ({len(POPULAR_LEAGUES)} ligues)")
        except Exception as e:
            st.error(f"❌ Erreur config: {e}")
            
        # Test de connexion API
        if API_KEY:
            try:
                api_test = FootballAPI()
                st.success("✅ Client API initialisé")
            except Exception as e:
                st.error(f"❌ Erreur API client: {e}")
    
    # Vérification de la clé API
    from config import API_KEY
    if not API_KEY or API_KEY == "your_rapidapi_key_here":
        st.error("🔑 Clé API manquante!")
        st.markdown("""
        Pour utiliser cette application, vous devez:
        1. Obtenir une clé API RapidAPI pour l'API Football
        2. Dans Streamlit Cloud: Configurer dans App settings > Secrets
        3. En local: Créer un fichier .env avec RAPIDAPI_KEY=votre_clé
        """)
        st.stop()
    
    # Initialisation de l'API
    try:
        api = FootballAPI()
    except Exception as e:
        st.error(f"Erreur d'initialisation de l'API: {e}")
        st.stop()
    
    # Sidebar pour les options
    with st.sidebar:
        st.header("🎛️ Options")
        
        # Sélection du mode
        mode = st.selectbox(
            "Mode d'affichage",
            ["Matchs du jour", "Par ligue", "Matchs live"]
        )
        
        # Options selon le mode
        if mode == "Matchs du jour":
            selected_date = st.date_input(
                "Date des matchs",
                value=date.today()
            )
            max_matches = st.slider("Nombre max de matchs", 5, 30, 15)
            
        elif mode == "Par ligue":
            selected_league = st.selectbox(
                "Choisir une ligue",
                list(POPULAR_LEAGUES.keys())
            )
            max_matches = st.slider("Nombre max de matchs", 5, 20, 10)
        
        # Bouton de rafraîchissement
        if st.button("🔄 Actualiser", type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Utilisation API")
        # Le compteur sera affiché automatiquement par l'API
        
        st.markdown("---")
        st.markdown("**💡 Astuce:** Limitez le nombre de matchs pour économiser vos requêtes API")
    
    # Zone principale
    if mode == "Matchs du jour":
        display_daily_matches(api, selected_date, max_matches)
    elif mode == "Par ligue":
        display_league_matches(api, POPULAR_LEAGUES[selected_league], selected_league, max_matches)
    elif mode == "Matchs live":
        display_live_matches(api)

@st.cache_data(ttl=3600)  # Cache 1 heure
def get_fixtures_cached(mode, date_or_league_id, max_matches):
    """Version cachée pour éviter les requêtes répétées"""
    api = FootballAPI()
    
    if mode == "daily":
        return api.get_fixtures_by_date(date_or_league_id)[:max_matches]
    elif mode == "league":
        return api.get_fixtures_by_league(date_or_league_id, max_matches)
    elif mode == "live":
        return api.get_live_fixtures()
    
def display_daily_matches(api, selected_date, max_matches):
    """Affiche les matchs du jour sélectionné en format mobile-friendly"""
    st.header(f"📅 Matchs du {selected_date.strftime('%d/%m/%Y')}")
    
    with st.spinner("Récupération des matchs..."):
        fixtures = get_fixtures_cached("daily", selected_date.isoformat(), max_matches)
    
    if not fixtures:
        st.warning("Aucun match trouvé pour cette date")
        return
    
    st.success(f"✅ {len(fixtures)} matchs trouvés")
    
    # Mode complet avec prédictions
    show_predictions = st.checkbox("🎯 Afficher les prédictions (utilise plus de requêtes API)", value=False)
    
    if show_predictions:
        # Limiter automatiquement selon les requêtes restantes
        remaining_requests = 100 - api.request_count - 1
        max_predictions = min(len(fixtures), remaining_requests, 10)  # Max 10 pour économiser
        
        st.info(f"Affichage des prédictions pour {max_predictions} matchs (économie des requêtes API)")
        
        # Récupération et affichage des prédictions
        for i, fixture in enumerate(fixtures[:max_predictions]):
            with st.spinner(f"Récupération prédiction {i+1}/{max_predictions}..."):
                prediction = api.get_predictions(fixture['fixture']['id'])
                time.sleep(0.3)  # Petite pause pour éviter de surcharger l'API
            
            UIComponents.display_match_card(fixture, prediction)
    else:
        # Mode compact sans prédictions (économise les requêtes API)
        st.info("💡 Mode rapide - Cochez la case ci-dessus pour voir les prédictions")
        
        for fixture in fixtures:
            UIComponents.display_match_card(fixture, None)

def display_league_matches(api, league_id, league_name, max_matches):
    """Affiche les matchs d'une ligue"""
    st.header(f"🏆 {league_name}")
    
    with st.spinner("Récupération des matchs..."):
        fixtures = get_fixtures_cached("league", league_id, max_matches)
    
    if not fixtures:
        st.warning("Aucun match trouvé pour cette ligue")
        return
    
    st.success(f"✅ {len(fixtures)} matchs trouvés")
    
    # Récupération et affichage des prédictions
    remaining_requests = 100 - api.request_count - 1
    max_predictions = min(len(fixtures), remaining_requests)
    
    for fixture in fixtures[:max_predictions]:
        with st.expander(f"🆚 {fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}", expanded=True):
            with st.spinner("Récupération des prédictions..."):
                prediction = api.get_predictions(fixture['fixture']['id'])
                time.sleep(0.5)
            
            UIComponents.display_match_card(fixture, prediction)

def display_live_matches(api):
    """Affiche les matchs en direct"""
    st.header("🔴 Matchs en Direct")
    
    with st.spinner("Récupération des matchs live..."):
        fixtures = api.get_live_fixtures()
    
    if not fixtures:
        st.info("Aucun match en cours actuellement")
        return
    
    st.success(f"🔴 {len(fixtures)} matchs en direct")
    
    # Auto-refresh pour les matchs live
    placeholder = st.empty()
    
    for fixture in fixtures:
        with st.expander(f"🔴 {fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}", expanded=True):
            UIComponents.display_match_card(fixture, None)  # Pas de prédictions pour économiser les requêtes

if __name__ == "__main__":
    main()
