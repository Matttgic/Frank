#5. data_processor.py
import pandas as pd
from datetime import datetime
import streamlit as st

class DataProcessor:
    
    @staticmethod
    def process_fixture_data(fixture):
        """Traite les données d'un match"""
        return {
            'fixture_id': fixture['fixture']['id'],
            'date': fixture['fixture']['date'],
            'status': fixture['fixture']['status']['short'],
            'home_team': fixture['teams']['home']['name'],
            'away_team': fixture['teams']['away']['name'],
            'home_logo': fixture['teams']['home']['logo'],
            'away_logo': fixture['teams']['away']['logo'],
            'league': fixture['league']['name'],
            'league_logo': fixture['league']['logo'],
            'venue': fixture['fixture']['venue']['name'] if fixture['fixture']['venue'] else 'N/A',
            'score_home': fixture['goals']['home'],
            'score_away': fixture['goals']['away']
        }
    
    @staticmethod
    def process_prediction_data(prediction):
        """Traite les données de prédiction"""
        if not prediction:
            return {
                'winner': 'N/A',
                'win_or_draw': 'N/A',
                'under_over': 'N/A',
                'advice': 'Prédictions non disponibles',
                'percent_home': 0,
                'percent_draw': 0,
                'percent_away': 0
            }
        
        predictions = prediction.get('predictions', {})
        
        return {
            'winner': predictions.get('winner', {}).get('name', 'N/A'),
            'win_or_draw': predictions.get('win_or_draw', 'N/A'),
            'under_over': predictions.get('under_over', 'N/A'),
            'advice': predictions.get('advice', 'Aucun conseil disponible'),
            'percent_home': predictions.get('percent', {}).get('home', '0%'),
            'percent_draw': predictions.get('percent', {}).get('draw', '0%'),
            'percent_away': predictions.get('percent', {}).get('away', '0%')
        }
    
    @staticmethod
    def create_matches_dataframe(fixtures_with_predictions):
        """Crée un DataFrame avec tous les matchs et prédictions"""
        data = []
        
        for fixture, prediction in fixtures_with_predictions:
            fixture_data = DataProcessor.process_fixture_data(fixture)
            prediction_data = DataProcessor.process_prediction_data(prediction)
            
            # Combine les données
            match_data = {**fixture_data, **prediction_data}
            data.append(match_data)
        
        return pd.DataFrame(data)
    
    @staticmethod
    def format_match_time(date_str):
        """Formate l'heure du match"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%H:%M')
        except:
            return 'N/A'
    
    @staticmethod
    def get_status_emoji(status):
        """Retourne un emoji selon le statut du match"""
        status_map = {
            'NS': '⏳',  # Not Started
            '1H': '⚽',  # First Half
            '2H': '⚽',  # Second Half
            'HT': '☕',  # Half Time
            'FT': '✅',  # Full Time
            'AET': '⏱️', # After Extra Time
            'PEN': '🥅', # Penalties
            'PST': '⏸️', # Postponed
            'CANC': '❌', # Cancelled
            'LIVE': '🔴'  # Live generic
        }
        return status_map.get(status, '❓')
