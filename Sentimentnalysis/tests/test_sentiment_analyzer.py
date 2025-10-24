"""
Unit tests for the StockSentimentAnalyzer class
"""

import unittest
from unittest.mock import patch, MagicMock
import torch
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sentiment_analyzer import StockSentimentAnalyzer


class TestStockSentimentAnalyzer(unittest.TestCase):
    """Test cases for the StockSentimentAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_text = "Apple stock is performing exceptionally well today."
        self.sample_articles = [
            "Apple announces record profits",
            "iPhone sales exceed expectations",
            "Market concerns about supply chain issues"
        ]
    
    @patch('sentiment_analyzer.BertTokenizer')
    @patch('sentiment_analyzer.BertForSequenceClassification')
    def test_analyzer_initialization(self, mock_model_class, mock_tokenizer_class):
        """Test that the analyzer initializes correctly"""
        # Mock the tokenizer and model
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        # Initialize analyzer
        analyzer = StockSentimentAnalyzer()
        
        # Verify initialization
        self.assertEqual(analyzer.tokenizer, mock_tokenizer)
        self.assertEqual(analyzer.model, mock_model)
        mock_model.eval.assert_called_once()
        
        # Verify model and tokenizer were loaded with correct model name
        mock_tokenizer_class.from_pretrained.assert_called_with('ProsusAI/finbert')
        mock_model_class.from_pretrained.assert_called_with('ProsusAI/finbert')
    
    @patch('sentiment_analyzer.BertTokenizer')
    @patch('sentiment_analyzer.BertForSequenceClassification')
    def test_analyzer_initialization_custom_model(self, mock_model_class, mock_tokenizer_class):
        """Test that the analyzer initializes with custom model name"""
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        custom_model = 'custom/finbert-model'
        analyzer = StockSentimentAnalyzer(model_name=custom_model)
        
        mock_tokenizer_class.from_pretrained.assert_called_with(custom_model)
        mock_model_class.from_pretrained.assert_called_with(custom_model)
    
    @patch('sentiment_analyzer.BertTokenizer')
    @patch('sentiment_analyzer.BertForSequenceClassification')
    def test_analyze_sentiment(self, mock_model_class, mock_tokenizer_class):
        """Test sentiment analysis of single text"""
        # Setup mocks
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        
        # Mock tokenizer output
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3, 4]]),
            'attention_mask': torch.tensor([[1, 1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs
        
        # Mock model output - simulate logits for positive, negative, neutral
        mock_logits = torch.tensor([[2.0, 1.0, 0.5]])  # Higher score for positive
        mock_model.return_value.logits = mock_logits
        
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        # Initialize analyzer
        analyzer = StockSentimentAnalyzer()
        
        # Test sentiment analysis
        result = analyzer.analyze_sentiment(self.sample_text)
        
        # Verify tokenizer was called correctly
        mock_tokenizer.assert_called_once_with(
            self.sample_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # Verify model was called
        mock_model.assert_called_once_with(**mock_inputs)
        
        # Verify result structure
        self.assertIn('positive', result)
        self.assertIn('negative', result)
        self.assertIn('neutral', result)
        
        # Verify scores are probabilities (sum to 1)
        total_score = sum(result.values())
        self.assertAlmostEqual(total_score, 1.0, places=2)
        
        # Verify scores are positive
        for score in result.values():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
    
    @patch('sentiment_analyzer.BertTokenizer')
    @patch('sentiment_analyzer.BertForSequenceClassification')
    def test_get_stock_sentiment(self, mock_model_class, mock_tokenizer_class):
        """Test sentiment analysis of multiple articles"""
        # Setup mocks
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        
        # Mock tokenizer output
        mock_inputs = {
            'input_ids': torch.tensor([[1, 2, 3, 4]]),
            'attention_mask': torch.tensor([[1, 1, 1, 1]])
        }
        mock_tokenizer.return_value = mock_inputs
        
        # Mock model output
        mock_logits = torch.tensor([[1.5, 1.0, 1.2]])
        mock_model.return_value.logits = mock_logits
        
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        # Initialize analyzer
        analyzer = StockSentimentAnalyzer()
        
        # Test stock sentiment analysis
        symbol = "AAPL"
        result = analyzer.get_stock_sentiment(symbol, self.sample_articles)
        
        # Verify result structure
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.sample_articles))
        
        # Verify each article result
        for article_result in result:
            self.assertIn('positive', article_result)
            self.assertIn('negative', article_result)
            self.assertIn('neutral', article_result)
            
            # Verify scores are probabilities
            total_score = sum(article_result.values())
            self.assertAlmostEqual(total_score, 1.0, places=2)
        
        # Verify tokenizer was called for each article
        self.assertEqual(mock_tokenizer.call_count, len(self.sample_articles))
    
    @patch('sentiment_analyzer.BertTokenizer')
    @patch('sentiment_analyzer.BertForSequenceClassification')
    def test_analyze_sentiment_empty_text(self, mock_model_class, mock_tokenizer_class):
        """Test sentiment analysis with empty text"""
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        analyzer = StockSentimentAnalyzer()
        
        # Test with empty string
        result = analyzer.analyze_sentiment("")
        
        # Should still return valid sentiment scores
        self.assertIn('positive', result)
        self.assertIn('negative', result)
        self.assertIn('neutral', result)
    
    @patch('sentiment_analyzer.BertTokenizer')
    @patch('sentiment_analyzer.BertForSequenceClassification')
    def test_get_stock_sentiment_empty_list(self, mock_model_class, mock_tokenizer_class):
        """Test stock sentiment analysis with empty articles list"""
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
        mock_model_class.from_pretrained.return_value = mock_model
        
        analyzer = StockSentimentAnalyzer()
        
        # Test with empty articles list
        result = analyzer.get_stock_sentiment("AAPL", [])
        
        # Should return empty list
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestSentimentAnalyzerIntegration(unittest.TestCase):
    """Integration tests for the sentiment analyzer"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.test_texts = [
            "This company is doing extremely well financially",
            "The market is crashing and investors are panicking",
            "The stock price remained unchanged today"
        ]
    
    def test_sentiment_consistency(self):
        """Test that sentiment analysis is consistent"""
        # This test would require the actual model to be loaded
        # For now, we'll skip it in unit tests but it's useful for integration testing
        pass
    
    def test_different_text_lengths(self):
        """Test sentiment analysis with texts of different lengths"""
        # This test would require the actual model to be loaded
        # For now, we'll skip it in unit tests but it's useful for integration testing
        pass


if __name__ == '__main__':
    unittest.main()
