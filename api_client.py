#4. api_client.py
import requests
import streamlit as st
from datetime import datetime
import time
from config import HEADERS, BASE_URL

class FootballAPI:
    def __init__(self):
        self.request_count = 0
        self.max_requests = 100
        
    def _make_request(self, endpoint):
        """Effectue une requête avec gestion des erreurs et compteur"""
        if self.request_count >= self.max_requests:
            st.error("⚠️ Limite de requêtes atteinte pour aujourd'hui!")
            return None
            
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, headers=HEADERS, timeout=10)
            self.request_count += 1
            
            # Afficher le compteur dans la sidebar
            st.sidebar.metric("Requêtes utilisées", f"{self.request_count}/{self.max_requests}")
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Erreur API: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout - L'API met trop de temps à répondre")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion: {str(e)}")
            return None
    
    def get_fixtures_by_date(self, date):
        """Récupère les matchs d'une date donnée"""
        endpoint = f"/fixtures?date={date}"
        data = self._make_request(endpoint)
        return data.get('response', []) if data else []
    
    def get_fixtures_by_league(self, league_id, limit=10):
        """Récupère les prochains matchs d'une ligue"""
        endpoint = f"/fixtures?league={league_id}&next={limit}"
        data = self._make_request(endpoint)
        return data.get('response', []) if data else []
    
    def get_live_fixtures(self):
        """Récupère les matchs en cours"""
        endpoint = "/fixtures?live=all"
        data = self._make_request(endpoint)
        return data.get('response', []) if data else []
    
    def get_predictions(self, fixture_id):
        """Récupère les prédictions pour un match"""
        endpoint = f"/predictions?fixture={fixture_id}"
        data = self._make_request(endpoint)
        
        if data and data.get('response'):
            return data['response'][0]
        return None
    
    def reset_counter(self):
        """Remet le compteur à zéro (pour nouveau jour)"""
        self.request_count = 0
