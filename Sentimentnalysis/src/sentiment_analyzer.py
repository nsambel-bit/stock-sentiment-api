"""
Stock Sentiment Analysis Module using FinBERT
"""

from transformers import BertForSequenceClassification, BertTokenizer
import torch


class StockSentimentAnalyzer:
    """
    A class to perform sentiment analysis on financial text using Finbert.
    """
    def __init__(self, model_name='ProsusAI/finbert'):
        """
        Initializes the sentiment analyzer with a Finbert model.

        Args:
            model_name (str): The name of the pre-trained Finbert model to use.
        """
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name)
        self.model.eval()  # Set the model to evaluation mode

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of the given financial text.

        Args:
            text (str): The financial text to analyze.

        Returns:
            dict: A dictionary containing the sentiment scores (positive, negative, neutral).
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        scores = torch.softmax(outputs.logits, dim=1)[0].tolist()
        sentiment_scores = {
            'positive': scores[0],
            'negative': scores[1],
            'neutral': scores[2]
        }
        return sentiment_scores

    def get_stock_sentiment(self, symbol, news_articles):
        """
        Analyzes the sentiment of a list of news articles related to a stock symbol.

        Args:
            symbol (str): The stock symbol.
            news_articles (list): A list of news article texts related to the stock.

        Returns:
            list: A list of dictionaries, where each dictionary contains the sentiment scores for a news article.
        """
        sentiment_results = []
        for article in news_articles:
            sentiment_results.append(self.analyze_sentiment(article))
        return sentiment_results
