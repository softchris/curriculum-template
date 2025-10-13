"""
Quick demonstration of Python agent development concepts.
Run this file to see the key patterns in action.
"""

import asyncio
from datetime import datetime
from src.python_agents import CompositeAgent, AgentConfig, TaskAgent
from src.pydantic_models import TaskModel, Priority


def demonstrate_decorators():
    """Show decorator functionality."""
    print("🎭 Decorator Demo")
    print("-" * 30)
    
    config = AgentConfig(name="DecoratorDemo")
    agent = TaskAgent(config)
    
    # These operations will show logging, validation, and performance measurement
    agent.activate()
    agent.add_task("Demo task", "high")
    
    print(f"📊 Task summary: {agent.get_task_summary()}")
    agent.deactivate()


def demonstrate_pydantic():
    """Show Pydantic validation."""
    print("\n🔍 Pydantic Validation Demo")
    print("-" * 35)
    
    # Valid task creation
    try:
        task = TaskModel(
            title="Review budget report",
            description="Analyze Q4 budget and prepare recommendations",
            priority=Priority.HIGH,
            estimated_duration_minutes=120
        )
        print(f"✅ Created valid task: {task.title}")
        print(f"   Due date: {task.due_date}")
        print(f"   Is overdue: {task.is_overdue()}")
        
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
    
    # Invalid task (will show validation error)
    try:
        invalid_task = TaskModel(
            title="",  # Empty title should fail
            description="Test task",
            priority="invalid_priority"  # Invalid priority
        )
        print(f"⚠️  This shouldn't print - validation should have failed!")
        
    except Exception as e:
        print(f"✅ Validation correctly caught error: {e}")


async def demonstrate_async_agents():
    """Show async agent capabilities."""
    print("\n🚀 Async Agent Demo")
    print("-" * 25)
    
    # Create composite agent
    config = AgentConfig(
        name="DemoAgent",
        max_concurrent_tasks=3,
        enabled_capabilities=["task_management", "weather_monitoring"]
    )
    
    agent = CompositeAgent(config)
    agent.activate()
    
    try:
        # Add tasks
        print("📝 Adding tasks...")
        await agent.process_message("add task Review project proposal")
        await agent.process_message("add task Send client email")
        await agent.process_message("add task Update documentation")
        
        # Process tasks concurrently
        print("\n🔄 Processing tasks...")
        await agent.process_message("process tasks")
        
        # Check weather
        print("\n🌤️ Checking weather...")
        await agent.process_message("update weather")
        
        # Get final status
        print("\n📊 Final status:")
        await agent.process_message("status")
        
    finally:
        agent.deactivate()


def main():
    """Run all demonstrations."""
    print("🤖 Python Agent Development Demo")
    print("Chapter 2: Professional Python Patterns")
    print("=" * 50)
    
    # Run synchronous demos
    demonstrate_decorators()
    demonstrate_pydantic()
    
    # Run async demo
    print("\n" + "=" * 50)
    asyncio.run(demonstrate_async_agents())
    
    print("\n✅ Demo completed!")
    print("\nNext steps:")
    print("- Explore src/python_agents.py for complete implementations")
    print("- Check src/pydantic_models.py for data validation examples")
    print("- Run tests with: python -m pytest tests/ -v")


if __name__ == "__main__":
    main()