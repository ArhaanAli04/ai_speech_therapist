import requests
import json
import time

class AITherapistTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session_id = None
    
    def test_complete_workflow(self):
        """Test the complete AI therapist workflow"""
        print("🧪 Testing Complete AI Therapist System")
        print("=" * 50)
        
        # Test 1: Start Session
        print("\n1. Testing Session Creation...")
        if self.test_start_session():
            print("✅ Session creation: PASSED")
        else:
            print("❌ Session creation: FAILED")
            return False
        
        # Test 2: Text-based conversation
        print("\n2. Testing Text Conversation...")
        conversation_tests = [
            "I have been feeling very anxious about work lately",
            "It keeps me up at night and I feel overwhelmed",
            "I worry that I am falling behind my colleagues"
        ]
        
        for i, message in enumerate(conversation_tests, 1):
            print(f"   Message {i}: {message}")
            response = self.test_text_message(message)
            if response:
                ai_response_text = response.get('ai_response', 'No response text')
                print(f"   ✅ AI Response: {ai_response_text[:100]}...")
                print(f"   📊 Message Count: {response.get('message_count', 'Unknown')}")
            else:
                print(f"   ❌ Failed to get response")
        
        # Test 3: Session Summary
        print("\n3. Testing Session Summary...")
        summary = self.test_session_summary()
        if summary:
            print("✅ Session summary generated successfully")
            print(f"   📈 Total exchanges: {summary.get('total_exchanges', 0)}")
            print(f"   🎯 Main topics: {summary.get('main_topics', [])}")
            print(f"   💭 Dominant sentiment: {summary.get('dominant_sentiment', 'unknown')}")
        else:
            print("❌ Session summary failed")
        
        # Test 4: End Session
        print("\n4. Testing Session Termination...")
        if self.test_end_session():
            print("✅ Session termination: PASSED")
        else:
            print("❌ Session termination: FAILED")
        
        print("\n🎉 Complete System Test Finished!")
        return True
    
    def test_start_session(self):
        try:
            response = requests.post(f"{self.base_url}/start-therapy-session")
            data = response.json()
            if data.get('success'):
                self.session_id = data.get('session_id')
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def test_text_message(self, message):
        try:
            response = requests.post(
                f"{self.base_url}/text-therapy",
                json={"text": message, "session_id": self.session_id}
            )
            data = response.json()
            if data.get('success'):
                return data
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def test_session_summary(self):
        try:
            response = requests.get(f"{self.base_url}/session-summary/{self.session_id}")
            data = response.json()
            if data.get('success'):
                return data.get('session_summary')
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def test_end_session(self):
        try:
            response = requests.get(f"{self.base_url}/end-session/{self.session_id}")
            data = response.json()
            return data.get('success', False)
        except Exception as e:
            print(f"Error: {e}")
            return False

if __name__ == "__main__":
    tester = AITherapistTester()
    tester.test_complete_workflow()
