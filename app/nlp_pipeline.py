import re
import logging
from typing import Dict, List
from sentiment import analyze_sentiment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self):
        # Therapy-related keywords and patterns
        self.therapy_patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'feelings': ['feel', 'feeling', 'felt', 'emotion', 'emotional'],
            'problems': ['problem', 'issue', 'trouble', 'difficulty', 'struggle', 'challenge'],
            'relationships': ['relationship', 'partner', 'friend', 'family', 'parents', 'spouse'],
            'work_stress': ['work', 'job', 'boss', 'colleague', 'career', 'workplace'],
            'mental_health': ['anxiety', 'depression', 'stress', 'panic', 'overwhelmed', 'therapy']
        }
        
        self.question_patterns = [
            'how', 'what', 'why', 'when', 'where', 'who', 'can you', 'could you', 'would you'
        ]
    
    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract therapy-relevant keywords from text"""
        if not text:
            return {}
        
        text_lower = text.lower()
        found_categories = {}
        
        for category, keywords in self.therapy_patterns.items():
            found_words = []
            for keyword in keywords:
                if keyword in text_lower:
                    found_words.append(keyword)
            
            if found_words:
                found_categories[category] = found_words
        
        return found_categories
    
    def detect_question(self, text: str) -> bool:
        """Check if the text contains a question"""
        if not text:
            return False
        
        text_lower = text.lower().strip()
        
        # Check for question mark
        if '?' in text:
            return True
        
        # Enhanced question patterns - especially for help requests
        question_patterns = [
            'how', 'what', 'why', 'when', 'where', 'who', 'which',
            'can you', 'could you', 'would you', 'should i',
            'do you have', 'are there', 'is there', 'have you',
            'any suggestions', 'any advice', 'any strategies', 'any tips',
            'help me', 'what should', 'how do i', 'how can i'
        ]
        # Check for question words at the beginning
        for pattern in question_patterns:
            if pattern in text_lower:
                return True
        
        return False
    
    def categorize_topic(self, keywords: Dict[str, List[str]]) -> str:
        """Categorize the main topic based on keywords"""
        if not keywords:
            return 'general'
        
        # Priority order for topic classification
        priority_topics = ['mental_health', 'relationships', 'work_stress', 'problems', 'feelings']
        
        for topic in priority_topics:
            if topic in keywords:
                return topic
        
        # Return first found category if no priority matches
        return list(keywords.keys())[0] if keywords else 'general'
    
    def process_text(self, text: str) -> dict:
        """
        Main NLP processing function
        
        Args:
            text: Input text to process
            
        Returns:
            dict: {
                'original_text': str,
                'cleaned_text': str,
                'sentiment': dict,
                'keywords': dict,
                'is_question': bool,
                'topic_category': str,
                'response_type': str
            }
        """
        if not text or not text.strip():
            return {
                'original_text': text,
                'cleaned_text': '',
                'sentiment': {'sentiment': 'neutral', 'confidence': 0.5},
                'keywords': {},
                'is_question': False,
                'topic_category': 'general',
                'response_type': 'greeting'
            }
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Analyze sentiment
        sentiment_result = analyze_sentiment(cleaned_text)
        
        # Extract keywords
        keywords = self.extract_keywords(cleaned_text)
        
        # Detect if it's a question
        is_question = self.detect_question(cleaned_text)
        
        # Categorize topic
        topic_category = self.categorize_topic(keywords)
        
        # Determine response type
        response_type = self.determine_response_type(
            sentiment_result['sentiment'], 
            topic_category, 
            is_question,
            keywords
        )
        
        result = {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'sentiment': sentiment_result,
            'keywords': keywords,
            'is_question': is_question,
            'topic_category': topic_category,
            'response_type': response_type
        }
        
        logger.info(f"NLP Processing: topic={topic_category}, sentiment={sentiment_result['sentiment']}, response_type={response_type}")
        return result
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Basic text normalization
        text = text.lower()
        
        return text
    
    def determine_response_type(self, sentiment: str, topic: str, is_question: bool, keywords: dict) -> str:
        """Determine what type of response to generate"""
        
        # Greeting detection
        if 'greeting' in keywords:
            return 'greeting'
        
        # Crisis/urgent situations (would need more sophisticated detection in real app)
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'can\'t go on']
        text_lower = ' '.join([word for words in keywords.values() for word in words])
        if any(crisis in text_lower for crisis in crisis_keywords):
            return 'crisis'
        
        # Question responses
        if is_question:
            return 'question_response'
        
        # Sentiment-based responses
        if sentiment == 'negative':
            if topic == 'mental_health':
                return 'mental_health_support'
            elif topic == 'relationships':
                return 'relationship_support'
            else:
                return 'empathy_support'
        elif sentiment == 'positive':
            return 'positive_reinforcement'
        else:
            return 'exploration'

# Global NLP processor instance
nlp_processor = NLPProcessor()

def process_text(text: str) -> dict:
    """Convenience function for NLP processing"""
    return nlp_processor.process_text(text)
