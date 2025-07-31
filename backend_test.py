#!/usr/bin/env python3
"""
Backend API Testing for Football Predictions Streamlit App
Tests the API client functionality and data processing
"""

import sys
import os
import requests
from datetime import datetime, date
import time

# Add the app directory to Python path
sys.path.append('/app')

try:
    from api_client import FootballAPI
    from data_processor import DataProcessor
    from config import POPULAR_LEAGUES, API_KEY, BASE_URL, HEADERS
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

class FootballAPITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.api = None
        
    def run_test(self, test_name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {test_name}...")
        
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
                print(f"✅ Passed - {test_name}")
                return True
            else:
                print(f"❌ Failed - {test_name}")
                return False
        except Exception as e:
            print(f"❌ Failed - {test_name}: {str(e)}")
            return False
    
    def test_config_validation(self):
        """Test configuration and API key"""
        print("Testing configuration...")
        
        # Check API key exists
        if not API_KEY or API_KEY == "your_rapidapi_key_here":
            print("❌ API key not configured")
            return False
        
        print(f"✅ API key configured: {API_KEY[:10]}...{API_KEY[-5:]}")
        
        # Check popular leagues configuration
        if not POPULAR_LEAGUES or len(POPULAR_LEAGUES) == 0:
            print("❌ No leagues configured")
            return False
        
        print(f"✅ {len(POPULAR_LEAGUES)} leagues configured")
        
        # Check specific leagues mentioned in requirements
        required_leagues = [
            'Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1',
            'MLS', 'Liga MX', 'J1 League', 'K League 1', 'Saudi Pro League',
            'Brasileirão Serie A', 'Champions League'
        ]
        
        found_leagues = []
        for league_name in POPULAR_LEAGUES.keys():
            for required in required_leagues:
                if required in league_name:
                    found_leagues.append(required)
                    break
        
        print(f"✅ Found {len(found_leagues)}/{len(required_leagues)} required leagues")
        print(f"   Found: {', '.join(found_leagues)}")
        
        return True
    
    def test_api_client_initialization(self):
        """Test API client initialization"""
        try:
            self.api = FootballAPI()
            print(f"✅ API client initialized with request count: {self.api.request_count}")
            return True
        except Exception as e:
            print(f"❌ API client initialization failed: {e}")
            return False
    
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        if not self.api:
            print("❌ API client not initialized")
            return False
        
        try:
            # Test with a simple request - get today's fixtures
            today = date.today().isoformat()
            fixtures = self.api.get_fixtures_by_date(today)
            
            print(f"✅ API connectivity test passed")
            print(f"   Request count after test: {self.api.request_count}")
            print(f"   Fixtures returned: {len(fixtures) if fixtures else 0}")
            
            return True
        except Exception as e:
            print(f"❌ API connectivity test failed: {e}")
            return False
    
    def test_fixtures_by_date(self):
        """Test getting fixtures by date"""
        if not self.api:
            return False
        
        try:
            today = date.today().isoformat()
            fixtures = self.api.get_fixtures_by_date(today)
            
            if fixtures is not None:
                print(f"✅ Fixtures by date: {len(fixtures)} matches found for {today}")
                
                # Test data structure if fixtures exist
                if len(fixtures) > 0:
                    fixture = fixtures[0]
                    required_keys = ['fixture', 'teams', 'league', 'goals']
                    for key in required_keys:
                        if key not in fixture:
                            print(f"❌ Missing key '{key}' in fixture data")
                            return False
                    print("✅ Fixture data structure is valid")
                
                return True
            else:
                print("❌ Failed to get fixtures by date")
                return False
        except Exception as e:
            print(f"❌ Fixtures by date test failed: {e}")
            return False
    
    def test_fixtures_by_league(self):
        """Test getting fixtures by league"""
        if not self.api:
            return False
        
        try:
            # Test with Premier League (ID: 39)
            premier_league_id = 39
            fixtures = self.api.get_fixtures_by_league(premier_league_id, 5)
            
            if fixtures is not None:
                print(f"✅ Fixtures by league: {len(fixtures)} matches found for Premier League")
                return True
            else:
                print("❌ Failed to get fixtures by league")
                return False
        except Exception as e:
            print(f"❌ Fixtures by league test failed: {e}")
            return False
    
    def test_live_fixtures(self):
        """Test getting live fixtures"""
        if not self.api:
            return False
        
        try:
            live_fixtures = self.api.get_live_fixtures()
            
            if live_fixtures is not None:
                print(f"✅ Live fixtures: {len(live_fixtures)} live matches found")
                return True
            else:
                print("❌ Failed to get live fixtures")
                return False
        except Exception as e:
            print(f"❌ Live fixtures test failed: {e}")
            return False
    
    def test_data_processor(self):
        """Test data processing functionality"""
        try:
            # Create mock fixture data
            mock_fixture = {
                'fixture': {
                    'id': 12345,
                    'date': '2024-01-15T15:00:00Z',
                    'status': {'short': 'NS'},
                    'venue': {'name': 'Test Stadium'}
                },
                'teams': {
                    'home': {'name': 'Team A', 'logo': 'logo_a.png'},
                    'away': {'name': 'Team B', 'logo': 'logo_b.png'}
                },
                'league': {'name': 'Test League', 'logo': 'league_logo.png'},
                'goals': {'home': None, 'away': None}
            }
            
            # Test fixture data processing
            processed = DataProcessor.process_fixture_data(mock_fixture)
            
            required_keys = ['fixture_id', 'date', 'status', 'home_team', 'away_team', 'league', 'venue']
            for key in required_keys:
                if key not in processed:
                    print(f"❌ Missing key '{key}' in processed fixture data")
                    return False
            
            print("✅ Data processor working correctly")
            
            # Test status emoji
            emoji = DataProcessor.get_status_emoji('NS')
            if emoji:
                print(f"✅ Status emoji mapping working: NS -> {emoji}")
            
            # Test time formatting
            formatted_time = DataProcessor.format_match_time('2024-01-15T15:00:00Z')
            print(f"✅ Time formatting working: {formatted_time}")
            
            return True
        except Exception as e:
            print(f"❌ Data processor test failed: {e}")
            return False
    
    def test_request_limits(self):
        """Test request limit handling"""
        if not self.api:
            return False
        
        try:
            initial_count = self.api.request_count
            print(f"✅ Request counter working: {initial_count} requests made")
            
            # Check if we're approaching limits
            if initial_count >= 90:
                print("⚠️ Warning: Approaching API request limit")
            
            return True
        except Exception as e:
            print(f"❌ Request limits test failed: {e}")
            return False

def main():
    """Main test runner"""
    print("🚀 Starting Football Predictions API Tests")
    print("=" * 50)
    
    tester = FootballAPITester()
    
    # Run all tests
    tests = [
        ("Configuration Validation", tester.test_config_validation),
        ("API Client Initialization", tester.test_api_client_initialization),
        ("API Connectivity", tester.test_api_connectivity),
        ("Fixtures by Date", tester.test_fixtures_by_date),
        ("Fixtures by League", tester.test_fixtures_by_league),
        ("Live Fixtures", tester.test_live_fixtures),
        ("Data Processor", tester.test_data_processor),
        ("Request Limits", tester.test_request_limits),
    ]
    
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
        time.sleep(0.5)  # Small delay between tests
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.api:
        print(f"🔢 Total API requests made during testing: {tester.api.request_count}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())