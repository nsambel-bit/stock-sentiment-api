"""
Test script for the Stock Sentiment Analysis API
Run this after starting your API to verify everything works correctly
"""

import requests
import json

# Change this to your deployed URL or use localhost for local testing
BASE_URL = "http://localhost:5000"  # Change to your deployed URL after deployment

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check failed"
    print("✅ Health check passed!")


def test_single_analysis():
    """Test analyzing a single text"""
    print("\n" + "="*50)
    print("Testing Single Text Analysis")
    print("="*50)
    
    test_data = {
        "text": "Apple stock is performing exceptionally well with record-breaking earnings this quarter."
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Single analysis failed"
    result = response.json()
    assert "sentiment_scores" in result, "Missing sentiment_scores in response"
    assert "dominant_sentiment" in result, "Missing dominant_sentiment in response"
    print("✅ Single text analysis passed!")


def test_stock_analysis():
    """Test analyzing multiple news articles for a stock"""
    print("\n" + "="*50)
    print("Testing Stock News Analysis")
    print("="*50)
    
    test_data = {
        "symbol": "AAPL",
        "news_articles": [
            "Apple announces record profits and beats analyst expectations.",
            "Concerns about supply chain disruptions affecting Apple's production.",
            "Apple launches innovative new product line receiving mixed reviews."
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze-stock",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Stock analysis failed"
    result = response.json()
    assert "aggregate_sentiment" in result, "Missing aggregate_sentiment in response"
    assert "overall_sentiment" in result, "Missing overall_sentiment in response"
    assert result["articles_analyzed"] == 3, "Wrong number of articles analyzed"
    print("✅ Stock news analysis passed!")


def test_error_handling():
    """Test error handling with invalid requests"""
    print("\n" + "="*50)
    print("Testing Error Handling")
    print("="*50)
    
    # Test missing text field
    print("\nTest 1: Missing 'text' field")
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400, "Should return 400 for missing text"
    print("✅ Correctly handled missing text field")
    
    # Test empty news articles
    print("\nTest 2: Empty news_articles list")
    response = requests.post(
        f"{BASE_URL}/analyze-stock",
        json={"symbol": "AAPL", "news_articles": []},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400, "Should return 400 for empty articles"
    print("✅ Correctly handled empty news articles")


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 Starting API Tests".center(50, "="))
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_health_check()
        test_single_analysis()
        test_stock_analysis()
        test_error_handling()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED! Your API is working correctly.")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API.")
        print("Make sure the API is running at:", BASE_URL)
        print("\nTo start the API locally, run:")
        print("  python app.py")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════╗
║   Stock Sentiment Analysis API - Test Suite       ║
╚════════════════════════════════════════════════════╝
    
Before running these tests:
1. Make sure your API is running (python app.py)
2. Or update BASE_URL to your deployed URL
    """)
    
    run_all_tests()
