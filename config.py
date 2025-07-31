#3. config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration API
API_KEY = os.getenv('RAPIDAPI_KEY')
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3'

# Headers pour les requêtes
HEADERS = {
    'x-rapidapi-key': API_KEY,
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
