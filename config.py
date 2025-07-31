#3. config.py
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

# Configuration API - Check both local env and Streamlit secrets
API_KEY = None

# Try to get API key from Streamlit secrets first (for Streamlit Cloud)
try:
    API_KEY = st.secrets["RAPIDAPI_KEY"]
except (KeyError, FileNotFoundError):
    # Fallback to environment variable (for local development)
    API_KEY = os.getenv('RAPIDAPI_KEY')

BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3'

# Validation de la clé API
if not API_KEY:
    print("⚠️ Warning: RAPIDAPI_KEY not found in environment variables or Streamlit secrets")

# Headers pour les requêtes
HEADERS = {
    'x-rapidapi-key': API_KEY or '',
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
}

# Limites
MAX_DAILY_REQUESTS = 100
MAX_MATCHES_PER_DAY = 20  # Pour rester sous la limite

# Ligues principales organisées par région
POPULAR_LEAGUES = {
    # === EUROPEAN TOP LEAGUES (1st Division) ===
    '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League': 39,
    '🇪🇸 La Liga': 140,
    '🇮🇹 Serie A': 135,
    '🇩🇪 Bundesliga': 78, 
    '🇫🇷 Ligue 1': 61,
    '🇳🇱 Eredivisie': 88,
    '🇵🇹 Primeira Liga': 94,
    '🇧🇪 Pro League': 144,
    '🇦🇹 Bundesliga': 218,
    '🇨🇭 Super League': 207,
    '🇹🇷 Süper Lig': 203,
    '🇬🇷 Super League': 197,
    '🇷🇺 Premier League': 235,
    '🇺🇦 Premier League': 333,
    '🇳🇴 Eliteserien': 103,
    '🇸🇪 Allsvenskan': 113,
    '🇩🇰 Superliga': 119,
    
    # === BIG 5 SECOND DIVISIONS ===
    '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Championship': 40,
    '🇪🇸 Segunda División': 141,
    '🇮🇹 Serie B': 136,
    '🇩🇪 2. Bundesliga': 79,
    '🇫🇷 Ligue 2': 62,
    
    # === EUROPEAN COMPETITIONS & QUALIFIERS ===
    '🏆 Champions League': 2,
    '🥈 Europa League': 3,
    '🥉 Conference League': 848,
    '🏆 Champions League Qualification': 531,
    '🥈 Europa League Qualification': 679,
    
    # === SOUTH AMERICA (MAIN LEAGUES) ===
    '🇧🇷 Brasileirão Serie A': 71,
    '🇦🇷 Liga Profesional': 128,
    '🇺🇾 Primera División': 218,
    '🇨🇱 Primera División': 265,
    '🇨🇴 Liga BetPlay': 239,
    
    # === NORTH & CENTRAL AMERICA ===
    '🇺🇸 MLS': 253,
    '🇲🇽 Liga MX': 262,
    
    # === ASIA ===
    '🇯🇵 J1 League': 98,
    '🇰🇷 K League 1': 292,
    '🇨🇳 Chinese Super League': 169,
    '🇸🇦 Saudi Pro League': 307,
    
    # === OCEANIA ===
    '🇦🇺 A-League': 188,
}
