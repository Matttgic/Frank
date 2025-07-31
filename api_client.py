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
            response = requests.get(url, headers=HEADERS, timeout=30)
            self.request_count += 1
            
            # Afficher le compteur dans la sidebar
            st.sidebar.metric("Requêtes utilisées", f"{self.request_count}/{self.max_requests}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                st.error("⚠️ Limite de taux API atteinte. Veuillez patienter.")
                return None
            elif response.status_code == 403:
                st.error("🔑 Clé API invalide ou expirée.")
                return None
            else:
                st.error(f"Erreur API: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout - L'API met trop de temps à répondre")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🌐 Erreur de connexion - Vérifiez votre connexion internet")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de requête: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Erreur inattendue: {str(e)}")
            return None
    
    def get_fixtures_by_date(self, date):
        """Récupère les matchs d'une date donnée"""
        endpoint = f"/fixtures?date={date}"
        data = self._make_request(endpoint)
        return data.get('response', []) if data else []
    
    def get_fixtures_by_league(self, league_id, limit=50):
        """Récupère TOUS les matchs d'une ligue (prochains + récents)"""
        all_fixtures = []
        
        # Récupérer les prochains matchs
        endpoint_next = f"/fixtures?league={league_id}&next={min(limit//2, 25)}"
        data_next = self._make_request(endpoint_next)
        if data_next:
            all_fixtures.extend(data_next.get('response', []))
        
        # Récupérer les matchs récents
        endpoint_last = f"/fixtures?league={league_id}&last={min(limit//2, 25)}"
        data_last = self._make_request(endpoint_last)
        if data_last:
            all_fixtures.extend(data_last.get('response', []))
        
        # Supprimer les doublons basés sur l'ID
        seen_ids = set()
        unique_fixtures = []
        for fixture in all_fixtures:
            fixture_id = fixture['fixture']['id']
            if fixture_id not in seen_ids:
                seen_ids.add(fixture_id)
                unique_fixtures.append(fixture)
        
        # Trier par date (plus récents d'abord)
        unique_fixtures.sort(key=lambda x: x['fixture']['date'], reverse=True)
        
        return unique_fixtures[:limit]
    
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
