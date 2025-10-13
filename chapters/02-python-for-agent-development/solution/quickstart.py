"""
Quick start guide for Python agent development.
Simple examples to get you started with the concepts.
"""

import asyncio
from datetime import datetime, timedelta
from src.python_agents import BaseAgent, TaskAgent, AgentConfig
from src.pydantic_models import TaskModel, Priority


def basic_agent_example():
    """Create and use a basic agent."""
    print("🤖 Basic Agent Example")
    print("-" * 25)
    
    # Step 1: Create configuration
    config = AgentConfig(
        name="MyFirstAgent",
        max_concurrent_tasks=3,
        enabled_capabilities=["basic_operations"]
    )
    
    # Step 2: Create agent
    agent = BaseAgent(config)
    
    # Step 3: Activate agent
    agent.activate()
    
    # Step 4: Check status
    status = agent.get_status()
    print(f"Agent '{status['name']}' is active: {status['is_active']}")
    print(f"Uptime: {status['uptime_seconds']:.1f} seconds")
    
    # Step 5: Deactivate when done
    agent.deactivate()


def task_agent_example():
    """Use a task management agent."""
    print("\n📝 Task Agent Example")
    print("-" * 25)
    
    # Create task agent
    config = AgentConfig(name="TaskBot")
    agent = TaskAgent(config)
    agent.activate()
    
    # Add some tasks
    task1 = agent.add_task("Write project documentation", "high")
    task2 = agent.add_task("Review code changes", "medium")
    task3 = agent.add_task("Update README file", "low")
    
    # Get task summary
    summary = agent.get_task_summary()
    print(f"\nTask Summary:")
    print(f"  Total tasks: {summary['total_tasks']}")
    print(f"  Pending: {summary['pending']}")
    print(f"  Completed: {summary['completed']}")
    
    agent.deactivate()


async def async_task_processing():
    """Process tasks asynchronously."""
    print("\n⚡ Async Task Processing")
    print("-" * 30)
    
    # Create agent
    config = AgentConfig(name="AsyncBot", max_concurrent_tasks=2)
    agent = TaskAgent(config)
    agent.activate()
    
    # Add multiple tasks
    agent.add_task("Process data file A", "high", 2.0)  # 2 minutes estimated
    agent.add_task("Send notification email", "medium", 0.5)  # 30 seconds
    agent.add_task("Generate monthly report", "high", 3.0)  # 3 minutes
    agent.add_task("Update user database", "medium", 1.0)  # 1 minute
    
    print(f"\nAdded {len(agent.tasks)} tasks")
    
    # Process all tasks concurrently
    print("🔄 Processing all tasks concurrently...")
    start_time = datetime.now()
    
    results = await agent.process_all_pending()
    
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    print(f"\n✅ All tasks completed in {total_time:.1f} seconds")
    print(f"📊 Final summary: {agent.get_task_summary()}")
    
    agent.deactivate()


def pydantic_validation_example():
    """Demonstrate data validation."""
    print("\n🔍 Data Validation Example")
    print("-" * 30)
    
    # Create a valid task
    try:
        task = TaskModel(
            title="Complete project milestone",
            description="Finish all remaining tasks for the Q4 milestone",
            priority=Priority.HIGH,
            due_date=datetime.now() + timedelta(days=7),
            estimated_duration_minutes=240,  # 4 hours
            tags=["project", "milestone", "q4"]
        )
        
        print("✅ Valid task created:")
        print(f"   Title: {task.title}")
        print(f"   Priority: {task.priority}")
        print(f"   Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Tags: {', '.join(task.tags)}")
        print(f"   Overdue: {task.is_overdue()}")
        
        # Calculate time until due
        hours_until_due = task.time_until_due()
        if hours_until_due:
            print(f"   Time until due: {hours_until_due:.1f} hours")
        
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
    
    # Try to create an invalid task
    print("\n🚫 Testing validation (this should fail):")
    try:
        invalid_task = TaskModel(
            title="",  # Empty title - should fail validation
            description="This task has an empty title",
            priority="invalid",  # Invalid priority
            due_date=datetime.now() - timedelta(days=1)  # Past date
        )
        print("⚠️  This shouldn't print - validation should have failed!")
        
    except Exception as e:
        print(f"✅ Validation correctly rejected invalid data: {e}")


def interactive_example():
    """Simple interactive example."""
    print("\n💬 Interactive Example")
    print("-" * 25)
    
    config = AgentConfig(name="InteractiveBot")
    agent = TaskAgent(config)
    agent.activate()
    
    print("Agent is ready! You can add tasks.")
    print("Type 'quit' to exit, or 'help' for commands.")
    
    while True:
        user_input = input("\n> ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'help':
            print("Commands:")
            print("  add <description>  - Add a new task")
            print("  list              - Show all tasks")
            print("  summary           - Show task summary")
            print("  quit              - Exit")
        elif user_input.startswith('add '):
            task_desc = user_input[4:].strip()
            if task_desc:
                agent.add_task(task_desc)
            else:
                print("Please provide a task description.")
        elif user_input.lower() == 'list':
            if agent.tasks:
                print("📋 Current tasks:")
                for task_id, task in agent.tasks.items():
                    status_emoji = "✅" if task.status == "completed" else "⏳"
                    print(f"  {status_emoji} {task.description} ({task.priority})")
            else:
                print("No tasks yet.")
        elif user_input.lower() == 'summary':
            summary = agent.get_task_summary()
            print(f"📊 Summary: {summary['completed']}/{summary['total_tasks']} completed")
        else:
            print("Unknown command. Type 'help' for available commands.")
    
    agent.deactivate()
    print("👋 Goodbye!")


async def main():
    """Run all examples."""
    print("🚀 Python Agent Development - Quick Start")
    print("=" * 50)
    
    # Run basic examples
    basic_agent_example()
    task_agent_example()
    pydantic_validation_example()
    
    # Run async example
    await async_task_processing()
    
    # Ask if user wants interactive mode
    print("\n" + "=" * 50)
    response = input("Would you like to try the interactive example? (y/n): ")
    if response.lower().startswith('y'):
        interactive_example()
    
    print("\n✅ Quick start completed!")
    print("\nWhat to try next:")
    print("- Run 'python demo.py' for more advanced examples")
    print("- Explore the source code in src/ directory")
    print("- Run tests with 'python -m pytest tests/ -v'")


if __name__ == "__main__":
    asyncio.run(main())