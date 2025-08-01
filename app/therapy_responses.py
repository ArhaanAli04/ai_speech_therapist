import random
import logging
from typing import Dict, List, Optional
from hybrid_response_generator import hybrid_generator
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedTherapyResponseGenerator:
    def __init__(self):
        # Enhanced response templates with therapeutic techniques
        self.response_templates = {
            'greeting': [
                "Hello! I'm here to listen and support you. How are you feeling today?",
                "Welcome to our session. I'm glad you're here. What's on your mind?",
                "Hi there! This is a safe space for you. What would you like to explore today?",
                "Good to see you! I'm here to help. How can I support you right now?"
            ],
            
            'follow_up_greeting': [
                "How have you been since we last talked?",
                "I'm glad you're back. What's been on your mind lately?",
                "Welcome back! How are things going for you?",
                "It's good to continue our conversation. What would you like to focus on today?"
            ],
            
            'reflection': [
                "It sounds like you're saying {reflection}. Is that accurate?",
                "Let me reflect back what I'm hearing: {reflection}. How does that resonate with you?",
                "I'm hearing that {reflection}. Does that capture how you're feeling?",
                "What I'm understanding is {reflection}. Is there more to it than that?"
            ],
            
            'validation': [
                "Your feelings are completely valid. It's understandable that you would feel this way.",
                "Thank you for sharing that with me. What you're experiencing makes a lot of sense.",
                "I can see why this would be difficult for you. Your reaction is very normal.",
                "It takes courage to acknowledge these feelings. You're being very brave."
            ],
            
            'empathy_support': [
                "I can hear the pain in your words. This sounds really difficult for you.",
                "It sounds like you're carrying a heavy burden right now. You don't have to face this alone.",
                "I can sense how much this is affecting you. That must be exhausting.",
                "This sounds overwhelming. It's okay to feel this way given what you're going through."
            ],
            
            'mental_health_support': [
                "Mental health struggles are real and deserve attention. How are you taking care of yourself?",
                "It's brave of you to talk about this. Mental health is just as important as physical health.",
                "You're not alone in this experience. Many people struggle with similar feelings.",
                "Thank you for trusting me with this. What kind of support feels most helpful right now?"
            ],
            
            'coping_strategies': [
                "Have you tried any coping strategies that have helped in the past?",
                "Let's think about some ways you might manage these feelings. What has worked for you before?",
                "There are some techniques that might help. Would you be interested in exploring some options?",
                "What do you do to take care of yourself when you're feeling this way?"
            ],
            
            'exploration': [
                "Tell me more about that. I'm interested in understanding your experience better.",
                "That's important. Can you help me understand what that means to you?",
                "I'd like to explore this further with you. What comes up when you think about this?",
                "That sounds significant. What thoughts or feelings does that bring up for you?"
            ],
            
            'crisis': [
                "I'm very concerned about your safety right now. Have you thought about getting immediate help?",
                "These feelings are serious, and I want to make sure you're safe. Do you have someone you can call?",
                "Your life is valuable. Please consider reaching out to a crisis hotline: National Suicide Prevention Lifeline 988.",
                "I'm worried about you. Have you considered going to an emergency room or calling 911?"
            ],
            
            'positive_reinforcement': [
                "I can hear the strength in your words. That takes real courage.",
                "It sounds like you're finding some positive ways to cope. That's wonderful.",
                "I'm glad to hear there are some bright spots for you. What's contributing to these good feelings?",
                "That sounds like progress! How does it feel to recognize that positive change?"
            ],
            
            'session_closing': [
                "As we wrap up, what feels most important from our conversation today?",
                "What are you taking away from our session today?",
                "How are you feeling as we end our time together?",
                "Is there anything else you'd like to share before we close?"
            ],

            'exploration': [
                "Tell me more about that. I'm interested in understanding your experience better.",
                "That's important. Can you help me understand what that means to you?",
                "I'd like to explore this further with you. What comes up when you think about this?",
                "That sounds significant. What thoughts or feelings does that bring up for you?",
                "Help me understand this better - what does this experience feel like for you?",
                "I'm curious about your perspective on this. What stands out most to you?",
                "What would you say is the most challenging part of what you're describing?",
                "When you think about this situation, what comes to mind first?",
                "I want to make sure I understand - how has this been affecting you?",
                "What's it like for you when you're experiencing this?"
            ],
            
            'empathy_support': [
                "I can hear the pain in your words. This sounds really difficult for you.",
                "It sounds like you're carrying a heavy burden right now. That must be exhausting.",
                "I can sense how much this is affecting you. You're not alone in feeling this way.",
                "This sounds overwhelming. It takes strength to share something so personal.",
                "I understand this is hard for you. Your feelings make complete sense given what you're going through.",
                "It's clear this situation is causing you real distress. Thank you for trusting me with this.",
                "What you're describing sounds incredibly challenging to navigate.",
                "I can imagine how isolating this must feel. Your courage in sharing this is meaningful.",
                "This sounds like it's been weighing on you heavily. How long have you been carrying this?",
                "Your struggle is valid and your feelings are completely understandable."
            ]
        }
        
        self.coping_strategies = {
            'anxiety': [
                "Try deep breathing: inhale for 4 counts, hold for 4, exhale for 6",
                "Ground yourself using the 5-4-3-2-1 technique: notice 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
                "Progressive muscle relaxation can help reduce physical tension",
                "Mindfulness meditation, even for 5 minutes, can calm anxiety"
            ],
            'depression': [
                "Even small activities like making your bed can create a sense of accomplishment",
                "Try to spend a few minutes outside each day - sunlight and fresh air can help mood",
                "Connecting with one supportive person, even briefly, can make a difference",
                "Gentle movement or stretching can boost mood-regulating chemicals in your brain"
            ],
            'stress': [
                "Breaking large problems into smaller, manageable steps can reduce overwhelm",
                "Time management techniques like the Pomodoro method might help",
                "Regular breaks during stressful work can prevent burnout",
                "Physical exercise is one of the most effective stress relievers"
            ],
            'general': [
                "Journaling can help you process and understand your feelings better",
                "Establishing a routine can provide structure and stability",
                "Practicing gratitude, even for small things, can shift perspective",
                "Self-compassion - treating yourself as kindly as you would a good friend"
            ]
        }
        
        self.therapeutic_techniques = {
            'cognitive_reframing': [
                "Let's examine that thought. Is there another way to look at this situation?",
                "What evidence supports this belief? What evidence might challenge it?",
                "If a friend told you this about themselves, what would you say to them?",
                "What would be a more balanced way to think about this?"
            ],
            'behavioral_activation': [
                "What activities used to bring you joy? How might we incorporate those back in?",
                "What's one small step you could take this week toward feeling better?",
                "How might your environment be affecting your mood? Any changes you could make?",
                "What would a good day look like for you right now?"
            ],
            'mindfulness': [
                "Let's focus on the present moment. What are you aware of right now in your body?",
                "Can you notice these thoughts and feelings without judging them?",
                "What would it be like to observe these emotions as temporary visitors?",
                "How might accepting these feelings, rather than fighting them, change your experience?"
            ]
        }

    

    def generate_contextual_response(self, nlp_result: Dict, session_context: Dict) -> str:
        """Generate response based on NLP analysis and session context"""
        response_type = nlp_result.get('response_type', 'exploration')
        sentiment = nlp_result.get('sentiment', {}).get('sentiment', 'neutral')
        topic_category = nlp_result.get('topic_category', 'general')
        is_first_message = session_context.get('is_first_message', True)
        message_count = session_context.get('message_count', 0)
        recent_history = session_context.get('recent_history', [])
        is_question = nlp_result.get('is_question', False)
        user_text = nlp_result.get('original_text', '').lower()

        logger.info(f"Generating contextual response: type={response_type}, message_count={message_count}, sentiment={sentiment}")
        
        # Get recent AI responses to avoid repetition
        recent_responses = [exchange.get('ai_response', '') for exchange in recent_history[-3:]]
        
        # PRIORITY 1: Handle direct questions/requests for help
        if is_question or any(keyword in user_text for keyword in ['strategies', 'help', 'advice', 'suggestions', 'tips', 'how do i', 'what should']):
            return self._handle_direct_question(user_text, topic_category, recent_responses)

        # PRIORITY 2: Handle specific content themes
        if any(keyword in user_text for keyword in ['burnout', 'exhausted', 'overwhelmed', 'pressure', 'racing mind', 'overthinking']):
            return self._handle_burnout_stress(user_text, message_count, recent_responses)
        
        # PRIORITY 3: Handle work-related concerns specifically
        if topic_category == 'work_stress' or any(keyword in user_text for keyword in ['work', 'job', 'career', 'workplace', 'colleague']):
            return self._handle_work_stress(user_text, sentiment, recent_responses)
        
        # PRIORITY 4: Handle emotional expressions
        if sentiment == 'negative' and any(keyword in user_text for keyword in ['scared', 'worry', 'anxious', 'fear', 'losing interest']):
            return self._handle_emotional_distress(user_text, recent_responses)

        # Crisis handling (highest priority)
        if self._detect_crisis_language(nlp_result.get('original_text', '')):
            return self._get_varied_response('crisis', recent_responses)
        
        # Check if user is actually greeting
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        user_text_lower = nlp_result.get('original_text', '').lower()
        is_actual_greeting = any(keyword in user_text_lower for keyword in greeting_keywords)
        
        # Only give greeting response if user actually said a greeting
        if is_first_message and is_actual_greeting:
            return self._get_varied_response('greeting', recent_responses)
        
        # Generate varied therapeutic response based on content
        if sentiment == 'negative':
            if topic_category == 'work_stress':
                work_responses = [
                    "I can hear that work is creating significant stress and anxiety for you. That sounds really challenging to deal with.",
                    "Work-related stress can be overwhelming. It sounds like this is really weighing on you.",
                    "I sense that your job is causing you considerable distress. Let's explore what's making work so difficult.",
                    "Work stress can affect every part of your life. How long have you been feeling this way about your job?",
                    "It sounds like work has become a major source of anxiety for you. That must be exhausting."
                ]
                base_response = random.choice([r for r in work_responses if r not in recent_responses] or work_responses)
                
            elif topic_category == 'mental_health':
                mental_health_responses = [
                    "I understand you're struggling with difficult feelings right now. That takes courage to acknowledge and share.",
                    "Mental health challenges can feel isolating, but you're not alone in this. Thank you for opening up.",
                    "It's brave of you to talk about your mental health. These feelings deserve attention and care.",
                    "Mental health struggles are real and valid. I'm here to support you through this difficult time.",
                    "Acknowledging mental health concerns shows self-awareness and strength. How can I best support you?"
                ]
                base_response = random.choice([r for r in mental_health_responses if r not in recent_responses] or mental_health_responses)
            else:
                base_response = self._get_varied_response('empathy_support', recent_responses)
                
        elif sentiment == 'positive':
            base_response = self._get_varied_response('positive_reinforcement', recent_responses)
        else:
            base_response = self._get_varied_response('exploration', recent_responses)
        
        # Add varied contextual follow-up based on conversation history
        if message_count > 1:
            context_additions = [
                " Based on what you've shared, it sounds like these feelings are building up over time.",
                " I'm noticing a pattern in what you're telling me.",
                " This seems to connect with what you mentioned earlier.",
                " I can see how these experiences are affecting you.",
                " It sounds like this has been on your mind for a while."
            ]
            # Only add if this specific addition wasn't used recently
            available_additions = [add for add in context_additions if not any(add.strip() in recent_resp for recent_resp in recent_responses)]
            if available_additions:
                base_response += random.choice(available_additions)
        
        # Add therapeutic technique if appropriate
        if message_count > 1 and sentiment == 'negative' and random.random() < 0.4:  # Only 40% of the time
            technique_addition = self._add_therapeutic_technique(topic_category, recent_history)
            if technique_addition and not any(technique_addition in recent_resp for recent_resp in recent_responses):
                base_response += " " + technique_addition
        
        return base_response


    
    def _generate_therapeutic_response(self, nlp_result, session_context, response_type, sentiment, topic_category):
        """Core therapeutic response generation"""
        
        # Use reflection technique
        if response_type in ['empathy_support', 'mental_health_support'] and random.random() < 0.4:
            reflection = self._generate_reflection(nlp_result.get('original_text', ''))
            if reflection:
                template = random.choice(self.response_templates['reflection'])
                base_response = template.format(reflection=reflection)
            else:
                base_response = self._get_response(response_type)
        else:
            base_response = self._get_response(response_type)
        
        # Add validation for negative emotions
        if sentiment == 'negative' and random.random() < 0.5:
            validation = self._get_response('validation')
            base_response = validation + " " + base_response
        
        return base_response
    
    def _generate_reflection(self, user_text: str) -> Optional[str]:
        """Generate a therapeutic reflection of what the user said"""
        if not user_text:
            return None
            
        # Simple reflection generation (in a real app, this would be more sophisticated)
        user_lower = user_text.lower()
        
        if 'anxious' in user_lower or 'worried' in user_lower:
            return "you're experiencing anxiety and worry"
        elif 'sad' in user_lower or 'depressed' in user_lower:
            return "you're feeling sad and down"
        elif 'stressed' in user_lower:
            return "you're under a lot of stress right now"
        elif 'angry' in user_lower or 'frustrated' in user_lower:
            return "you're feeling angry and frustrated"
        elif 'lonely' in user_lower:
            return "you're feeling isolated and alone"
        elif 'work' in user_lower:
            return "work is creating challenges for you"
        elif 'relationship' in user_lower:
            return "you're having relationship difficulties"
        
        return None
    
    def _get_varied_response(self, response_type: str, recent_responses: List[str]) -> str:
        """Get a response while avoiding recent repetitions"""
        responses = self.response_templates.get(response_type, self.response_templates['exploration'])
        
        # Filter out recently used responses
        available_responses = [r for r in responses if not any(r in recent for recent in recent_responses)]
        
        # If all responses were used recently, use the full set
        if not available_responses:
            available_responses = responses
        
        return random.choice(available_responses)

    def _add_therapeutic_technique(self, topic_category: str, recent_history: List) -> Optional[str]:
        """Add a therapeutic technique based on conversation flow"""
        if not recent_history:
            return None
            
        # Check if we should introduce a technique
        if len(recent_history) >= 2:
            recent_sentiments = [ex['sentiment'] for ex in recent_history[-2:]]
            if recent_sentiments.count('negative') >= 1:
                
                # Choose technique based on topic
                if topic_category == 'mental_health':
                    return random.choice(self.therapeutic_techniques['mindfulness'])
                elif topic_category == 'work_stress':
                    return random.choice(self.therapeutic_techniques['cognitive_reframing'])
                else:
                    technique = random.choice(['cognitive_reframing', 'mindfulness'])
                    return random.choice(self.therapeutic_techniques[technique])
        
        return None
    
    def _suggest_coping_strategy(self, topic_category: str) -> Optional[str]:
        """Suggest a relevant coping strategy"""
        strategy_intro = "Here's something that might help: "
        
        if topic_category == 'mental_health':
            if 'anxiety' in topic_category.lower():
                strategy = random.choice(self.coping_strategies['anxiety'])
            elif 'depression' in topic_category.lower():
                strategy = random.choice(self.coping_strategies['depression'])
            else:
                strategy = random.choice(self.coping_strategies['general'])
        elif topic_category == 'work_stress':
            strategy = random.choice(self.coping_strategies['stress'])
        else:
            strategy = random.choice(self.coping_strategies['general'])
            
        return strategy_intro + strategy
    
    def _detect_crisis_language(self, text: str) -> bool:
        """Enhanced crisis detection"""
        crisis_phrases = [
            'want to die', 'kill myself', 'end it all', 'suicide', 'can\'t go on',
            'better off dead', 'no point in living', 'want to disappear',
            'hurt myself', 'end my life'
        ]
        
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in crisis_phrases)
    
    def _get_response(self, response_type: str) -> str:
        """Get a random response from the specified category"""
        responses = self.response_templates.get(response_type, self.response_templates['exploration'])
        return random.choice(responses)
    
    def generate_session_closing(self) -> str:
        """Generate a session closing response"""
        return self._get_response('session_closing')

    def _handle_direct_question(self, user_text: str, topic: str, recent_responses: List[str]) -> str:
        """Handle direct questions and requests for help"""
        
        if any(keyword in user_text for keyword in ['strategies', 'manage', 'cope', 'deal with']):
            if 'stress' in user_text or 'overthinking' in user_text:
                stress_strategies = [
                    "Here are some effective strategies for managing work stress: Try setting clear boundaries between work and personal time - perhaps designating specific hours when you won't check emails. What do you think about implementing a 'shutdown ritual' at the end of your workday?",
                    "For overthinking, I'd suggest trying the '5-4-3-2-1' grounding technique when your mind races: Notice 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. Also, consider keeping a 'worry journal' - write down your concerns for 10 minutes, then close it. How does that sound?",
                    "To break the cycle of overthinking, try time-blocking: set specific times for checking emails rather than constantly monitoring them. Also, practice 'thought stopping' - when you catch yourself replaying conversations, consciously redirect to something else. What feels most doable for you right now?"
                ]
                return random.choice([r for r in stress_strategies if r not in recent_responses] or stress_strategies)
        
        return "I hear you're looking for practical solutions. Let's work together to identify some strategies that might help your specific situation. What aspect feels most urgent to address first?"

    def _handle_burnout_stress(self, user_text: str, message_count: int, recent_responses: List[str]) -> str:
        """Handle burnout and stress-related content"""
        
        burnout_responses = [
            "What you're describing sounds like classic signs of burnout - the emotional exhaustion, feeling overwhelmed by small tasks, and the racing mind. It's important to recognize these patterns. Burnout is your mind and body telling you that something needs to change.",
            "The combination of physical and emotional exhaustion you're experiencing is a clear signal. When even small tasks feel overwhelming, it often means we've been operating in survival mode for too long. Your awareness of this is actually the first step toward healing.",
            "That inability to 'switch off' is so common with burnout - your nervous system is stuck in high alert mode. The fact that you're checking emails late and replaying conversations shows how your work stress has invaded your personal time and mental space."
        ]
        
        available_responses = [r for r in burnout_responses if r not in recent_responses] or burnout_responses
        return random.choice(available_responses)

    def _handle_work_stress(self, user_text: str, sentiment: str, recent_responses: List[str]) -> str:
        """Handle work-related stress and concerns"""
        
        if 'falling behind' in user_text or 'not doing enough' in user_text:
            responses = [
                "That fear of falling behind despite working long hours suggests you might be dealing with perfectionism or imposter syndrome. When we're in this mindset, no amount of work ever feels 'enough.' Have you noticed this pattern before?",
                "It's exhausting when you feel like you're constantly racing to catch up, even when you're putting in so much effort. This kind of persistent self-doubt can be more draining than the work itself. What would 'doing enough' actually look like to you?"
            ]
        elif 'lost interest' in user_text or 'dream career' in user_text:
            responses = [
                "Losing passion for what was once your dream career is heartbreaking and can feel like losing part of your identity. Sometimes this happens when we've been operating under chronic stress - it's hard to feel joy when you're in survival mode.",
                "When work becomes constant pressure instead of fulfillment, it's natural to question whether you've changed or if the environment has. Often, it's both - and recognizing this is important for figuring out your next steps."
            ]
        else:
            responses = [
                "Work stress has a way of infiltrating every part of our lives. It sounds like you're carrying the weight of your job even when you're not there physically.",
                "The pressure you're describing at work seems to be creating a cycle where you never feel like you can rest or be present in your non-work life."
            ]
        
        available_responses = [r for r in responses if r not in recent_responses] or responses
        return random.choice(available_responses)

    def _handle_emotional_distress(self, user_text: str, recent_responses: List[str]) -> str:
        """Handle emotional expressions and distress"""
        
        emotional_responses = [
            "I can hear the fear in your words about potentially losing something that meant so much to you. That uncertainty about whether you're changing or your environment is changing can feel destabilizing.",
            "The worry and second-guessing you're experiencing sound exhausting. When we're constantly questioning ourselves, it creates an additional layer of mental load on top of everything else.",
            "Fear about our career and identity can feel particularly intense because work is such a big part of how we see ourselves. Your concerns are completely understandable."
        ]
        
        available_responses = [r for r in emotional_responses if r not in recent_responses] or emotional_responses
        return random.choice(available_responses)
# Global advanced response generator
advanced_therapy_responder = AdvancedTherapyResponseGenerator()

def generate_advanced_therapy_response(nlp_result: Dict, session_context: Dict) -> str:
    """Generate contextual therapy response with session awareness"""
    return advanced_therapy_responder.generate_contextual_response(nlp_result, session_context)

def generate_hybrid_therapy_response(nlp_result: Dict, session_context: Dict) -> str:
        """Generate response using hybrid approach"""
        user_input = nlp_result.get('original_text', '')
        
        # Determine strategy: rule-based vs AI generation
        strategy = hybrid_generator.determine_response_strategy(user_input, nlp_result, session_context)
        
        logger.info(f"Using {strategy} strategy for: {user_input[:50]}...")
        
        if strategy == 'rule_based':
            # Use your existing advanced template system for simple cases
            return advanced_therapy_responder.generate_contextual_response(nlp_result, session_context)
        else:
            # Use AI generation for complex cases
            return hybrid_generator.generate_with_transformer(user_input, nlp_result, session_context)