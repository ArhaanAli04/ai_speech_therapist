from flask import Flask, jsonify, request, session
from flask_cors import CORS 
from speech_to_text import speech_to_text, test_microphone
from text_to_speech import text_to_speech, get_available_voices
from nlp_pipeline import process_text
from sentiment import analyze_sentiment
from therapy_responses import generate_advanced_therapy_response
from session_manager import session_manager
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')  # Change this in production

@app.route('/')
def home():
    return jsonify({"message": "Advanced AI Speech Therapist backend is running!"})

# Session Management Endpoints

@app.route('/start-therapy-session', methods=['POST'])
def start_therapy_session():
    """Start a new therapy session"""
    try:
        session_id = session_manager.create_session()
        session['current_session_id'] = session_id
        
        # Generate welcome message
        welcome_message = "Hello! I'm your AI therapy assistant. I'm here to provide support and listen without judgment. How are you feeling today?"
        
        # Speak welcome message
        tts_result = text_to_speech(welcome_message, async_mode=False)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'welcome_message': welcome_message,
            'speech_success': tts_result['success']
        })
        
    except Exception as e:
        logger.error(f"Error starting therapy session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/continue-session', methods=['POST'])
def continue_session():
    """Continue an existing therapy session with speech input/output"""
    try:
        data = request.get_json() if request.is_json else {}
        session_id = data.get('session_id') or session.get('current_session_id')
        timeout = data.get('timeout', 10)
        phrase_time_limit = data.get('phrase_time_limit', 15)
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'No active session. Please start a session first.'
            }), 400
        
        therapy_session = session_manager.get_session(session_id)
        if not therapy_session:
            return jsonify({
                'success': False,
                'error': 'Session not found. Please start a new session.'
            }), 404
        
        logger.info(f"Continuing session {session_id}...")
        
        # Step 1: Listen to user
        stt_result = speech_to_text(timeout=timeout, phrase_time_limit=phrase_time_limit)
        if not stt_result['success']:
            return jsonify({
                'success': False,
                'step': 'speech-to-text',
                'error': stt_result['error']
            })
        
        user_input = stt_result['text']
        logger.info(f"User said: {user_input}")
        
        # Step 2: Process through NLP
        nlp_result = process_text(user_input)
        
        # Step 3: Get session context
        context = therapy_session.get_conversation_context()
        
        # Step 4: Generate contextual therapy response
        ai_response = generate_advanced_therapy_response(nlp_result, context)
        
        # Step 5: Add to session history
        therapy_session.add_exchange(user_input, nlp_result, ai_response)
        
        # Step 6: Speak the response
        tts_result = text_to_speech(ai_response, async_mode=False)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'user_input': user_input,
            'ai_response': ai_response,
            'sentiment': nlp_result['sentiment']['sentiment'],
            'topic': nlp_result['topic_category'],
            'message_count': therapy_session.message_count,
            'speech_success': tts_result['success'],
            'session_context': {
                'dominant_sentiment': therapy_session.session_context['dominant_sentiment'],
                'main_topics': therapy_session.session_context['main_topics'],
                'crisis_indicators': therapy_session.session_context['crisis_indicators']
            }
        })
        
    except Exception as e:
        logger.error(f"Error continuing session: {e}")
        return jsonify({
            'success': False,
            'step': 'session',
            'error': str(e)
        }), 500

@app.route('/end-session/<session_id>')
def end_therapy_session(session_id):
    """End a therapy session and get summary"""
    try:
        summary = session_manager.end_session(session_id)
        if summary:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'session_summary': summary
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error ending session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/session-status/<session_id>')
def get_session_status(session_id):
    """Get current session status"""
    try:
        therapy_session = session_manager.get_session(session_id)
        if not therapy_session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        context = therapy_session.get_conversation_context()
        return jsonify({
            'success': True,
            'session_status': context
        })
        
    except Exception as e:
        logger.error(f"Error getting session status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Text-based endpoints for testing
@app.route('/text-therapy', methods=['POST'])
def text_therapy():
    """Text-based therapy interaction"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        user_input = data['text']
        session_id = data.get('session_id')
        
        # Debug logging
        logger.info(f"Text therapy request - Session ID: {session_id}, Input: {user_input}")
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required. Please start a session first.'
            }), 400
        
        # Get the session
        therapy_session = session_manager.get_session(session_id)
        if not therapy_session:
            return jsonify({
                'success': False,
                'error': f'Session {session_id} not found. Please start a new session.'
            }), 404
        
        logger.info(f"Found session {session_id} with {therapy_session.message_count} messages")
        
        # Process input
        nlp_result = process_text(user_input)
        context = therapy_session.get_conversation_context()
        
        logger.info(f"Session context - is_first_message: {context.get('is_first_message')}, message_count: {context.get('message_count')}")
        
        # Generate response
        ai_response = generate_advanced_therapy_response(nlp_result, context)
        
        # Add to session BEFORE returning response
        therapy_session.add_exchange(user_input, nlp_result, ai_response)
        
        logger.info(f"Added exchange, new message count: {therapy_session.message_count}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'user_input': user_input,
            'ai_response': ai_response,
            'nlp_analysis': nlp_result,
            'message_count': therapy_session.message_count,
            'session_context': therapy_session.session_context,
            'debug_info': {
                'was_first_message': context.get('is_first_message'),
                'previous_message_count': context.get('message_count')
            }
        })
        
    except Exception as e:
        logger.error(f"Error in text therapy: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Legacy endpoints (keep for compatibility)
@app.route('/test-microphone')
def test_mic():
    result = test_microphone()
    return jsonify(result)

@app.route('/speech-to-text', methods=['POST'])
def stt_endpoint():
    try:
        data = request.get_json() if request.is_json else {}
        timeout = data.get('timeout', 5)
        phrase_time_limit = data.get('phrase_time_limit', 10)
        
        result = speech_to_text(timeout=timeout, phrase_time_limit=phrase_time_limit)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'text': '',
            'error': str(e)
        }), 500

@app.route('/text-to-speech', methods=['POST'])
def tts_endpoint():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided in request body'
            }), 400
        
        text = data['text']
        async_mode = data.get('async', False)
        
        result = text_to_speech(text, async_mode=async_mode)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/voices')
def voices_endpoint():
    result = get_available_voices()
    return jsonify(result)

@app.route('/complete-voice-therapy', methods=['POST'])
def complete_voice_therapy():
    """Complete voice-to-voice therapy session with full context"""
    try:
        data = request.get_json() if request.is_json else {}
        session_id = data.get('session_id')
        timeout = data.get('timeout', 12)
        phrase_time_limit = data.get('phrase_time_limit', 20)
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required. Please start a session first.'
            }), 400
        
        therapy_session = session_manager.get_session(session_id)
        if not therapy_session:
            return jsonify({
                'success': False,
                'error': 'Session not found. Please start a new session.'
            }), 404
        
        logger.info(f"Starting complete voice therapy for session {session_id}")
        
        # Step 1: Listen with encouraging prompts
        if therapy_session.message_count == 0:
            # First message - give more time and encouragement
            prompt_message = "I'm listening. Please share what's on your mind."
            text_to_speech(prompt_message, async_mode=False)
            timeout = 15
            phrase_time_limit = 25
        else:
            # Continuing conversation
            prompt_message = "I'm here to listen."
            text_to_speech(prompt_message, async_mode=False)
        
        # Step 2: Capture speech with extended timeouts
        stt_result = speech_to_text(timeout=timeout, phrase_time_limit=phrase_time_limit)
        if not stt_result['success']:
            # Gentle error handling
            error_response = "I didn't catch that. Would you like to try again? Take your time."
            text_to_speech(error_response, async_mode=False)
            return jsonify({
                'success': False,
                'step': 'speech-to-text',
                'error': stt_result['error'],
                'gentle_error': error_response
            })
        
        user_input = stt_result['text']
        logger.info(f"User said: {user_input}")
        
        # Step 3: Process with full NLP pipeline
        nlp_result = process_text(user_input)
        context = therapy_session.get_conversation_context()
        
        # Step 4: Generate advanced contextual response
        ai_response = generate_advanced_therapy_response(nlp_result, context)
        
        # Step 5: Add to session history
        therapy_session.add_exchange(user_input, nlp_result, ai_response)
        
        # Step 6: Speak response with proper pacing
        tts_result = text_to_speech(ai_response, async_mode=False)
        
        # Step 7: Return comprehensive session data
        return jsonify({
            'success': True,
            'session_id': session_id,
            'conversation_exchange': {
                'user_input': user_input,
                'ai_response': ai_response,
                'sentiment': nlp_result['sentiment']['sentiment'],
                'confidence': nlp_result['sentiment']['confidence'],
                'topic': nlp_result['topic_category'],
                'message_count': therapy_session.message_count
            },
            'session_context': {
                'dominant_sentiment': therapy_session.session_context['dominant_sentiment'],
                'main_topics': therapy_session.session_context['main_topics'],
                'session_duration': str(datetime.now() - therapy_session.start_time),
                'progress_indicators': therapy_session.session_context.get('progress_notes', [])
            },
            'speech_success': tts_result['success']
        })
        
    except Exception as e:
        logger.error(f"Error in complete voice therapy: {e}")
        # Gentle error response even for system errors
        error_message = "I'm experiencing some technical difficulties. Let's try again in a moment."
        text_to_speech(error_message, async_mode=False)
        return jsonify({
            'success': False,
            'step': 'system',
            'error': str(e)
        }), 500

@app.route('/session-summary/<session_id>')
def get_session_summary(session_id):
    """Get a comprehensive session summary"""
    try:
        therapy_session = session_manager.get_session(session_id)
        if not therapy_session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        summary = therapy_session.generate_session_summary()
        
        # Add therapeutic insights
        insights = []
        if summary['total_exchanges'] >= 3:
            insights.append("Client engaged in meaningful conversation")
        
        if summary['dominant_sentiment'] == 'negative':
            insights.append("Client expressed distress - follow-up recommended")
        elif summary['dominant_sentiment'] == 'positive':
            insights.append("Client showed positive emotional indicators")
        
        if 'work_stress' in summary['main_topics']:
            insights.append("Work-related stress identified as primary concern")
        
        summary['therapeutic_insights'] = insights
        
        return jsonify({
            'success': True,
            'session_summary': summary
        })
        
    except Exception as e:
        logger.error(f"Error getting session summary: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
