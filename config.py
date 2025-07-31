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

# Ligues populaires avec leurs IDs
POPULAR_LEAGUES = {
    'Premier League': 39,
    'La Liga': 140,
    'Serie A': 135,
    'Bundesliga': 78,
    'Ligue 1': 61,
    'Champions League': 2
}
