"""
Interactive demonstration script for exploring AI agent concepts.
Run this script to see agents in action and experiment with different scenarios.
"""

from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path so we can import our agents
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_agents import ProductivityAgent, SimpleWeatherAgent, ReactiveSpamFilter, DeliberativePersonalAssistant


def demonstrate_weather_agent():
    """Interactive demonstration of the simple weather agent"""
    print("🌤️  Weather Agent Demonstration")
    print("-" * 40)
    
    agent = SimpleWeatherAgent()
    
    # Different weather scenarios
    scenarios = [
        {'temperature': 75, 'condition': 'sunny'},
        {'temperature': 35, 'condition': 'snow'},
        {'temperature': 60, 'condition': 'rain'},
        {'temperature': 85, 'condition': 'sunny'}
    ]
    
    for i, weather_data in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {weather_data['condition']}, {weather_data['temperature']}°F")
        result = agent.run_agent_cycle(weather_data)
        print(f"Recommendations: {', '.join(result['recommended'])}")


def demonstrate_productivity_agent():
    """Interactive demonstration of the productivity agent"""
    print("\n📋 Productivity Agent Demonstration")
    print("-" * 40)
    
    agent = ProductivityAgent()
    
    print("Adding tasks throughout the day...")
    
    # Morning tasks
    print("\n🌅 Morning: Adding initial tasks")
    agent.add_task("Review quarterly budget report", "high", datetime.now() + timedelta(days=1))
    agent.add_task("Send email to project team", "medium")
    agent.add_task("Prepare presentation slides", "high", datetime.now() + timedelta(hours=4))
    agent.add_task("Plan weekend hiking trip", "low")
    
    # Get initial recommendation
    print("\n" + agent.get_next_task_recommendation())
    
    # Midday progress
    print("\n🕐 Midday: Making progress")
    agent.complete_task("Send email to project team")
    agent.complete_task("Review quarterly budget report")
    
    print("\n" + agent.get_next_task_recommendation())
    
    # Add urgent task
    print("\n🚨 Afternoon: Urgent task added")
    agent.add_task("Fix critical bug in production", "high", datetime.now() + timedelta(hours=1))
    
    print("\n" + agent.get_next_task_recommendation())
    
    # End of day
    print("\n🌅 End of day summary")
    agent.daily_summary()
    
    # Show statistics
    print(agent.get_task_statistics())


def demonstrate_agent_types():
    """Compare reactive vs deliberative agents"""
    print("\n🤖 Agent Types Comparison")
    print("-" * 40)
    
    # Reactive Agent Example
    print("\n📧 Reactive Agent: Spam Filter")
    spam_filter = ReactiveSpamFilter()
    
    test_emails = [
        {
            'sender': 'boss@company.com',
            'content': 'Please review the quarterly report when you have time.'
        },
        {
            'sender': 'unknown@suspicious.com',
            'content': 'URGENT! You are a WINNER! Click now for FREE MONEY and limited time offers!'
        },
        {
            'sender': 'newsletter@tech.com',
            'content': 'This week in technology: new AI breakthroughs and startup news.'
        }
    ]
    
    for i, email in enumerate(test_emails, 1):
        result = spam_filter.classify_email(email)
        print(f"Email {i}: {result}")
        print(f"  From: {email['sender']}")
        print(f"  Content: {email['content'][:50]}...")
    
    # Deliberative Agent Example
    print("\n🤔 Deliberative Agent: Personal Assistant")
    assistant = DeliberativePersonalAssistant()
    
    requests = [
        "Book a restaurant for dinner tonight",
        "Schedule a team meeting for next week",
        "Help me plan a vacation to Japan"
    ]
    
    for request in requests:
        print(f"\nRequest: '{request}'")
        actions = assistant.process_request(request)
        print(f"Planned actions: {actions}")


def interactive_productivity_session():
    """Let users interact with the productivity agent"""
    print("\n🎮 Interactive Productivity Agent")
    print("-" * 40)
    print("Type 'help' for commands, 'quit' to exit")
    
    agent = ProductivityAgent()
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'help':
                print("""
Available commands:
- add [task description] [priority] : Add a new task (priority: high/medium/low)
- complete [task description]      : Mark a task as completed
- recommend                        : Get next task recommendation
- summary                          : View daily summary
- stats                           : View task statistics
- quit                            : Exit
                """)
            elif user_input.lower().startswith('add '):
                parts = user_input[4:].split()
                if len(parts) >= 1:
                    if len(parts) > 1 and parts[-1] in ['high', 'medium', 'low']:
                        priority = parts[-1]
                        description = ' '.join(parts[:-1])
                    else:
                        priority = 'medium'
                        description = ' '.join(parts)
                    
                    agent.add_task(description, priority)
                else:
                    print("Please provide a task description")
            
            elif user_input.lower().startswith('complete '):
                task_description = user_input[9:]
                agent.complete_task(task_description)
            
            elif user_input.lower() == 'recommend':
                print(agent.get_next_task_recommendation())
            
            elif user_input.lower() == 'summary':
                agent.daily_summary()
            
            elif user_input.lower() == 'stats':
                print(agent.get_task_statistics())
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main demonstration program"""
    print("🚀 AI Agents Chapter 1 - Interactive Demonstrations")
    print("=" * 60)
    
    while True:
        print("""
Choose a demonstration:

1. Weather Agent - See basic agent perception and action
2. Productivity Agent - Experience a complete AI assistant
3. Agent Types - Compare reactive vs deliberative agents
4. Interactive Session - Control the productivity agent yourself
5. Exit

        """)
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                demonstrate_weather_agent()
            elif choice == '2':
                demonstrate_productivity_agent()
            elif choice == '3':
                demonstrate_agent_types()
            elif choice == '4':
                interactive_productivity_session()
            elif choice == '5':
                print("Thanks for exploring AI agents! 🤖")
                break
            else:
                print("Please enter a number between 1 and 5.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()