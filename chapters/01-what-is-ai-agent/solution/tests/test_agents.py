import unittest
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_agents import ProductivityAgent, SimpleWeatherAgent, ReactiveSpamFilter, DeliberativePersonalAssistant


class TestProductivityAgent(unittest.TestCase):
    """Test cases for the productivity agent"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.agent = ProductivityAgent()
    
    def test_task_creation(self):
        """Test that tasks are created correctly"""
        task = self.agent.add_task("Test task", "high")
        
        self.assertEqual(task['description'], "Test task")
        self.assertEqual(task['priority'], "high")
        self.assertFalse(task['completed'])
        self.assertIsNotNone(task['created_at'])
        self.assertIsNotNone(task['estimated_duration'])
    
    def test_duration_estimation(self):
        """Test that duration estimation works correctly"""
        # Test meeting estimation
        meeting_duration = self.agent.estimate_duration("Team meeting with stakeholders")
        self.assertEqual(meeting_duration, 60)
        
        # Test email estimation
        email_duration = self.agent.estimate_duration("Send email to client")
        self.assertEqual(email_duration, 15)
        
        # Test complex task estimation
        complex_duration = self.agent.estimate_duration("Analyze quarterly financial reports and prepare comprehensive presentation")
        self.assertEqual(complex_duration, 120)
    
    def test_task_completion(self):
        """Test task completion functionality"""
        self.agent.add_task("Complete this task", "medium")
        
        # Test successful completion
        result = self.agent.complete_task("Complete this task")
        self.assertTrue(result)
        
        # Verify task is marked as completed
        completed_task = next(t for t in self.agent.tasks if t['description'] == "Complete this task")
        self.assertTrue(completed_task['completed'])
        self.assertIsNotNone(completed_task['completed_at'])
        
        # Test completing non-existent task
        result = self.agent.complete_task("Non-existent task")
        self.assertFalse(result)
    
    def test_workload_analysis(self):
        """Test workload analysis and recommendations"""
        # Add multiple high-priority tasks
        for i in range(5):
            self.agent.add_task(f"High priority task {i}", "high")
        
        feedback = self.agent.analyze_workload()
        self.assertIn("high-priority tasks", feedback)
        
        # Test with manageable workload
        agent2 = ProductivityAgent()
        agent2.add_task("Simple task", "low")
        feedback2 = agent2.analyze_workload()
        self.assertIn("manageable", feedback2)
    
    def test_task_recommendation(self):
        """Test task recommendation logic"""
        # Test with no tasks
        recommendation = self.agent.get_next_task_recommendation()
        self.assertIn("All tasks completed", recommendation)
        
        # Add tasks with different priorities and deadlines
        self.agent.add_task("Low priority task", "low")
        self.agent.add_task("High priority task", "high")
        self.agent.add_task("Urgent task", "medium", datetime.now() + timedelta(hours=1))
        
        recommendation = self.agent.get_next_task_recommendation()
        # Should recommend either high priority or urgent task
        self.assertTrue("High priority task" in recommendation or "Urgent task" in recommendation)


class TestSimpleWeatherAgent(unittest.TestCase):
    """Test cases for the simple weather agent"""
    
    def setUp(self):
        self.agent = SimpleWeatherAgent()
    
    def test_perception(self):
        """Test weather perception"""
        weather_data = {'temperature': 65, 'condition': 'sunny'}
        self.agent.perceive_environment(weather_data)
        
        self.assertEqual(self.agent.current_temperature, 65)
        self.assertEqual(self.agent.weather_condition, 'sunny')
    
    def test_comfort_assessment(self):
        """Test comfort level assessment"""
        self.agent.current_temperature = 45
        self.assertEqual(self.agent.assess_comfort_level(), 'cold')
        
        self.agent.current_temperature = 85
        self.assertEqual(self.agent.assess_comfort_level(), 'hot')
        
        self.agent.current_temperature = 70
        self.assertEqual(self.agent.assess_comfort_level(), 'comfortable')
    
    def test_decision_making(self):
        """Test weather-based decision making"""
        self.agent.current_temperature = 45
        self.agent.weather_condition = 'rain'
        
        recommendations = self.agent.make_decision()
        
        self.assertIn('dress_warmly', recommendations)
        self.assertIn('bring_umbrella', recommendations)
        self.assertIn('wear_raincoat', recommendations)
    
    def test_complete_cycle(self):
        """Test complete agent cycle"""
        weather_data = {'temperature': 75, 'condition': 'sunny'}
        result = self.agent.run_agent_cycle(weather_data)
        
        self.assertIn('perceived', result)
        self.assertIn('recommended', result)
        self.assertIn('actions', result)
        
        self.assertIn('good_for_outdoor_activities', result['recommended'])


class TestReactiveSpamFilter(unittest.TestCase):
    """Test cases for the reactive spam filter"""
    
    def setUp(self):
        self.filter = ReactiveSpamFilter()
    
    def test_trusted_sender(self):
        """Test trusted sender classification"""
        email = {
            'sender': 'family@email.com',
            'content': 'Hi there! How are you doing?'
        }
        
        result = self.filter.classify_email(email)
        self.assertEqual(result, 'trusted')
    
    def test_spam_detection(self):
        """Test spam detection"""
        spam_email = {
            'sender': 'unknown@spam.com',
            'content': 'Urgent! You are a winner! Click now for free money and limited time offers!'
        }
        
        result = self.filter.classify_email(spam_email)
        self.assertEqual(result, 'spam')
    
    def test_legitimate_email(self):
        """Test legitimate email classification"""
        legitimate_email = {
            'sender': 'newsletter@tech.com',
            'content': 'This week in technology: new developments in AI and machine learning.'
        }
        
        result = self.filter.classify_email(legitimate_email)
        self.assertEqual(result, 'legitimate')


class TestDeliberativePersonalAssistant(unittest.TestCase):
    """Test cases for the deliberative personal assistant"""
    
    def setUp(self):
        self.assistant = DeliberativePersonalAssistant()
    
    def test_conversation_memory(self):
        """Test that assistant remembers conversations"""
        request = "Book a restaurant for tonight"
        self.assistant.process_request(request)
        
        self.assertEqual(len(self.assistant.conversation_history), 1)
        self.assertEqual(self.assistant.conversation_history[0]['user_input'], request)
    
    def test_restaurant_planning(self):
        """Test restaurant booking plan creation"""
        plan = self.assistant.create_plan("Book a restaurant for dinner")
        
        self.assertEqual(len(plan), 3)
        self.assertEqual(plan[0]['action'], 'search_web')
        self.assertEqual(plan[1]['action'], 'schedule_event')
        self.assertEqual(plan[2]['action'], 'set_reminder')
    
    def test_meeting_planning(self):
        """Test meeting planning"""
        plan = self.assistant.create_plan("Schedule a team meeting")
        
        self.assertEqual(len(plan), 2)
        self.assertEqual(plan[0]['action'], 'schedule_event')
        self.assertEqual(plan[1]['action'], 'send_email')
    
    def test_action_execution(self):
        """Test action execution"""
        action = {'action': 'search_web', 'query': 'restaurants'}
        result = self.assistant.execute_action(action)
        
        self.assertIn('Searched for: restaurants', result)


if __name__ == '__main__':
    print("🧪 Running tests for AI Agents...")
    print("=" * 50)
    
    # Run all tests
    unittest.main(verbosity=2)