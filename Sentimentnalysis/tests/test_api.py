"""
Test script for the Stock Sentiment Analysis API
Run this after starting your API to verify everything works correctly
"""

import requests
import json
import unittest
from unittest.mock import patch, MagicMock


class TestStockSentimentAPI(unittest.TestCase):
    """Test cases for the Stock Sentiment Analysis API"""
    
    def setUp(self):
        """Set up test configuration"""
        self.base_url = "http://localhost:5000"  # Change to your deployed URL after deployment
        self.test_text = "Apple stock is performing exceptionally well with record-breaking earnings this quarter."
        self.test_articles = [
            "Apple announces record profits and beats analyst expectations.",
            "Concerns about supply chain disruptions affecting Apple's production.",
            "Apple launches innovative new product line receiving mixed reviews."
        ]
    
    def test_health_check(self):
        """Test the health check endpoint"""
        print("\n" + "="*50)
        print("Testing Health Check Endpoint")
        print("="*50)
        
        response = requests.get(f"{self.base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        self.assertEqual(response.status_code, 200, "Health check failed")
        self.assertIn("status", response.json())
        self.assertEqual(response.json()["status"], "active")
        print("✅ Health check passed!")

    def test_single_analysis(self):
        """Test analyzing a single text"""
        print("\n" + "="*50)
        print("Testing Single Text Analysis")
        print("="*50)
        
        test_data = {"text": self.test_text}
        
        response = requests.post(
            f"{self.base_url}/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        self.assertEqual(response.status_code, 200, "Single analysis failed")
        result = response.json()
        self.assertIn("sentiment_scores", result, "Missing sentiment_scores in response")
        self.assertIn("dominant_sentiment", result, "Missing dominant_sentiment in response")
        self.assertIn("confidence", result, "Missing confidence in response")
        
        # Verify sentiment scores structure
        sentiment_scores = result["sentiment_scores"]
        self.assertIn("positive", sentiment_scores)
        self.assertIn("negative", sentiment_scores)
        self.assertIn("neutral", sentiment_scores)
        
        # Verify scores are valid probabilities
        total_score = sum(sentiment_scores.values())
        self.assertAlmostEqual(total_score, 1.0, places=2, msg="Sentiment scores should sum to 1.0")
        
        print("✅ Single text analysis passed!")

    def test_stock_analysis(self):
        """Test analyzing multiple news articles for a stock"""
        print("\n" + "="*50)
        print("Testing Stock News Analysis")
        print("="*50)
        
        test_data = {
            "symbol": "AAPL",
            "news_articles": self.test_articles
        }
        
        response = requests.post(
            f"{self.base_url}/analyze-stock",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        self.assertEqual(response.status_code, 200, "Stock analysis failed")
        result = response.json()
        self.assertIn("aggregate_sentiment", result, "Missing aggregate_sentiment in response")
        self.assertIn("overall_sentiment", result, "Missing overall_sentiment in response")
        self.assertEqual(result["articles_analyzed"], len(self.test_articles), "Wrong number of articles analyzed")
        self.assertEqual(result["symbol"], "AAPL", "Wrong symbol returned")
        
        # Verify aggregate sentiment structure
        aggregate = result["aggregate_sentiment"]
        self.assertIn("positive", aggregate)
        self.assertIn("negative", aggregate)
        self.assertIn("neutral", aggregate)
        
        # Verify individual sentiments
        self.assertEqual(len(result["individual_sentiments"]), len(self.test_articles))
        
        print("✅ Stock news analysis passed!")

    def test_error_handling_missing_text(self):
        """Test error handling with missing text field"""
        print("\n" + "="*50)
        print("Testing Error Handling - Missing Text")
        print("="*50)
        
        response = requests.post(
            f"{self.base_url}/analyze",
            json={},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 400, "Should return 400 for missing text")
        self.assertIn("error", response.json())
        print("✅ Correctly handled missing text field")

    def test_error_handling_empty_articles(self):
        """Test error handling with empty news articles"""
        print("\n" + "="*50)
        print("Testing Error Handling - Empty Articles")
        print("="*50)
        
        response = requests.post(
            f"{self.base_url}/analyze-stock",
            json={"symbol": "AAPL", "news_articles": []},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 400, "Should return 400 for empty articles")
        self.assertIn("error", response.json())
        print("✅ Correctly handled empty news articles")

    def test_error_handling_invalid_text_type(self):
        """Test error handling with invalid text type"""
        print("\n" + "="*50)
        print("Testing Error Handling - Invalid Text Type")
        print("="*50)
        
        response = requests.post(
            f"{self.base_url}/analyze",
            json={"text": 123},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 400, "Should return 400 for invalid text type")
        self.assertIn("error", response.json())
        print("✅ Correctly handled invalid text type")

    def test_error_handling_missing_news_articles(self):
        """Test error handling with missing news_articles field"""
        print("\n" + "="*50)
        print("Testing Error Handling - Missing News Articles")
        print("="*50)
        
        response = requests.post(
            f"{self.base_url}/analyze-stock",
            json={"symbol": "AAPL"},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 400, "Should return 400 for missing news_articles")
        self.assertIn("error", response.json())
        print("✅ Correctly handled missing news_articles field")


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 Starting API Tests".center(50, "="))
    print(f"Base URL: http://localhost:5000")
    
    try:
        # Create test suite
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestStockSentimentAPI)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        if result.wasSuccessful():
            print("\n" + "="*50)
            print("✅ ALL TESTS PASSED! Your API is working correctly.")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("❌ SOME TESTS FAILED!")
            print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API.")
        print("Make sure the API is running at: http://localhost:5000")
        print("\nTo start the API locally, run:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════╗
║   Stock Sentiment Analysis API - Test Suite       ║
╚════════════════════════════════════════════════════╝
    
Before running these tests:
1. Make sure your API is running (python main.py)
2. Or update BASE_URL to your deployed URL
    """)
    
    run_all_tests()
