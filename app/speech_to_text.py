import speech_recognition as sr
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def speech_to_text(timeout=5, phrase_time_limit=10):
    """
    Convert speech from microphone to text using Google Speech Recognition
    
    Args:
        timeout: Time to wait for speech to start
        phrase_time_limit: Maximum time to listen for a phrase
    
    Returns:
        dict: {'success': bool, 'text': str, 'error': str}
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        logger.info("Adjusting for ambient noise...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        logger.info("Listening for speech...")
        with microphone as source:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        
        logger.info("Processing speech...")
        text = recognizer.recognize_google(audio)
        logger.info(f"Recognized text: {text}")
        
        return {
            'success': True,
            'text': text,
            'error': None
        }
        
    except sr.WaitTimeoutError:
        error_msg = "No speech detected within timeout period"
        logger.error(error_msg)
        return {'success': False, 'text': '', 'error': error_msg}
        
    except sr.UnknownValueError:
        error_msg = "Could not understand the speech"
        logger.error(error_msg)
        return {'success': False, 'text': '', 'error': error_msg}
        
    except sr.RequestError as e:
        error_msg = f"Could not request results from speech recognition service: {e}"
        logger.error(error_msg)
        return {'success': False, 'text': '', 'error': error_msg}
        
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(error_msg)
        return {'success': False, 'text': '', 'error': error_msg}

def test_microphone():
    """
    Test if microphone is available and working
    
    Returns:
        dict: {'available': bool, 'microphones': list, 'error': str}
    """
    try:
        mics = sr.Microphone.list_microphone_names()
        return {
            'available': len(mics) > 0,
            'microphones': mics,
            'error': None
        }
    except Exception as e:
        return {
            'available': False,
            'microphones': [],
            'error': str(e)
        }
