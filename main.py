#7. main.py
import streamlit as st
from datetime import datetime, date
import time
from api_client import FootballAPI
from data_processor import DataProcessor
from ui_components import UIComponents
from config import POPULAR_LEAGUES

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

# CSS personnalisé
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Titre principal
    st.title("⚽ Football Prédictions & Matchs")
    st.markdown("---")
    
    # Initialisation de l'API
    api = FootballAPI()
    
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
    """Affiche les matchs du jour sélectionné"""
    st.header(f"📅 Matchs du {selected_date.strftime('%d/%m/%Y')}")
    
    with st.spinner("Récupération des matchs..."):
        fixtures = get_fixtures_cached("daily", selected_date.isoformat(), max_matches)
    
    if not fixtures:
        st.warning("Aucun match trouvé pour cette date")
        return
    
    st.success(f"✅ {len(fixtures)} matchs trouvés")
    
    # Sélection des matchs pour les prédictions
    st.subheader("🎯 Prédictions")
    
    # Limiter automatiquement selon les requêtes restantes
    remaining_requests = 100 - api.request_count - 1  # -1 pour la requête fixtures
    max_predictions = min(len(fixtures), remaining_requests, max_matches)
    
    st.info(f"Affichage des prédictions pour {max_predictions} matchs (économie des requêtes API)")
    
    # Récupération et affichage des prédictions
    for i, fixture in enumerate(fixtures[:max_predictions]):
        with st.expander(f"🆚 {fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}", expanded=True):
            with st.spinner("Récupération des prédictions..."):
                prediction = api.get_predictions(fixture['fixture']['id'])
                time.sleep(0.5)  # Petite pause pour éviter de surcharger l'API
            
            UIComponents.display_match_card(fixture, prediction)

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
