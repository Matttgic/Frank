# Football Predictions Streamlit App

A French football predictions application that displays match information and predictions using RapidAPI's Football API.

## Features

- 📅 Daily match view with date selection
- 🏆 League-specific match display
- 🔴 Live matches monitoring
- 🎯 Match predictions with probability charts
- 📊 API usage tracking (100 requests/day limit)
- 🎨 Responsive design with team logos

## Deployment on Streamlit Cloud

### Prerequisites

1. **RapidAPI Account**: Get a free account at [RapidAPI](https://rapidapi.com/)
2. **Football API Subscription**: Subscribe to the [API-FOOTBALL](https://rapidapi.com/api-sports/api/api-football/) on RapidAPI
3. **API Key**: Get your RapidAPI key from your dashboard

### Streamlit Cloud Setup

1. **Fork/Clone** this repository to your GitHub account
2. **Connect to Streamlit Cloud**: 
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
3. **Configure Secrets**:
   - In your Streamlit Cloud app dashboard, go to "App settings" > "Secrets"
   - Add the following:
     ```toml
     RAPIDAPI_KEY = "your_actual_rapidapi_key_here"
     ```
4. **Deploy**: Click "Deploy" and your app will be live!

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file with your API key:
   ```
   RAPIDAPI_KEY=your_actual_rapidapi_key_here
   ```
4. Run the app:
   ```bash
   streamlit run main.py
   ```

## Usage

- **Matchs du jour**: View matches for a specific date
- **Par ligue**: Browse matches by popular leagues (Premier League, La Liga, etc.)
- **Matchs live**: See currently ongoing matches
- Use the sidebar to control display options and monitor API usage

## API Limits

- Free tier: 100 requests per day
- The app includes built-in request tracking and caching to optimize usage

## Technologies Used

- **Streamlit**: Web app framework
- **Plotly**: Interactive charts
- **Pandas**: Data processing
- **RapidAPI Football API**: Match data and predictions

## Support

For issues with deployment or functionality, check:
1. API key is correctly configured
2. All dependencies are installed
3. API limits haven't been exceeded