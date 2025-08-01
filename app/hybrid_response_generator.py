from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
import random
from typing import Dict, List

logger = logging.getLogger(__name__)

class HybridTherapyResponseGenerator:
    def __init__(self):
        # Load DialoGPT model for conversational AI
        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = None
        self.model = None
        self.load_model()
        
        # Simple intent patterns for routing decisions
        self.simple_intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'direct_question': ['how', 'what', 'why', 'when', 'can you help', 'strategies', 'advice'],
            'crisis': ['suicide', 'kill myself', 'end it all', 'want to die'],
            'simple_affirmation': ['yes', 'no', 'okay', 'sure', 'thanks']
        }
        
        # Therapy-specific prompt templates
        self.therapy_prompts = {
            'burnout': "You are an empathetic therapist. The client is experiencing burnout and work exhaustion. Respond with understanding and practical support. Client says: ",
            'anxiety': "You are a compassionate therapist. The client is expressing anxiety and worry. Provide validation and gentle exploration. Client says: ",
            'work_stress': "You are a supportive therapist. The client is dealing with work-related stress. Offer empathy and helpful perspectives. Client says: ",
            'general': "You are a caring therapist. Listen with empathy and respond therapeutically to help the client process their feelings. Client says: "
        }
    
    def load_model(self):
        """Load the DialoGPT model"""
        try:
            logger.info("Loading DialoGPT model for conversational generation...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            logger.info("DialoGPT model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load DialoGPT model: {e}")
            self.model = None
            self.tokenizer = None
    
    def determine_response_strategy(self, user_input: str, nlp_result: Dict, session_context: Dict) -> str:
        """Decide whether to use rule-based or AI generation"""
        user_text = user_input.lower()
        message_count = session_context.get('message_count', 0)
        confidence = nlp_result.get('sentiment', {}).get('confidence', 0)
        
        # Use rule-based for simple, clear cases
        for intent, keywords in self.simple_intents.items():
            if any(keyword in user_text for keyword in keywords):
                if intent in ['greeting', 'simple_affirmation', 'crisis']:
                    return 'rule_based'
        
        # Use rule-based for very first message
        if message_count == 0:
            return 'rule_based'
        
        # Use AI generation for complex emotional content
        complex_indicators = [
            'feel', 'feeling', 'emotion', 'burnout', 'exhausted', 'overwhelmed',
            'anxious', 'depressed', 'stressed', 'worried', 'scared', 'lost',
            'relationship', 'work', 'career', 'dream', 'passion'
        ]
        
        if any(indicator in user_text for indicator in complex_indicators):
            return 'ai_generation'
        
        # Use AI for questions requiring thoughtful responses
        if nlp_result.get('is_question', False) and len(user_text.split()) > 5:
            return 'ai_generation'
        
        # Default to AI generation for richer responses
        return 'ai_generation'
    
    def generate_with_transformer(self, user_input: str, nlp_result: Dict, session_context: Dict) -> str:
        """Generate response using DialoGPT transformer"""
        if not self.model or not self.tokenizer:
            return "I'm having some technical difficulties. Could you please rephrase that?"
        
        try:
            # Select appropriate prompt based on detected topic
            topic = nlp_result.get('topic_category', 'general')
            sentiment = nlp_result.get('sentiment', {}).get('sentiment', 'neutral')
            
            # Map topics to prompt templates
            if topic == 'work_stress' or 'work' in user_input.lower():
                prompt_key = 'work_stress'
            elif sentiment == 'negative' and any(word in user_input.lower() for word in ['exhausted', 'burnout', 'overwhelming']):
                prompt_key = 'burnout'
            elif sentiment == 'negative' and any(word in user_input.lower() for word in ['anxious', 'worried', 'scared']):
                prompt_key = 'anxiety'
            else:
                prompt_key = 'general'
            
            # Build context-aware prompt
            prompt = self.therapy_prompts[prompt_key] + user_input
            
            # Add conversation context if available
            recent_history = session_context.get('recent_history', [])
            if recent_history:
                context_summary = self._build_context_summary(recent_history)
                prompt = f"Previous context: {context_summary}\n\n{prompt}"
            
            # Generate response
            response = self._generate_response(prompt)
            
            # Post-process to ensure therapeutic quality
            response = self._post_process_response(response, nlp_result)
            
            logger.info(f"AI generated response: {response[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error in transformer generation: {e}")
            return "I want to make sure I understand what you're sharing. Could you tell me more about how you're feeling?"
    
    def _generate_response(self, prompt: str) -> str:
        """Core transformer generation logic"""
        # Encode the prompt
        inputs = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors='pt')
        
        # Generate response with controlled parameters
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + 100,  # Limit response length
                num_return_sequences=1,
                temperature=0.7,  # Balanced creativity
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2  # Reduce repetition
            )
        
        # Decode only the generated part
        response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        
        # Clean up the response
        response = response.strip()
        if not response:
            response = "I hear what you're saying. Can you tell me more about how this is affecting you?"
        
        return response
    
    def _build_context_summary(self, recent_history: List[Dict]) -> str:
        """Build a concise context summary from recent conversation"""
        if not recent_history:
            return ""
        
        # Get last 2 exchanges for context
        context_parts = []
        for exchange in recent_history[-2:]:
            user_input = exchange.get('user_input', '')
            topic = exchange.get('topic_category', '')
            if user_input and topic:
                context_parts.append(f"User discussed {topic}: {user_input[:50]}...")
        
        return " ".join(context_parts)
    
    def _post_process_response(self, response: str, nlp_result: Dict) -> str:
        """Ensure response meets therapeutic standards"""
        # Remove any inappropriate content (basic filtering)
        inappropriate_words = ['stupid', 'dumb', 'pathetic', 'worthless']
        for word in inappropriate_words:
            response = response.replace(word, 'challenging')
        
        # Ensure response ends appropriately
        if not response.endswith(('.', '?', '!')):
            response += "."
        
        # Add gentle follow-up if response is very short
        if len(response.split()) < 8:
            follow_ups = [
                " How does that resonate with you?",
                " What are your thoughts on this?",
                " How are you feeling about this situation?"
            ]
            response += random.choice(follow_ups)
        
        return response

# Global instance
hybrid_generator = HybridTherapyResponseGenerator()
