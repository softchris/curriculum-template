from datetime import datetime, timedelta
import json

class ProductivityAgent:
    """
    A complete AI agent that demonstrates all four pillars of agent architecture:
    1. Perception - gathering task information from user input
    2. Knowledge - maintaining task database and user preferences
    3. Decision-making - prioritizing tasks and analyzing workload
    4. Action - providing recommendations and organizing tasks
    """
    
    def __init__(self):
        # Agent's knowledge base
        self.tasks = []
        self.priorities = {'high': 3, 'medium': 2, 'low': 1}
        self.user_preferences = {
            'work_hours_start': 9,
            'work_hours_end': 17,
            'break_interval': 2  # hours between breaks
        }
        self.last_break_suggestion = None
    
    def perceive_task_input(self, task_description, priority='medium', deadline=None):
        """
        Pillar 1: Perception - gather information about new tasks
        
        This method demonstrates how agents perceive and interpret their environment.
        It doesn't just store raw data, but enriches it with intelligent analysis.
        """
        task_data = {
            'description': task_description,
            'priority': priority,
            'deadline': deadline,
            'created_at': datetime.now(),
            'completed': False,
            'estimated_duration': self.estimate_duration(task_description)
        }
        
        print(f"📝 Perceived new task: {task_description}")
        return task_data
    
    def estimate_duration(self, description):
        """
        Use simple heuristics to estimate task duration.
        This shows how agents can derive additional insights from basic input.
        """
        word_count = len(description.split())
        description_lower = description.lower()
        
        if 'meeting' in description_lower:
            return 60  # 1 hour for meetings
        elif 'email' in description_lower:
            return 15  # 15 minutes for emails
        elif 'call' in description_lower:
            return 30  # 30 minutes for calls
        elif word_count > 10:
            return 120  # 2 hours for complex tasks
        else:
            return 30  # 30 minutes for simple tasks
    
    def add_task(self, task_description, priority='medium', deadline=None):
        """
        Complete agent cycle for adding a task.
        This demonstrates how all four pillars work together in one operation.
        """
        # Pillar 1: Perception
        task_data = self.perceive_task_input(task_description, priority, deadline)
        
        # Pillar 2 & 3: Knowledge and Decision-making
        self.tasks.append(task_data)
        
        # Pillar 4: Action - provide intelligent feedback
        feedback = self.analyze_workload()
        print(f"✅ Task added: {task_description}")
        print(f"💡 {feedback}")
        
        return task_data
    
    def analyze_workload(self):
        """
        Pillar 2 & 3: Use knowledge to make decisions about workload
        
        This method shows how agents combine stored knowledge with current
        state to provide intelligent insights.
        """
        incomplete_tasks = [t for t in self.tasks if not t['completed']]
        high_priority_count = len([t for t in incomplete_tasks if t['priority'] == 'high'])
        total_estimated_time = sum(t['estimated_duration'] for t in incomplete_tasks)
        
        # Decision-making based on workload analysis
        if high_priority_count > 3:
            return "You have many high-priority tasks. Consider focusing on the most urgent ones first."
        elif total_estimated_time > 480:  # More than 8 hours
            return "Your task list is quite full. You might want to postpone some lower-priority items."
        else:
            return "Your workload looks manageable. Great job staying organized!"
    
    def get_next_task_recommendation(self):
        """
        Pillar 3: Decision-making for task prioritization
        
        This demonstrates sophisticated reasoning: considering multiple factors
        and combining them to make optimal recommendations.
        """
        incomplete_tasks = [t for t in self.tasks if not t['completed']]
        
        if not incomplete_tasks:
            return "🎉 All tasks completed! Time to relax or add new goals."
        
        # Sort by priority and deadline using intelligent scoring
        def task_score(task):
            priority_score = self.priorities[task['priority']]
            deadline_score = 0
            
            if task['deadline']:
                days_until_deadline = (task['deadline'] - datetime.now()).days
                deadline_score = max(0, 10 - days_until_deadline)  # More urgent = higher score
            
            return priority_score + deadline_score
        
        recommended_task = max(incomplete_tasks, key=task_score)
        
        return f"🎯 Recommended next task: {recommended_task['description']} (Priority: {recommended_task['priority']})"
    
    def complete_task(self, task_description):
        """
        Pillar 4: Action - mark tasks as completed
        
        This shows how agents take action in their environment and provide
        encouraging feedback to support user goals.
        """
        for task in self.tasks:
            if task['description'].lower() == task_description.lower() and not task['completed']:
                task['completed'] = True
                task['completed_at'] = datetime.now()
                
                # Celebrate completion and provide encouragement
                print(f"🎉 Task completed: {task_description}")
                
                remaining_tasks = len([t for t in self.tasks if not t['completed']])
                if remaining_tasks > 0:
                    print(f"💪 {remaining_tasks} tasks remaining. You're making great progress!")
                else:
                    print("🌟 All tasks completed! Excellent work!")
                
                return True
        
        print(f"❓ Task not found: {task_description}")
        return False
    
    def daily_summary(self):
        """
        Pillar 4: Action - provide daily insights
        
        This demonstrates how agents can analyze patterns and provide
        valuable summaries without being explicitly programmed for every scenario.
        """
        completed_today = [t for t in self.tasks 
                          if t['completed'] and t.get('completed_at', datetime.min).date() == datetime.now().date()]
        
        pending_tasks = [t for t in self.tasks if not t['completed']]
        
        print("\n📊 Daily Summary:")
        print(f"✅ Completed today: {len(completed_today)} tasks")
        print(f"⏳ Still pending: {len(pending_tasks)} tasks")
        
        if completed_today:
            print("🎯 Completed tasks:")
            for task in completed_today:
                print(f"   • {task['description']}")
        
        if pending_tasks:
            next_recommendation = self.get_next_task_recommendation()
            print(f"\n{next_recommendation}")
    
    def get_task_statistics(self):
        """
        Additional utility method to demonstrate agent's analytical capabilities
        """
        if not self.tasks:
            return "No tasks have been added yet."
        
        completed_tasks = [t for t in self.tasks if t['completed']]
        completion_rate = len(completed_tasks) / len(self.tasks) * 100
        
        avg_completion_time = 0
        if completed_tasks:
            completion_times = []
            for task in completed_tasks:
                if 'completed_at' in task:
                    time_diff = task['completed_at'] - task['created_at']
                    completion_times.append(time_diff.total_seconds() / 3600)  # Convert to hours
            
            if completion_times:
                avg_completion_time = sum(completion_times) / len(completion_times)
        
        return f"""
📈 Task Statistics:
• Total tasks: {len(self.tasks)}
• Completed: {len(completed_tasks)}
• Completion rate: {completion_rate:.1f}%
• Average completion time: {avg_completion_time:.1f} hours
        """


# Simple demonstration agents for learning
class SimpleWeatherAgent:
    """A basic example showing the core agent structure"""
    
    def __init__(self):
        self.current_temperature = None
        self.weather_condition = None
        self.weather_knowledge = {
            'rain': ['bring_umbrella', 'wear_raincoat', 'avoid_outdoor_activities'],
            'sunny': ['wear_sunscreen', 'bring_water', 'good_for_outdoor_activities'],
            'snow': ['dress_warmly', 'drive_carefully', 'check_for_ice']
        }
    
    def perceive_environment(self, sensor_data):
        """Pillar 1: Perception"""
        self.current_temperature = sensor_data.get('temperature')
        self.weather_condition = sensor_data.get('condition')
        print(f"Perceived: {self.current_temperature}°F, {self.weather_condition}")
    
    def assess_comfort_level(self):
        """Pillar 2: Knowledge application"""
        if self.current_temperature < 50:
            return 'cold'
        elif self.current_temperature > 80:
            return 'hot'
        else:
            return 'comfortable'
    
    def make_decision(self):
        """Pillar 3: Decision-making"""
        comfort_level = self.assess_comfort_level()
        weather_actions = self.weather_knowledge.get(self.weather_condition, [])
        
        recommendations = []
        
        # Temperature-based recommendations
        if comfort_level == 'cold':
            recommendations.append('dress_warmly')
        elif comfort_level == 'hot':
            recommendations.append('stay_hydrated')
        
        # Weather-based recommendations
        recommendations.extend(weather_actions)
        
        return list(set(recommendations))  # Remove duplicates
    
    def take_action(self, recommendations):
        """Pillar 4: Action"""
        actions_taken = []
        
        for recommendation in recommendations:
            if recommendation == 'bring_umbrella':
                self.send_notification("Don't forget your umbrella!")
                actions_taken.append('umbrella_notification_sent')
            elif recommendation == 'dress_warmly':
                self.send_notification("Bundle up! It's cold outside.")
                actions_taken.append('cold_weather_alert_sent')
            elif recommendation == 'good_for_outdoor_activities':
                self.suggest_activities(['hiking', 'picnic', 'outdoor_sports'])
                actions_taken.append('outdoor_activities_suggested')
        
        return actions_taken
    
    def send_notification(self, message):
        """Simulate sending a notification to the user"""
        print(f"📱 Notification: {message}")
    
    def suggest_activities(self, activities):
        """Simulate suggesting activities to the user"""
        print(f"💡 Suggested activities: {', '.join(activities)}")
    
    def run_agent_cycle(self, sensor_data):
        """Complete agent cycle: perceive, decide, act"""
        # 1. Perception
        self.perceive_environment(sensor_data)
        
        # 2. Decision-making (using knowledge)
        recommendations = self.make_decision()
        
        # 3. Action
        actions_taken = self.take_action(recommendations)
        
        return {
            'perceived': f"{self.current_temperature}°F, {self.weather_condition}",
            'recommended': recommendations,
            'actions': actions_taken
        }


class ReactiveSpamFilter:
    """Example of a reactive agent - responds immediately to input"""
    
    def __init__(self):
        self.spam_keywords = ['urgent', 'winner', 'click now', 'limited time', 'free money']
        self.trusted_senders = ['family@email.com', 'work@company.com']
    
    def classify_email(self, email):
        """React immediately to incoming email without memory or planning"""
        # Check sender trust level
        if email['sender'] in self.trusted_senders:
            return 'trusted'
        
        # Check for spam indicators
        spam_score = 0
        for keyword in self.spam_keywords:
            if keyword.lower() in email['content'].lower():
                spam_score += 1
        
        # Immediate decision based on current email only
        return 'spam' if spam_score > 2 else 'legitimate'


class DeliberativePersonalAssistant:
    """Example of a deliberative agent - plans and remembers"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.task_queue = []
        self.available_actions = ['search_web', 'send_email', 'schedule_event', 'set_reminder']
    
    def process_request(self, user_input):
        """Plan and execute multi-step responses"""
        # Remember this interaction
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_input': user_input
        })
        
        # Analyze the request and create a plan
        plan = self.create_plan(user_input)
        
        # Execute the plan
        results = []
        for action in plan:
            result = self.execute_action(action)
            results.append(result)
        
        return results
    
    def create_plan(self, request):
        """Plan sequence of actions to fulfill request"""
        plan = []
        request_lower = request.lower()
        
        if "restaurant" in request_lower and "book" in request_lower:
            plan = [
                {'action': 'search_web', 'query': 'restaurants near me'},
                {'action': 'schedule_event', 'title': 'Dinner reservation'},
                {'action': 'set_reminder', 'message': 'Confirm restaurant booking'}
            ]
        elif "meeting" in request_lower:
            plan = [
                {'action': 'schedule_event', 'title': 'Meeting'},
                {'action': 'send_email', 'purpose': 'meeting_invitation'}
            ]
        
        return plan
    
    def execute_action(self, action):
        """Simulate executing planned actions"""
        action_type = action['action']
        
        if action_type == 'search_web':
            return f"Searched for: {action.get('query', 'general search')}"
        elif action_type == 'schedule_event':
            return f"Event scheduled: {action.get('title', 'New event')}"
        elif action_type == 'send_email':
            return f"Email sent: {action.get('purpose', 'general email')}"
        elif action_type == 'set_reminder':
            return f"Reminder set: {action.get('message', 'general reminder')}"
        
        return f"Executed: {action_type}"


if __name__ == "__main__":
    print("🤖 AI Agent Examples - Chapter 1")
    print("=" * 50)
    
    # Example 1: Simple Weather Agent
    print("\n1. Simple Weather Agent Example:")
    weather_agent = SimpleWeatherAgent()
    weather_data = {'temperature': 45, 'condition': 'rain'}
    result = weather_agent.run_agent_cycle(weather_data)
    print(f"Result: {result}")
    
    # Example 2: Productivity Agent
    print("\n2. Productivity Agent Example:")
    productivity_agent = ProductivityAgent()
    
    # Add some tasks
    productivity_agent.add_task("Review quarterly budget report", "high", datetime.now() + timedelta(days=1))
    productivity_agent.add_task("Send email to project team", "medium")
    productivity_agent.add_task("Plan weekend hiking trip", "low")
    
    # Get recommendation
    print("\n" + productivity_agent.get_next_task_recommendation())
    
    # Complete a task
    print("\n--- Completing a task ---")
    productivity_agent.complete_task("Send email to project team")
    
    # Daily summary
    productivity_agent.daily_summary()
    
    # Example 3: Agent Types Comparison
    print("\n3. Agent Types Comparison:")
    
    # Reactive agent
    spam_filter = ReactiveSpamFilter()
    test_email = {
        'sender': 'unknown@spam.com',
        'content': 'Urgent! You are a winner! Click now for free money!'
    }
    spam_result = spam_filter.classify_email(test_email)
    print(f"Spam filter result: {spam_result}")
    
    # Deliberative agent
    assistant = DeliberativePersonalAssistant()
    assistant_result = assistant.process_request("Book a restaurant for dinner tonight")
    print(f"Assistant planned actions: {assistant_result}")