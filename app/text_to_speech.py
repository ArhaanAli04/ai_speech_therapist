import pyttsx3
import logging
import threading
from typing import Optional
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_new_tts_engine():
    """Create a fresh TTS engine instance"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        
        # Set voice if available
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        return engine
    except Exception as e:
        logger.error(f"Failed to create TTS engine: {e}")
        return None

def text_to_speech_simple(text: str) -> dict:
    """
    Simple text-to-speech that creates a fresh engine each time
    """
    if not text or not text.strip():
        return {'success': False, 'error': 'No text provided'}
    
    try:
        # Create fresh engine for each request
        engine = create_new_tts_engine()
        if not engine:
            return {'success': False, 'error': 'Could not initialize TTS engine'}
        
        logger.info(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        
        # Clean up
        engine.stop()
        del engine
        
        return {'success': True, 'error': None}
        
    except Exception as e:
        error_msg = f"Error during speech synthesis: {e}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}

# Main function for backward compatibility
def text_to_speech(text: str, async_mode: bool = False) -> dict:
    """
    Convert text to speech (simplified version)
    """
    return text_to_speech_simple(text)

def get_available_voices() -> dict:
    """Get list of available voices"""
    try:
        engine = create_new_tts_engine()
        if not engine:
            return {'voices': [], 'error': 'Could not initialize TTS engine'}
        
        voices = engine.getProperty('voices')
        voice_list = []
        
        if voices:
            for voice in voices:
                voice_list.append({
                    'id': voice.id,
                    'name': voice.name,
                    'age': getattr(voice, 'age', 'Unknown'),
                    'gender': getattr(voice, 'gender', 'Unknown')
                })
        
        engine.stop()
        del engine
        return {'voices': voice_list, 'error': None}
        
    except Exception as e:
        return {'voices': [], 'error': str(e)}
