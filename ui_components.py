import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_processor import DataProcessor

class UIComponents:
    
    @staticmethod
    def display_match_card(fixture, prediction):
        """Affiche une carte de match optimisée avec prédiction et conseil séparés"""
        fixture_data = DataProcessor.process_fixture_data(fixture)
        prediction_data = DataProcessor.process_prediction_data(prediction)
        
        # Format compact pour mobile et desktop
        home_team = fixture_data['home_team']
        away_team = fixture_data['away_team']
        status_emoji = DataProcessor.get_status_emoji(fixture_data['status'])
        
        # Score ou heure
        if fixture_data['score_home'] is not None:
            score_time = f"{fixture_data['score_home']}-{fixture_data['score_away']}"
        else:
            score_time = DataProcessor.format_match_time(fixture_data['date'])
        
        # Titre principal du match
        match_title = f"**{status_emoji} {home_team} vs {away_team} • {score_time}**"
        
        # Informations complémentaires
        league_info = f"🏆 {fixture_data['league']}"
        if fixture_data['venue'] != 'N/A':
            league_info += f" • 🏟️ {fixture_data['venue']}"
        
        # Prédiction et conseil séparés avec emojis distincts
        prediction_info = []
        
        if prediction_data['winner'] != 'N/A':
            # 🎯 pour la prédiction du gagnant
            prediction_info.append(f"🎯 {prediction_data['winner']}")
            
            # 💡 pour les conseils/tips
            if prediction_data['advice'] != 'Aucun conseil disponible':
                prediction_info.append(f"💡 {prediction_data['advice']}")
            
            # Informations sur les buts si disponibles
            if prediction_data['under_over'] != 'N/A':
                prediction_info.append(f"⚽ {prediction_data['under_over']}")
        else:
            prediction_info.append("⚠️ Prédictions non disponibles")
        
        # Construction du contenu de l'expander
        expander_content = f"{match_title}\n{league_info}"
        if prediction_info:
            expander_content += "\n" + "\n".join(prediction_info)
        
        # Utiliser un expander fermé par défaut avec toutes les infos essentielles
        with st.expander(expander_content, expanded=False):
            # Contenu détaillé quand on clique
            
            # Header avec équipes et logos
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.markdown(f"### 🏠 {fixture_data['home_team']}")
                if fixture_data['home_logo']:
                    try:
                        st.image(fixture_data['home_logo'], width=60)
                    except:
                        st.markdown("🔵 Logo indisponible")
            
            with col2:
                st.markdown(f"## {status_emoji}")
                if fixture_data['score_home'] is not None:
                    st.markdown(f"# **{fixture_data['score_home']} - {fixture_data['score_away']}**")
                else:
                    match_time = DataProcessor.format_match_time(fixture_data['date'])
                    st.markdown(f"## **{match_time}**")
            
            with col3:
                st.markdown(f"### 🚌 {fixture_data['away_team']}")
                if fixture_data['away_logo']:
                    try:
                        st.image(fixture_data['away_logo'], width=60)
                    except:
                        st.markdown("🔴 Logo indisponible")
            
            st.markdown("---")
            
            # Informations détaillées du match
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.markdown(f"**🏆 Compétition :** {fixture_data['league']}")
                st.markdown(f"**🏟️ Stade :** {fixture_data['venue']}")
            with info_col2:
                st.markdown(f"**📅 Date :** {fixture_data['date'][:10]}")
                st.markdown(f"**⏰ Heure :** {DataProcessor.format_match_time(fixture_data['date'])}")
            
            # Prédictions détaillées (seulement si disponibles)
            if prediction_data['winner'] != 'N/A':
                st.markdown("---")
                st.markdown("## 🎯 Analyse Complète")
                
                pred_col1, pred_col2 = st.columns(2)
                
                with pred_col1:
                    st.markdown("### 🎯 Prédictions")
                    st.success(f"**Gagnant prédit :** {prediction_data['winner']}")
                    if prediction_data['under_over'] != 'N/A':
                        st.info(f"**Buts :** {prediction_data['under_over']}")
                    
                    # Afficher les pourcentages si disponibles
                    if prediction_data['percent_home'] != '0%':
                        st.markdown("**📊 Probabilités :**")
                        st.markdown(f"• **{fixture_data['home_team']} :** {prediction_data['percent_home']}")
                        st.markdown(f"• **Match nul :** {prediction_data['percent_draw']}")
                        st.markdown(f"• **{fixture_data['away_team']} :** {prediction_data['percent_away']}")
                
                with pred_col2:
                    st.markdown("### 💡 Conseil Expert")
                    st.warning(f"*{prediction_data['advice']}*")
                    
                    # Ajout d'un indicateur de confiance basé sur les pourcentages
                    if prediction_data['percent_home'] != '0%':
                        try:
                            home_pct = float(prediction_data['percent_home'].replace('%', ''))
                            away_pct = float(prediction_data['percent_away'].replace('%', ''))
                            draw_pct = float(prediction_data['percent_draw'].replace('%', ''))
                            
                            max_pct = max(home_pct, away_pct, draw_pct)
                            if max_pct >= 60:
                                confidence = "🔥 Forte"
                            elif max_pct >= 45:
                                confidence = "⚡ Modérée"
                            else:
                                confidence = "⚠️ Faible"
                            
                            st.markdown(f"**🎲 Confiance :** {confidence}")
                        except:
                            pass
                
                # Graphique des pourcentages (seulement si données disponibles)
                if prediction_data['percent_home'] != '0%':
                    st.markdown("### 📊 Graphique des Probabilités")
                    UIComponents.display_probability_chart(
                        fixture_data['home_team'],
                        fixture_data['away_team'],
                        prediction_data
                    )
            else:
                st.markdown("---")
                st.warning("⚠️ **Prédictions non disponibles** pour ce match")
                st.info("💡 Les prédictions peuvent être indisponibles pour certains matchs ou ligues")
    
    @staticmethod
    def display_probability_chart(home_team, away_team, prediction_data):
        """Affiche un graphique des probabilités amélioré"""
        try:
            # Extraire les pourcentages
            home_pct = float(prediction_data['percent_home'].replace('%', ''))
            draw_pct = float(prediction_data['percent_draw'].replace('%', ''))
            away_pct = float(prediction_data['percent_away'].replace('%', ''))
            
            # Créer un graphique en barres moderne
            fig = go.Figure(data=[
                go.Bar(
                    x=[f"🏠 {home_team}", "⚖️ Match Nul", f"🚌 {away_team}"],
                    y=[home_pct, draw_pct, away_pct],
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                    text=[f"{home_pct}%", f"{draw_pct}%", f"{away_pct}%"],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Probabilité: %{y}%<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title={
                    'text': "📊 Probabilités de Victoire",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                yaxis_title="Pourcentage (%)",
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            # Ajouter une ligne de référence à 33.33% (probabilité égale)
            fig.add_hline(y=33.33, line_dash="dash", line_color="gray", 
                         annotation_text="Probabilité égale (33.33%)", 
                         annotation_position="top right")
            
            st.plotly_chart(fig, use_container_width=True)
            
        except (ValueError, KeyError) as e:
            st.info("📊 Données de probabilité non disponibles pour le graphique")
    
    @staticmethod
    def display_summary_stats(fixtures):
        """Affiche des statistiques résumées améliorées"""
        if not fixtures:
            return
            
        # Calculer les statistiques
        total_matches = len(fixtures)
        live_matches = len([f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE']])
        finished_matches = len([f for f in fixtures if f['fixture']['status']['short'] == 'FT'])
        upcoming_matches = len([f for f in fixtures if f['fixture']['status']['short'] == 'NS'])
        
        # Affichage en colonnes
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⚽ Total", total_matches, help="Nombre total de matchs")
        
        with col2:
            st.metric("🔴 Live", live_matches, help="Matchs en cours")
        
        with col3:
            st.metric("✅ Terminés", finished_matches, help="Matchs terminés")
        
        with col4:
            st.metric("⏳ À venir", upcoming_matches, help="Matchs à venir")
        
        # Barre de progression
        if total_matches > 0:
            progress = finished_matches / total_matches
            st.progress(progress, text=f"Progression: {finished_matches}/{total_matches} matchs terminés")