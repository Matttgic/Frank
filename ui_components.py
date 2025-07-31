#6. ui_components.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_processor import DataProcessor

class UIComponents:
    
    @staticmethod
    def display_match_card(fixture, prediction):
        """Affiche une carte de match compacte et mobile-friendly avec prédiction et conseil dans le titre"""
        fixture_data = DataProcessor.process_fixture_data(fixture)
        prediction_data = DataProcessor.process_prediction_data(prediction)
        
        # Format compact pour mobile
        home_team = fixture_data['home_team']
        away_team = fixture_data['away_team']
        status_emoji = DataProcessor.get_status_emoji(fixture_data['status'])
        
        # Score ou heure
        if fixture_data['score_home'] is not None:
            score_time = f"{fixture_data['score_home']}-{fixture_data['score_away']}"
        else:
            score_time = DataProcessor.format_match_time(fixture_data['date'])
        
        # Prédiction et conseil directement dans le titre
        prediction_info = ""
        if prediction_data['winner'] != 'N/A' and prediction_data['advice'] != 'Aucun conseil disponible':
            # Format: "🎯 Gagnant • Conseil"
            prediction_info = f"🎯 {prediction_data['winner']} • {prediction_data['advice']}"
        elif prediction_data['winner'] != 'N/A':
            # Seulement le gagnant si pas de conseil
            prediction_info = f"🎯 {prediction_data['winner']}"
        else:
            prediction_info = "⚠️ Pas de prédiction disponible"
        
        # Titre compact pour l'expander avec toutes les infos essentielles
        match_title = f"**{status_emoji} {home_team} vs {away_team} • {score_time}**"
        prediction_line = f"{prediction_info}"
        
        # Utiliser un expander fermé par défaut avec info complète
        with st.expander(f"{match_title}\n{prediction_line}", expanded=False):
            # Contenu détaillé quand on clique
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown(f"**🏠 {fixture_data['home_team']}**")
                if fixture_data['home_logo']:
                    st.image(fixture_data['home_logo'], width=40)
            
            with col2:
                st.markdown(f"### {status_emoji}")
                if fixture_data['score_home'] is not None:
                    st.markdown(f"**{fixture_data['score_home']} - {fixture_data['score_away']}**")
                else:
                    match_time = DataProcessor.format_match_time(fixture_data['date'])
                    st.markdown(f"**{match_time}**")
            
            with col3:
                st.markdown(f"**🚌 {fixture_data['away_team']}**")
                if fixture_data['away_logo']:
                    st.image(fixture_data['away_logo'], width=40)
            
            # Informations du match
            st.markdown(f"🏆 **{fixture_data['league']}** • 🏟️ {fixture_data['venue']}")
            
            # Prédictions détaillées avec pourcentages
            if prediction_data['winner'] != 'N/A':
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🎯 Prédictions Détaillées")
                    st.markdown(f"**Gagnant prédit:** {prediction_data['winner']}")
                    st.markdown(f"**Buts:** {prediction_data['under_over']}")
                    
                    # Afficher les pourcentages dans la vue détaillée
                    if prediction_data['percent_home'] != '0%':
                        st.markdown("**Probabilités:**")
                        st.markdown(f"• {fixture_data['home_team']}: {prediction_data['percent_home']}")
                        st.markdown(f"• Match nul: {prediction_data['percent_draw']}")
                        st.markdown(f"• {fixture_data['away_team']}: {prediction_data['percent_away']}")
                    
                with col2:
                    st.markdown("### 💡 Conseil Complet")
                    st.markdown(f"*{prediction_data['advice']}*")
                
                # Graphique des pourcentages seulement dans la vue détaillée
                if prediction_data['percent_home'] != '0%':
                    UIComponents.display_probability_chart(
                        fixture_data['home_team'],
                        fixture_data['away_team'],
                        prediction_data
                    )
            else:
                st.warning("⚠️ Prédictions non disponibles pour ce match")
    
    @staticmethod
    def display_probability_chart(home_team, away_team, prediction_data):
        """Affiche un graphique des probabilités"""
        try:
            # Extraire les pourcentages
            home_pct = float(prediction_data['percent_home'].replace('%', ''))
            draw_pct = float(prediction_data['percent_draw'].replace('%', ''))
            away_pct = float(prediction_data['percent_away'].replace('%', ''))
            
            fig = go.Figure(data=[
                go.Bar(
                    x=[home_team, 'Match Nul', away_team],
                    y=[home_pct, draw_pct, away_pct],
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
                )
            ])
            
            fig.update_layout(
                title="Probabilités de victoire",
                yaxis_title="Pourcentage (%)",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except ValueError:
            st.info("Données de probabilité non disponibles")
    
    @staticmethod
    def display_summary_stats(df):
        """Affiche des statistiques résumées"""
        if df.empty:
            return
            
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_matches = len(df)
            st.metric("Total Matchs", total_matches)
        
        with col2:
            live_matches = len(df[df['status'].isin(['1H', '2H', 'HT'])])
            st.metric("Matchs Live", live_matches)
        
        with col3:
            finished_matches = len(df[df['status'] == 'FT'])
            st.metric("Matchs Terminés", finished_matches)
        
        with col4:
            upcoming_matches = len(df[df['status'] == 'NS'])
            st.metric("À Venir", upcoming_matches)
