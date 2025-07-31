#!/usr/bin/env python3
"""
Test du nouveau format mobile avec prédictions + conseils dans les lignes
"""

import sys
sys.path.append('/app')

from config import POPULAR_LEAGUES
from api_client import FootballAPI
from data_processor import DataProcessor

def demo_nouveau_format():
    print("🚀 NOUVEAU FORMAT MOBILE - PRÉDICTIONS + CONSEILS")
    print("=" * 60)
    
    # Simulation du nouveau format d'affichage
    print("\n📱 EXEMPLE DU NOUVEAU FORMAT:\n")
    
    # Mock data pour démonstration
    exemples = [
        {
            "match": "⏳ Liverpool vs Manchester City • 16:30",
            "prediction": "🎯 Liverpool • Double chance : Liverpool ou match nul"
        },
        {
            "match": "⚽ Arsenal vs Chelsea • 2-1",
            "prediction": "🎯 Arsenal • Victoire probable à domicile"
        },
        {
            "match": "✅ Real Madrid vs Barcelona • 3-2",
            "prediction": "🎯 Real Madrid • El Clasico toujours indécis"
        },
        {
            "match": "⏳ PSG vs Marseille • 21:00",
            "prediction": "🎯 PSG • Favori logique au Parc des Princes"
        },
        {
            "match": "🔴 Bayern Munich vs Dortmund • 1-0",
            "prediction": "🎯 Bayern Munich • Der Klassiker en cours"
        }
    ]
    
    for i, exemple in enumerate(exemples, 1):
        print(f"📋 Match {i}:")
        print(f"   {exemple['match']}")
        print(f"   {exemple['prediction']}")
        print(f"   [Cliquez pour voir détails complets]")
        print()
    
    print("🎯 AVANTAGES DU NOUVEAU FORMAT:")
    print("✅ Prédiction visible immédiatement")
    print("✅ Conseil/conseil directement affiché")
    print("✅ Pas besoin de pourcentages en première vue")
    print("✅ Information utile sans cliquer")
    print("✅ Consultation rapide sur mobile")
    print("✅ Tous les détails disponibles en cliquant")
    
    # Test avec vrais données
    print(f"\n🔧 TEST AVEC DONNÉES RÉELLES:")
    
    try:
        api = FootballAPI()
        fixtures = api.get_fixtures_by_league(39, 1)  # Premier League, 1 match
        
        if fixtures:
            fixture = fixtures[0]
            prediction = api.get_predictions(fixture['fixture']['id'])
            
            if prediction:
                fixture_data = DataProcessor.process_fixture_data(fixture)
                prediction_data = DataProcessor.process_prediction_data(prediction)
                
                home_team = fixture_data['home_team']
                away_team = fixture_data['away_team']
                status_emoji = DataProcessor.get_status_emoji(fixture_data['status'])
                score_time = DataProcessor.format_match_time(fixture_data['date'])
                
                # Nouveau format réel
                if prediction_data['winner'] != 'N/A' and prediction_data['advice'] != 'Aucun conseil disponible':
                    prediction_info = f"🎯 {prediction_data['winner']} • {prediction_data['advice']}"
                elif prediction_data['winner'] != 'N/A':
                    prediction_info = f"🎯 {prediction_data['winner']}"
                else:
                    prediction_info = "⚠️ Pas de prédiction disponible"
                
                print(f"\n✅ EXEMPLE RÉEL:")
                print(f"   {status_emoji} {home_team} vs {away_team} • {score_time}")
                print(f"   {prediction_info}")
                print(f"   [Cliquez sur cette ligne pour voir logos, graphiques, %, etc.]")
                
            else:
                print("   ⚠️ Pas de prédiction disponible pour ce match")
        else:
            print("   ⚠️ Aucun match disponible actuellement")
            
    except Exception as e:
        print(f"   ❌ Erreur de test: {e}")
    
    print(f"\n📊 CONFIGURATION:")
    print(f"   🏆 Ligues disponibles: {len(POPULAR_LEAGUES)}")
    print(f"   🌐 URL mobile: http://34.121.6.206:8502")
    print(f"   📱 Interface: Optimisée smartphone")
    print(f"   🎯 Format: Prédiction + Conseil dans la ligne")
    print(f"   👆 Détails: Cliquez sur un match pour tout voir")
    
    print(f"\n🎉 APPLICATION PRÊTE POUR MOBILE!")
    print("=" * 60)

if __name__ == "__main__":
    demo_nouveau_format()