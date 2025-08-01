import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TherapySession:
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.start_time = datetime.now()
        self.conversation_history = []
        self.session_context = {
            'main_topics': [],
            'dominant_sentiment': 'neutral',
            'crisis_indicators': [],
            'progress_notes': [],
            'coping_strategies_suggested': [],
            'user_name': None
        }
        self.message_count = 0
        
    def add_exchange(self, user_input: str, nlp_analysis: dict, ai_response: str):
        """Add a conversation exchange to session history"""
        exchange = {
            'timestamp': datetime.now(),
            'message_id': self.message_count,
            'user_input': user_input,
            'sentiment': nlp_analysis.get('sentiment', {}).get('sentiment', 'neutral'),
            'confidence': nlp_analysis.get('sentiment', {}).get('confidence', 0.5),
            'topic_category': nlp_analysis.get('topic_category', 'general'),
            'keywords': nlp_analysis.get('keywords', {}),
            'ai_response': ai_response,
            'response_type': nlp_analysis.get('response_type', 'exploration')
        }
        
        self.conversation_history.append(exchange)
        self.message_count += 1
        self._update_session_context(exchange)
        
        logger.info(f"Session {self.session_id}: Added exchange #{self.message_count}")
        
    def _update_session_context(self, exchange: dict):
        """Update session context based on new exchange"""
        topic = exchange['topic_category']
        sentiment = exchange['sentiment']
        
        # Track main topics
        if topic not in self.session_context['main_topics']:
            self.session_context['main_topics'].append(topic)
        
        # Update dominant sentiment (weighted by recent messages)
        if len(self.conversation_history) <= 3:
            self.session_context['dominant_sentiment'] = sentiment
        else:
            # Weight recent messages more heavily
            recent_sentiments = [ex['sentiment'] for ex in self.conversation_history[-3:]]
            if recent_sentiments.count('negative') >= 2:
                self.session_context['dominant_sentiment'] = 'negative'
            elif recent_sentiments.count('positive') >= 2:
                self.session_context['dominant_sentiment'] = 'positive'
        
        # Check for crisis indicators
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'can\'t go on', 'want to die']
        user_text_lower = exchange['user_input'].lower()
        for keyword in crisis_keywords:
            if keyword in user_text_lower and keyword not in self.session_context['crisis_indicators']:
                self.session_context['crisis_indicators'].append(keyword)
                logger.warning(f"Crisis indicator detected: {keyword}")
    
    def get_conversation_context(self, last_n_messages: int = 3) -> dict:
        """Get recent conversation context for response generation"""
        recent_history = self.conversation_history[-last_n_messages:] if self.conversation_history else []
        
        return {
            'session_id': self.session_id,
            'message_count': self.message_count,
            'session_duration': str(datetime.now() - self.start_time),
            'recent_history': recent_history,
            'session_context': self.session_context,
            'is_first_message': self.message_count == 0
        }
    
    def generate_session_summary(self) -> dict:
        """Generate a summary of the therapy session"""
        if not self.conversation_history:
            return {'summary': 'No conversation occurred', 'recommendations': []}
        
        # Analyze session patterns
        sentiments = [ex['sentiment'] for ex in self.conversation_history]
        topics = [ex['topic_category'] for ex in self.conversation_history]
        
        sentiment_counts = {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        }
        
        # Generate summary
        summary = {
            'session_duration': str(datetime.now() - self.start_time),
            'total_exchanges': len(self.conversation_history),
            'main_topics': list(set(topics)),
            'sentiment_distribution': sentiment_counts,
            'dominant_sentiment': max(sentiment_counts.items(), key=lambda x: x[1])[0],
            'crisis_indicators': self.session_context['crisis_indicators'],
            'progress_observations': self._generate_progress_observations()
        }
        
        return summary
    
    def _generate_progress_observations(self) -> List[str]:
        """Generate therapeutic observations about the session"""
        observations = []
        
        if len(self.conversation_history) >= 3:
            # Check for emotional progression
            early_sentiment = self.conversation_history[0]['sentiment']
            recent_sentiment = self.conversation_history[-1]['sentiment']
            
            if early_sentiment == 'negative' and recent_sentiment in ['neutral', 'positive']:
                observations.append("Client showed emotional improvement during session")
            elif early_sentiment in ['neutral', 'positive'] and recent_sentiment == 'negative':
                observations.append("Client's mood declined during session - follow-up recommended")
        
        # Check for engagement
        if self.message_count >= 5:
            observations.append("Client showed good engagement and willingness to communicate")
        
        # Check for specific topics
        topics = [ex['topic_category'] for ex in self.conversation_history]
        if 'work_stress' in topics:
            observations.append("Work-related stress identified as key concern")
        if 'relationships' in topics:
            observations.append("Relationship issues discussed")
        if 'mental_health' in topics:
            observations.append("Mental health concerns addressed")
            
        return observations

class SessionManager:
    def __init__(self):
        self.active_sessions: Dict[str, TherapySession] = {}
        self.session_history: Dict[str, TherapySession] = {}
        
    def create_session(self) -> str:
        """Create a new therapy session"""
        session = TherapySession()
        self.active_sessions[session.session_id] = session
        logger.info(f"Created new session: {session.session_id}")
        return session.session_id
        
    def get_session(self, session_id: str) -> Optional[TherapySession]:
        """Get an active session"""
        return self.active_sessions.get(session_id)
    
    def end_session(self, session_id: str) -> Optional[dict]:
        """End a session and generate summary"""
        session = self.active_sessions.pop(session_id, None)
        if session:
            summary = session.generate_session_summary()
            self.session_history[session_id] = session
            logger.info(f"Ended session: {session_id}")
            return summary
        return None

# Global session manager
session_manager = SessionManager()
