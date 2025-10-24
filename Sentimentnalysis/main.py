"""
Stock Sentiment Analysis API - Main Application
===============================================

This is the main entry point for the Stock Sentiment Analysis API.
The API uses FinBERT to analyze sentiment of financial text and news articles.

Usage Examples:
==============

1. Running the API locally:
   python main.py

2. Testing with curl commands:
   
   # Health check
   curl http://localhost:5000/
   
   # Analyze single text
   curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "Apple stock is performing exceptionally well today"}'
   
   # Analyze stock news
   curl -X POST http://localhost:5000/analyze-stock \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "AAPL",
       "news_articles": [
         "Apple announces record profits",
         "iPhone sales exceed expectations"
       ]
     }'

3. Running tests:
   python -m pytest tests/
   python tests/test_api.py

4. Deployment:
   See README.md for deployment options (Railway, Heroku, Google Cloud Run, etc.)

Features:
=========
- Financial sentiment analysis using FinBERT
- Single text sentiment analysis
- Multiple news articles sentiment analysis for stocks
- RESTful API with proper error handling
- CORS enabled for GPT integration
- Comprehensive test suite
- Ready for deployment to various platforms
"""

from src.api import create_app
import os


def main():
    """Main function to run the Flask application"""
    app = create_app()
    
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"""
╔════════════════════════════════════════════════════╗
║        Stock Sentiment Analysis API                ║
║                                                    ║
║  🚀 Starting server at http://{host}:{port}        ║
║  📊 Ready for financial sentiment analysis        ║
║  🤖 GPT Builder integration ready                 ║
╚════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
