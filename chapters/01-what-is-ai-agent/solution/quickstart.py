#!/usr/bin/env python3
"""
Quick start script for Chapter 1: What Is an AI Agent?

This script provides an easy way to explore the key concepts from the chapter
by running different AI agent examples.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai_agents import ProductivityAgent, SimpleWeatherAgent
from datetime import datetime, timedelta


def quick_productivity_demo():
    """Quick demonstration of the productivity agent"""
    print("🚀 Quick Productivity Agent Demo")
    print("=" * 40)
    
    # Create agent
    agent = ProductivityAgent()
    
    # Add some sample tasks
    print("\n📝 Adding sample tasks...")
    agent.add_task("Review project proposal", "high", datetime.now() + timedelta(hours=2))
    agent.add_task("Send status update email", "medium")
    agent.add_task("Book restaurant for weekend", "low")
    
    # Get recommendation
    print("\n🎯 Getting task recommendation...")
    print(agent.get_next_task_recommendation())
    
    # Complete a task
    print("\n✅ Completing a task...")
    agent.complete_task("Send status update email")
    
    # Show daily summary
    print("\n📊 Daily summary:")
    agent.daily_summary()


def quick_weather_demo():
    """Quick demonstration of the weather agent"""
    print("\n🌤️ Quick Weather Agent Demo")
    print("=" * 40)
    
    # Create agent
    agent = SimpleWeatherAgent()
    
    # Test different weather conditions
    weather_scenarios = [
        {'temperature': 35, 'condition': 'snow'},
        {'temperature': 85, 'condition': 'sunny'},
        {'temperature': 60, 'condition': 'rain'}
    ]
    
    for weather in weather_scenarios:
        print(f"\n🌡️ Weather: {weather['condition']}, {weather['temperature']}°F")
        result = agent.run_agent_cycle(weather)
        print(f"Recommendations: {', '.join(result['recommended'])}")


if __name__ == "__main__":
    print("🤖 Chapter 1: AI Agent Quick Start")
    print("=" * 50)
    print("This script demonstrates the core concepts from Chapter 1")
    print("Learn about the four pillars of AI agents in action!\n")
    
    try:
        # Run productivity demo
        quick_productivity_demo()
        
        # Run weather demo
        quick_weather_demo()
        
        print("\n🎉 Demo complete!")
        print("\nNext steps:")
        print("• Run 'python demo.py' for interactive demonstrations")
        print("• Run 'python -m pytest tests/' to see all tests pass")
        print("• Explore the source code in src/ai_agents.py")
        print("• Read the README.md for detailed explanations")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this script from the solution directory")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check the installation and try again")