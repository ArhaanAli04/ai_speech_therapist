from textblob import TextBlob
import logging
from transformers import pipeline
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.huggingface_analyzer = None
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize sentiment analysis models"""
        try:
            # Try to load HuggingFace model (more accurate)
            logger.info("Loading HuggingFace sentiment model...")
            self.huggingface_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            logger.info("HuggingFace model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load HuggingFace model: {e}")
            logger.info("Will use TextBlob as fallback")
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def analyze_with_textblob(self, text: str) -> dict:
        """Analyze sentiment using TextBlob (simple but reliable)"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
            subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
            
            # Convert polarity to categories
            if polarity > 0.1:
                sentiment = "positive"
                confidence = polarity
            elif polarity < -0.1:
                sentiment = "negative" 
                confidence = abs(polarity)
            else:
                sentiment = "neutral"
                confidence = 1 - abs(polarity)
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'model': 'textblob'
            }
            
        except Exception as e:
            logger.error(f"TextBlob analysis failed: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'polarity': 0.0,
                'subjectivity': 0.5,
                'model': 'fallback'
            }
    
    def analyze_with_huggingface(self, text: str) -> dict:
        """Analyze sentiment using HuggingFace transformer model"""
        try:
            results = self.huggingface_analyzer(text)[0]
            
            # Convert HuggingFace labels to our format
            label_mapping = {
                'LABEL_0': 'negative',  # or 'NEGATIVE'
                'LABEL_1': 'neutral',   # or 'NEUTRAL' 
                'LABEL_2': 'positive',  # or 'POSITIVE'
                'NEGATIVE': 'negative',
                'NEUTRAL': 'neutral',
                'POSITIVE': 'positive'
            }
            
            # Find the highest confidence prediction
            best_result = max(results, key=lambda x: x['score'])
            sentiment = label_mapping.get(best_result['label'], 'neutral')
            confidence = best_result['score']
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'all_scores': results,
                'model': 'huggingface'
            }
            
        except Exception as e:
            logger.error(f"HuggingFace analysis failed: {e}")
            # Fallback to TextBlob
            return self.analyze_with_textblob(text)
    
    def analyze_sentiment(self, text: str) -> dict:
        """
        Main sentiment analysis function
        
        Args:
            text: Input text to analyze
            
        Returns:
            dict: {
                'sentiment': str,     # 'positive', 'negative', 'neutral'
                'confidence': float,  # 0.0 to 1.0
                'emotion_keywords': list,
                'model': str,
                'raw_text': str
            }
        """
        if not text or not text.strip():
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'emotion_keywords': [],
                'model': 'empty_input',
                'raw_text': text
            }
        
        cleaned_text = self.clean_text(text)
        
        # Try HuggingFace first, fallback to TextBlob
        if self.huggingface_analyzer:
            result = self.analyze_with_huggingface(cleaned_text)
        else:
            result = self.analyze_with_textblob(cleaned_text)
        
        # Add emotion keywords detection
        result['emotion_keywords'] = self.detect_emotion_keywords(cleaned_text)
        result['raw_text'] = cleaned_text
        
        logger.info(f"Sentiment analysis: {result['sentiment']} (confidence: {result['confidence']:.2f})")
        return result
    
    def detect_emotion_keywords(self, text: str) -> list:
        """Detect emotional keywords in text"""
        emotion_keywords = {
            'positive': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'good', 'better', 'best', 'love', 'like'],
            'negative': ['sad', 'depressed', 'anxious', 'worried', 'angry', 'frustrated', 'terrible', 'awful', 'hate', 'worst', 'bad'],
            'anxiety': ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic', 'stress', 'overwhelmed'],
            'depression': ['sad', 'depressed', 'hopeless', 'empty', 'lonely', 'down', 'low']
        }
        
        found_keywords = []
        text_lower = text.lower()
        
        for category, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.append({'keyword': keyword, 'category': category})
        
        return found_keywords

# Global analyzer instance
sentiment_analyzer = SentimentAnalyzer()

def analyze_sentiment(text: str) -> dict:
    """Convenience function for sentiment analysis"""
    return sentiment_analyzer.analyze_sentiment(text)
