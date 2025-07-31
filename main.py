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
st.set_page_config(
    page_title="⚽ Football Prédictions",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS optimisé pour mobile et desktop
st.markdown("""
<style>
    /* Interface propre et moderne */
    .main > div {
        padding: 0.8rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Titre principal */
    .main h1 {
        text-align: center;
        color: #1f4e79;
        margin-bottom: 2rem;
    }
    
    /* Métriques */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        border: none;
        text-align: center;
    }
    
    /* Expanders optimisés */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        padding: 0.8rem !important;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e9ecef;
        transition: all 0.2s ease;
    }
    
    /* Contenu des expanders */
    .streamlit-expanderContent {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem !important;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Boutons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main > div {
            padding: 0.4rem;
        }
        
        .streamlit-expanderHeader {
            padding: 0.6rem !important;
            font-size: 0.9rem;
        }
        
        img {
            max-width: 25px !important;
            height: auto !important;
        }
        
        .stMarkdown h1 {
            font-size: 1.8rem !important;
        }
        
        .stMarkdown h2 {
            font-size: 1.4rem !important;
        }
    }
    
    /* Animation loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
    }
</style>""", unsafe_allow_html=True)

def main():
    # Titre principal avec style
    st.markdown("# ⚽ Football Prédictions & Matchs")
    st.markdown("### 🌍 Tous les championnats du monde à votre portée")
    st.markdown("---")
    
    # Vérification de la clé API
    from config import API_KEY
    if not API_KEY or API_KEY == "your_rapidapi_key_here":
        st.error("🔑 Clé API manquante!")
        st.markdown("""
        Pour utiliser cette application, vous devez configurer votre clé API RapidAPI.
        """)
        st.stop()
    
    # Initialisation de l'API
    try:
        api = FootballAPI()
    except Exception as e:
        st.error(f"Erreur d'initialisation de l'API: {e}")
        st.stop()
    
    # Sidebar optimisée
    with st.sidebar:
        st.markdown("## 🎛️ Navigation")
        
        # Sélection du mode
        mode = st.selectbox(
            "🎯 Mode d'affichage",
            ["Matchs du jour", "Par ligue", "Matchs live"],
            help="Choisissez comment voir les matchs"
        )
        
        st.markdown("---")
        
        # Options selon le mode
        if mode == "Matchs du jour":
            st.markdown("### 📅 Configuration")
            selected_date = st.date_input(
                "Date des matchs",
                value=date.today(),
                help="Sélectionnez la date pour voir les matchs"
            )
            
            # Option pour TOUS les matchs
            show_all = st.toggle("📋 Afficher TOUS les matchs", value=True)
            if not show_all:
                max_matches = st.slider("Nombre max de matchs", 10, 100, 50)
            else:
                max_matches = 1000  # Très élevé pour récupérer tout
            
        elif mode == "Par ligue":
            st.markdown("### 🏆 Configuration")
            
            # Grouper les ligues par région pour meilleure UX
            regions = {
                "🇪🇺 Europe Top": [k for k in POPULAR_LEAGUES.keys() if any(x in k for x in ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'])],
                "🇪🇺 Europe Autres": [k for k in POPULAR_LEAGUES.keys() if any(x in k for x in ['Eredivisie', 'Primeira Liga', 'Pro League', 'Super League', 'Süper Lig', 'Eliteserien', 'Allsvenskan', 'Superliga'])],
                "🏆 Compétitions EU": [k for k in POPULAR_LEAGUES.keys() if 'Champions League' in k or 'Europa League' in k or 'Conference League' in k],
                "📈 Europe 2nd Div": [k for k in POPULAR_LEAGUES.keys() if any(x in k for x in ['Championship', 'Segunda División', 'Serie B', '2. Bundesliga', 'Ligue 2'])],
                "🌎 Amériques": [k for k in POPULAR_LEAGUES.keys() if any(x in k for x in ['🇧🇷', '🇦🇷', '🇺🇸', '🇲🇽', '🇺🇾', '🇨🇱', '🇨🇴'])],
                "🌏 Asie": [k for k in POPULAR_LEAGUES.keys() if any(x in k for x in ['🇯🇵', '🇰🇷', '🇨🇳', '🇸🇦'])],
                "🌏 Océanie": [k for k in POPULAR_LEAGUES.keys() if '🇦🇺' in k]
            }
            
            selected_region = st.selectbox("🌍 Région", list(regions.keys()))
            selected_league = st.selectbox("🏆 Ligue", regions[selected_region])
            
            # Option pour TOUS les matchs de la ligue
            show_all = st.toggle("📋 Afficher TOUS les matchs", value=True)
            if not show_all:
                max_matches = st.slider("Nombre max de matchs", 5, 50, 25)
            else:
                max_matches = 100  # Élevé pour récupérer tout
        
        st.markdown("---")
        
        # Options de prédictions
        st.markdown("### 🎯 Prédictions")
        show_predictions = st.toggle("💡 Activer les prédictions", value=False, help="Active les prédictions (consomme des requêtes API)")
        
        if show_predictions:
            prediction_limit = st.slider("Max prédictions", 5, 50, 20, help="Limite pour économiser l'API")
        else:
            prediction_limit = 0
        
        # Bouton de rafraîchissement
        st.markdown("---")
        if st.button("🔄 Actualiser", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        # Informations utiles
        st.markdown("---")
        st.markdown("### 📊 Informations")
        st.info(f"🏆 {len(POPULAR_LEAGUES)} ligues disponibles")
        
        # Aide
        with st.expander("💡 Aide rapide"):
            st.markdown("""
            **🎯 Mode d'utilisation :**
            - **Matchs du jour** : Tous les matchs d'une date
            - **Par ligue** : Matchs spécifiques d'une ligue
            - **Matchs live** : Matchs en cours maintenant
            
            **📱 Mobile :**
            - Format compact pour smartphone
            - Cliquez sur un match pour les détails
            - Toggle prédictions pour économiser l'API
            """)
    
    # Zone principale avec le mode sélectionné
    if mode == "Matchs du jour":
        display_daily_matches(api, selected_date, max_matches, show_predictions, prediction_limit)
    elif mode == "Par ligue":
        display_league_matches(api, POPULAR_LEAGUES[selected_league], selected_league, max_matches, show_predictions, prediction_limit)
    elif mode == "Matchs live":
        display_live_matches(api)

@st.cache_data(ttl=1800)  # Cache 30 minutes pour plus de réactivité
def get_fixtures_cached(mode, date_or_league_id, max_matches):
    """Version cachée pour éviter les requêtes répétées"""
    api = FootballAPI()
    
    if mode == "daily":
        all_fixtures = api.get_fixtures_by_date(date_or_league_id)
        return all_fixtures[:max_matches] if max_matches < 1000 else all_fixtures
    elif mode == "league":
        return api.get_fixtures_by_league(date_or_league_id, max_matches)
    elif mode == "live":
        return api.get_live_fixtures()

def display_daily_matches(api, selected_date, max_matches, show_predictions, prediction_limit):
    """Affiche TOUS les matchs du jour sélectionné"""
    st.markdown(f"## 📅 Matchs du {selected_date.strftime('%d/%m/%Y')}")
    
    with st.spinner("🔍 Récupération de tous les matchs..."):
        fixtures = get_fixtures_cached("daily", selected_date.isoformat(), max_matches)
    
    if not fixtures:
        st.warning("😔 Aucun match trouvé pour cette date")
        st.info("💡 Essayez une autre date ou vérifiez que c'est une journée de matchs")
        return
    
    # Statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚽ Total Matchs", len(fixtures))
    with col2:
        live_count = len([f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE']])
        st.metric("🔴 En Direct", live_count)
    with col3:
        finished_count = len([f for f in fixtures if f['fixture']['status']['short'] == 'FT'])
        st.metric("✅ Terminés", finished_count)
    
    st.markdown("---")
    
    # Affichage des matchs
    if show_predictions and prediction_limit > 0:
        remaining_requests = max(0, 100 - api.request_count - 1)
        actual_predictions = min(len(fixtures), remaining_requests, prediction_limit)
        
        st.info(f"🎯 Affichage avec prédictions pour {actual_predictions} matchs (économie API : {100 - api.request_count} requêtes restantes)")
        
        # Matchs avec prédictions
        for i, fixture in enumerate(fixtures[:actual_predictions]):
            with st.spinner(f"⚽ Analyse match {i+1}/{actual_predictions}..."):
                prediction = api.get_predictions(fixture['fixture']['id'])
                time.sleep(0.2)  # Pause courte
            UIComponents.display_match_card(fixture, prediction)
        
        # Matchs restants sans prédictions
        if len(fixtures) > actual_predictions:
            st.markdown(f"### 📋 Autres matchs ({len(fixtures) - actual_predictions} restants)")
            st.info("💡 Matchs sans prédictions pour économiser l'API")
            for fixture in fixtures[actual_predictions:]:
                UIComponents.display_match_card(fixture, None)
    else:
        st.info(f"⚡ Mode rapide : {len(fixtures)} matchs sans prédictions")
        for fixture in fixtures:
            UIComponents.display_match_card(fixture, None)

def display_league_matches(api, league_id, league_name, max_matches, show_predictions, prediction_limit):
    """Affiche TOUS les matchs d'une ligue"""
    st.markdown(f"## 🏆 {league_name}")
    
    with st.spinner("🔍 Récupération des matchs de la ligue..."):
        fixtures = get_fixtures_cached("league", league_id, max_matches)
    
    if not fixtures:
        st.warning(f"😔 Aucun match trouvé pour {league_name}")
        st.info("💡 Cette ligue pourrait être en pause ou hors saison")
        return
    
    # Statistiques de la ligue
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚽ Matchs Trouvés", len(fixtures))
    with col2:
        upcoming_count = len([f for f in fixtures if f['fixture']['status']['short'] == 'NS'])
        st.metric("⏳ À Venir", upcoming_count)
    with col3:
        st.metric("🏆 Ligue ID", league_id)
    
    st.markdown("---")
    
    # Affichage des matchs
    if show_predictions and prediction_limit > 0:
        remaining_requests = max(0, 100 - api.request_count - 1)
        actual_predictions = min(len(fixtures), remaining_requests, prediction_limit)
        
        st.info(f"🎯 Prédictions pour {actual_predictions} matchs")
        
        for fixture in fixtures[:actual_predictions]:
            with st.spinner("🔮 Récupération prédiction..."):
                prediction = api.get_predictions(fixture['fixture']['id'])
                time.sleep(0.2)
            UIComponents.display_match_card(fixture, prediction)
        
        # Matchs restants
        if len(fixtures) > actual_predictions:
            st.markdown(f"### 📋 Autres matchs ({len(fixtures) - actual_predictions} restants)")
            for fixture in fixtures[actual_predictions:]:
                UIComponents.display_match_card(fixture, None)
    else:
        for fixture in fixtures:
            UIComponents.display_match_card(fixture, None)

def display_live_matches(api):
    """Affiche TOUS les matchs en direct"""
    st.markdown("## 🔴 Matchs en Direct")
    
    with st.spinner("🔍 Recherche des matchs live..."):
        fixtures = api.get_live_fixtures()
    
    if not fixtures:
        st.info("😴 Aucun match en cours actuellement")
        st.markdown("💡 **Conseil :** Les matchs live sont plus fréquents les week-ends et en soirée européenne")
        
        # Suggérer des alternatives
        st.markdown("### 🔄 Alternatives :")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 Voir les matchs d'aujourd'hui"):
                st.session_state.mode = "Matchs du jour"
                st.rerun()
        with col2:
            if st.button("🏆 Parcourir par ligue"):
                st.session_state.mode = "Par ligue"
                st.rerun()
        return
    
    # Statistiques live
    st.metric("🔴 Matchs en Direct", len(fixtures))
    st.markdown("---")
    
    # Affichage des matchs live (pas de prédictions pour économiser l'API)
    for fixture in fixtures:
        UIComponents.display_match_card(fixture, None)
    
    # Auto-refresh suggestion
    st.markdown("---")
    st.info("🔄 Les matchs live se mettent à jour automatiquement. Cliquez sur 'Actualiser' pour les dernières infos.")

if __name__ == "__main__":
    main()