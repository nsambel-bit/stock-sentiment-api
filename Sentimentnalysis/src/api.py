"""
Flask API endpoints for Stock Sentiment Analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from .sentiment_analyzer import StockSentimentAnalyzer


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for OpenAI to access your API
    
    # Initialize the analyzer once when the app starts
    print("Loading FinBERT model... This may take a moment.")
    analyzer = StockSentimentAnalyzer()
    print("Model loaded successfully!")
    
    @app.route('/', methods=['GET'])
    def home():
        """Health check endpoint"""
        return jsonify({
            "status": "active",
            "message": "Stock Sentiment Analysis API is running",
            "endpoints": {
                "/analyze": "POST - Analyze sentiment of a single text",
                "/analyze-stock": "POST - Analyze sentiment for multiple news articles about a stock"
            }
        })

    @app.route('/analyze', methods=['POST'])
    def analyze_single():
        """
        Endpoint to analyze sentiment of a single text.
        
        Expected JSON body:
        {
            "text": "Your financial text here"
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({
                    "error": "Missing 'text' field in request body"
                }), 400
            
            text = data['text']
            
            if not text or not isinstance(text, str):
                return jsonify({
                    "error": "'text' must be a non-empty string"
                }), 400
            
            sentiment = analyzer.analyze_sentiment(text)
            
            # Determine dominant sentiment
            dominant_sentiment = max(sentiment, key=sentiment.get)
            
            return jsonify({
                "text": text,
                "sentiment_scores": sentiment,
                "dominant_sentiment": dominant_sentiment,
                "confidence": sentiment[dominant_sentiment]
            })
        
        except Exception as e:
            return jsonify({
                "error": f"An error occurred: {str(e)}"
            }), 500

    @app.route('/analyze-stock', methods=['POST'])
    def analyze_stock():
        """
        Endpoint to analyze sentiment for multiple news articles about a stock.
        
        Expected JSON body:
        {
            "symbol": "AAPL",
            "news_articles": [
                "Article text 1",
                "Article text 2"
            ]
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'news_articles' not in data:
                return jsonify({
                    "error": "Missing 'news_articles' field in request body"
                }), 400
            
            symbol = data.get('symbol', 'UNKNOWN')
            news_articles = data['news_articles']
            
            if not isinstance(news_articles, list):
                return jsonify({
                    "error": "'news_articles' must be a list of strings"
                }), 400
            
            if not news_articles:
                return jsonify({
                    "error": "'news_articles' list cannot be empty"
                }), 400
            
            sentiment_results = analyzer.get_stock_sentiment(symbol, news_articles)
            
            # Calculate aggregate sentiment
            aggregate = {
                'positive': sum(s['positive'] for s in sentiment_results) / len(sentiment_results),
                'negative': sum(s['negative'] for s in sentiment_results) / len(sentiment_results),
                'neutral': sum(s['neutral'] for s in sentiment_results) / len(sentiment_results)
            }
            
            overall_sentiment = max(aggregate, key=aggregate.get)
            
            return jsonify({
                "symbol": symbol,
                "articles_analyzed": len(news_articles),
                "individual_sentiments": sentiment_results,
                "aggregate_sentiment": aggregate,
                "overall_sentiment": overall_sentiment,
                "confidence": aggregate[overall_sentiment]
            })
        
        except Exception as e:
            return jsonify({
                "error": f"An error occurred: {str(e)}"
            }), 500
    
    return app
