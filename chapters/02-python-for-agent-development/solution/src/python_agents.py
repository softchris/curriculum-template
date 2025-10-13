"""
Professional AI Agent Development Examples - Chapter 2

This module demonstrates the Python techniques covered in Chapter 2:
- Object-oriented agent design
- Asynchronous programming
- Type hints and data validation
- Decorators for agent enhancement
- Modern Python tooling (Pydantic, requests, dataclasses)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Callable, Any, Protocol
from dataclasses import dataclass, field
from functools import wraps
import asyncio
import json
import time
import random


# =============================================================================
# Type Definitions and Data Models
# =============================================================================

@dataclass
class AgentConfig:
    """Configuration for agent initialization with proper typing."""
    name: str
    max_concurrent_tasks: int = 5
    timeout_seconds: float = 30.0
    enabled_capabilities: List[str] = field(default_factory=list)
    api_keys: Dict[str, str] = field(default_factory=dict)
    log_level: str = "INFO"


@dataclass
class TaskData:
    """Type-safe task data structure."""
    id: str
    description: str
    priority: str
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    estimated_duration: float = 1.0
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class WeatherData:
    """Type-safe weather data structure."""
    city: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


# =============================================================================
# Protocols and Interfaces
# =============================================================================

class MessageProcessor(Protocol):
    """Protocol defining the interface for message processing components."""
    
    def process(self, message: str) -> str:
        """Process a message and return the result."""
        ...
    
    def validate(self, message: str) -> bool:
        """Check if this processor can handle the given message."""
        ...


class TaskHandler(Protocol):
    """Protocol for task handling components."""
    
    def can_handle(self, task: TaskData) -> bool:
        """Check if this handler can process the given task."""
        ...
    
    async def handle(self, task: TaskData) -> str:
        """Process the task and return result."""
        ...


# =============================================================================
# Decorators for Agent Enhancement
# =============================================================================

def log_agent_action(func: Callable) -> Callable:
    """
    Decorator to automatically log agent method calls.
    Provides visibility into agent behavior for debugging and monitoring.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        method_name = func.__name__
        class_name = self.__class__.__name__
        agent_name = getattr(self, 'name', 'Unknown')
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {class_name}({agent_name}) -> {method_name}")
        
        try:
            result = func(self, *args, **kwargs)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {class_name}({agent_name}) -> {method_name} ✅")
            return result
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {class_name}({agent_name}) -> {method_name} ❌ {e}")
            raise
    
    return wrapper


def validate_agent_state(func: Callable) -> Callable:
    """
    Decorator to ensure agent is in valid state before method execution.
    Prevents operations on inactive or misconfigured agents.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check if agent has required is_active attribute
        if not hasattr(self, 'is_active'):
            raise AttributeError(f"Agent {self.__class__.__name__} must have is_active attribute")
        
        # Check if agent is active
        if not self.is_active:
            agent_name = getattr(self, 'name', 'Unknown')
            raise RuntimeError(f"Agent {agent_name} is not active. Call activate() first.")
        
        return func(self, *args, **kwargs)
    
    return wrapper


def measure_performance(func: Callable) -> Callable:
    """
    Decorator to measure and log method execution time.
    Essential for monitoring agent performance in production.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        method_name = func.__name__
        class_name = self.__class__.__name__
        
        try:
            result = func(self, *args, **kwargs)
            execution_time = time.time() - start_time
            print(f"⏱️  {class_name}.{method_name}: {execution_time:.3f}s")
            return result
        except Exception:
            execution_time = time.time() - start_time
            print(f"⏱️  {class_name}.{method_name}: {execution_time:.3f}s (FAILED)")
            raise
    
    return wrapper


def async_retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator for async functions to retry on failure.
    Useful for network operations and external API calls.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        print(f"All {max_attempts} attempts failed.")
            
            raise last_exception
        
        return wrapper
    return decorator


# =============================================================================
# Base Agent Classes
# =============================================================================

class BaseAgent:
    """
    Foundation class for all AI agents.
    Demonstrates clean OOP structure with proper initialization and lifecycle.
    """
    
    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.name = config.name
        self.is_active = False
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.metrics: Dict[str, Any] = {
            "tasks_processed": 0,
            "errors_count": 0,
            "total_runtime": 0.0
        }
    
    @log_agent_action
    def activate(self) -> None:
        """Start the agent and make it ready for tasks."""
        self.is_active = True
        self.last_activity = datetime.now()
        print(f"🤖 Agent {self.name} is now active!")
    
    @log_agent_action
    def deactivate(self) -> None:
        """Stop the agent safely."""
        self.is_active = False
        uptime = (datetime.now() - self.created_at).total_seconds()
        self.metrics["total_runtime"] = uptime
        print(f"🛑 Agent {self.name} deactivated after {uptime:.1f}s uptime")
    
    def get_status(self) -> Dict[str, Any]:
        """Return comprehensive agent status."""
        uptime = (datetime.now() - self.created_at).total_seconds()
        return {
            "name": self.name,
            "is_active": self.is_active,
            "uptime_seconds": uptime,
            "last_activity": self.last_activity.isoformat(),
            "metrics": self.metrics.copy(),
            "capabilities": self.config.enabled_capabilities
        }


# =============================================================================
# Specialized Agent Implementations
# =============================================================================

class TaskAgent(BaseAgent):
    """
    Specialized agent for task management with async capabilities.
    Demonstrates inheritance, async programming, and professional error handling.
    """
    
    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        self.tasks: Dict[str, TaskData] = {}
        self.task_handlers: Dict[str, TaskHandler] = {}
        self.processing_queue: asyncio.Queue = asyncio.Queue()
        self.is_processing = False
    
    @validate_agent_state
    @log_agent_action
    def add_task(self, description: str, priority: str = "medium", 
                 estimated_duration: float = 1.0, tags: List[str] = None) -> TaskData:
        """Add a new task with automatic ID generation and validation."""
        task_id = f"task_{len(self.tasks) + 1}_{int(time.time())}"
        
        if priority not in ["low", "medium", "high"]:
            raise ValueError(f"Invalid priority: {priority}. Must be low, medium, or high")
        
        task = TaskData(
            id=task_id,
            description=description,
            priority=priority,
            estimated_duration=estimated_duration,
            tags=tags or []
        )
        
        self.tasks[task_id] = task
        print(f"📝 Added task: {description} (Priority: {priority})")
        return task
    
    @validate_agent_state
    @measure_performance
    async def process_task(self, task_id: str) -> Optional[str]:
        """Process a specific task asynchronously."""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        if task.status != "pending":
            return f"Task {task_id} is not pending (current status: {task.status})"
        
        task.status = "processing"
        self.last_activity = datetime.now()
        
        try:
            # Simulate task processing with realistic delay
            await asyncio.sleep(min(task.estimated_duration, 3.0))
            
            # Mark as completed
            task.status = "completed"
            task.completed_at = datetime.now()
            
            self.metrics["tasks_processed"] += 1
            
            result = f"✅ Completed task: {task.description}"
            print(result)
            return result
            
        except Exception as e:
            task.status = "failed"
            self.metrics["errors_count"] += 1
            error_msg = f"❌ Task {task_id} failed: {e}"
            print(error_msg)
            return error_msg
    
    @validate_agent_state
    @log_agent_action
    async def process_all_pending(self) -> List[str]:
        """Process all pending tasks concurrently with proper concurrency limits."""
        pending_tasks = [task for task in self.tasks.values() if task.status == "pending"]
        
        if not pending_tasks:
            return ["No pending tasks to process"]
        
        # Limit concurrent processing
        semaphore = asyncio.Semaphore(self.config.max_concurrent_tasks)
        
        async def process_with_semaphore(task: TaskData) -> str:
            async with semaphore:
                return await self.process_task(task.id)
        
        # Process tasks concurrently
        tasks = [process_with_semaphore(task) for task in pending_tasks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(f"Error: {result}")
            else:
                processed_results.append(result or "Unknown result")
        
        return processed_results
    
    def get_task_summary(self) -> Dict[str, Any]:
        """Generate comprehensive task statistics."""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks.values() if t.status == "completed"])
        pending_tasks = len([t for t in self.tasks.values() if t.status == "pending"])
        failed_tasks = len([t for t in self.tasks.values() if t.status == "failed"])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "completed": completed_tasks,
            "pending": pending_tasks,
            "failed": failed_tasks,
            "completion_rate": round(completion_rate, 1),
            "average_processing_time": self._calculate_avg_processing_time()
        }
    
    def _calculate_avg_processing_time(self) -> float:
        """Calculate average task processing time."""
        completed_tasks = [t for t in self.tasks.values() 
                          if t.status == "completed" and t.completed_at]
        
        if not completed_tasks:
            return 0.0
        
        processing_times = []
        for task in completed_tasks:
            duration = (task.completed_at - task.created_at).total_seconds()
            processing_times.append(duration)
        
        return round(sum(processing_times) / len(processing_times), 2)


class WeatherMonitorAgent(BaseAgent):
    """
    Professional weather monitoring agent demonstrating:
    - Async programming for concurrent API calls
    - Type hints for reliability  
    - Decorators for logging and validation
    - Clean object-oriented design
    """
    
    def __init__(self, config: AgentConfig, cities: List[str]) -> None:
        super().__init__(config)
        self.cities = cities
        self.weather_cache: Dict[str, WeatherData] = {}
        self.update_interval = 300  # 5 minutes
        self.last_update = datetime.min
    
    @validate_agent_state
    @measure_performance
    @async_retry(max_attempts=3, delay=1.0)
    async def fetch_weather_data(self, city: str) -> Optional[WeatherData]:
        """Fetch weather data for a single city with retry logic."""
        # Simulate API call delay and occasional failures
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Simulate occasional API failures for demonstration
        if random.random() < 0.1:  # 10% failure rate
            raise Exception(f"Simulated API failure for {city}")
        
        # Generate realistic weather data
        base_temp = 60 + random.uniform(-30, 30)
        conditions = ["sunny", "cloudy", "partly cloudy", "rainy", "snowy", "foggy"]
        
        weather_data = WeatherData(
            city=city,
            temperature=round(base_temp, 1),
            condition=random.choice(conditions),
            humidity=random.randint(30, 90),
            wind_speed=round(random.uniform(0, 25), 1)
        )
        
        self.weather_cache[city] = weather_data
        self.last_activity = datetime.now()
        return weather_data
    
    @validate_agent_state
    @log_agent_action
    async def update_all_cities(self) -> Dict[str, WeatherData]:
        """Update weather data for all monitored cities concurrently."""
        print(f"🌤️  Updating weather for {len(self.cities)} cities...")
        
        # Create tasks for concurrent execution
        tasks = [self.fetch_weather_data(city) for city in self.cities]
        
        # Execute with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=self.config.timeout_seconds
            )
            
            # Process results
            successful_updates = {}
            for city, result in zip(self.cities, results):
                if isinstance(result, Exception):
                    print(f"❌ Failed to update {city}: {result}")
                    self.metrics["errors_count"] += 1
                elif result:
                    successful_updates[city] = result
            
            self.last_update = datetime.now()
            print(f"✅ Successfully updated {len(successful_updates)}/{len(self.cities)} cities")
            
            return successful_updates
            
        except asyncio.TimeoutError:
            print(f"⏰ Weather update timed out after {self.config.timeout_seconds}s")
            return {}
    
    def get_weather_summary(self) -> str:
        """Generate a human-readable weather summary."""
        if not self.weather_cache:
            return "❓ No weather data available. Call update_all_cities() first."
        
        summary_lines = ["🌤️ Weather Summary:"]
        summary_lines.append(f"   Last updated: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append("")
        
        # Sort cities by temperature for better readability
        sorted_cities = sorted(self.weather_cache.items(), 
                             key=lambda x: x[1].temperature, reverse=True)
        
        for city, data in sorted_cities:
            age_minutes = (datetime.now() - data.timestamp).total_seconds() / 60
            age_indicator = "🔄" if age_minutes > 30 else "✅"
            
            summary_lines.append(
                f"   {age_indicator} {city}: {data.temperature}°F, {data.condition}, "
                f"{data.humidity}% humidity, {data.wind_speed} mph wind"
            )
        
        return "\n".join(summary_lines)
    
    def get_alerts(self, temp_threshold: float = 32.0, 
                   wind_threshold: float = 20.0) -> List[str]:
        """Generate weather alerts based on thresholds."""
        alerts = []
        
        for city, data in self.weather_cache.items():
            if data.temperature <= temp_threshold:
                alerts.append(f"🥶 Freezing alert for {city}: {data.temperature}°F")
            
            if data.wind_threshold >= wind_threshold:
                alerts.append(f"💨 High wind alert for {city}: {data.wind_speed} mph")
            
            if data.condition == "snowy":
                alerts.append(f"❄️  Snow alert for {city}")
            elif data.condition == "rainy":
                alerts.append(f"🌧️  Rain alert for {city}")
        
        return alerts


# =============================================================================
# Composite Agent with Multiple Capabilities
# =============================================================================

class CompositeAgent(BaseAgent):
    """
    Advanced agent that combines multiple capabilities using composition.
    Demonstrates how to build complex agents from simpler components.
    """
    
    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        
        # Initialize sub-agents
        self.task_agent = TaskAgent(config)
        self.weather_agent = WeatherMonitorAgent(config, ["New York", "London", "Tokyo"])
        
        # Shared message processing
        self.message_history: List[Dict[str, Any]] = []
    
    @log_agent_action
    def activate(self) -> None:
        """Activate the composite agent and all its components."""
        super().activate()
        self.task_agent.activate()
        self.weather_agent.activate()
        print(f"🚀 Composite agent {self.name} fully activated!")
    
    @log_agent_action
    def deactivate(self) -> None:
        """Deactivate all components safely."""
        self.task_agent.deactivate()
        self.weather_agent.deactivate()
        super().deactivate()
    
    @validate_agent_state
    async def process_message(self, message: str) -> str:
        """Process natural language messages and route to appropriate handlers."""
        message_lower = message.lower()
        timestamp = datetime.now()
        
        # Store message in history
        self.message_history.append({
            "timestamp": timestamp.isoformat(),
            "message": message,
            "processed": False
        })
        
        response = ""
        
        try:
            # Route based on message content
            if any(word in message_lower for word in ["task", "todo", "work", "job"]):
                if "add" in message_lower or "create" in message_lower:
                    # Extract task description (simplified)
                    task_desc = message.replace("add task", "").replace("create task", "").strip()
                    if task_desc:
                        task = self.task_agent.add_task(task_desc)
                        response = f"✅ Added task: {task.description}"
                    else:
                        response = "❓ Please specify what task to add"
                
                elif "process" in message_lower or "do" in message_lower:
                    results = await self.task_agent.process_all_pending()
                    response = f"🔄 Processed tasks:\n" + "\n".join(results)
                
                elif "status" in message_lower or "summary" in message_lower:
                    summary = self.task_agent.get_task_summary()
                    response = f"📊 Task Status: {summary['completed']}/{summary['total_tasks']} completed ({summary['completion_rate']}%)"
            
            elif any(word in message_lower for word in ["weather", "temperature", "forecast"]):
                if "update" in message_lower:
                    await self.weather_agent.update_all_cities()
                    response = "🌤️ Weather data updated!"
                
                summary = self.weather_agent.get_weather_summary()
                alerts = self.weather_agent.get_alerts()
                
                response = summary
                if alerts:
                    response += "\n\n🚨 Alerts:\n" + "\n".join(alerts)
            
            elif "status" in message_lower:
                status = self.get_comprehensive_status()
                response = f"🤖 Agent Status:\n{json.dumps(status, indent=2, default=str)}"
            
            else:
                response = "🤔 I can help with tasks and weather. Try 'add task <description>', 'process tasks', or 'update weather'."
            
            # Mark message as processed
            self.message_history[-1]["processed"] = True
            self.last_activity = datetime.now()
            
            return response
            
        except Exception as e:
            self.metrics["errors_count"] += 1
            error_response = f"❌ Error processing message: {e}"
            print(error_response)
            return error_response
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get status from all components."""
        return {
            "main_agent": self.get_status(),
            "task_agent": self.task_agent.get_status(),
            "weather_agent": self.weather_agent.get_status(),
            "task_summary": self.task_agent.get_task_summary(),
            "message_count": len(self.message_history)
        }


# =============================================================================
# Demo and Example Usage
# =============================================================================

async def demo_async_agents():
    """Demonstrate async agent capabilities."""
    print("🚀 Starting Async Agent Demo")
    print("=" * 50)
    
    # Create agent configuration
    config = AgentConfig(
        name="DemoAgent",
        max_concurrent_tasks=3,
        timeout_seconds=10.0,
        enabled_capabilities=["task_management", "weather_monitoring"],
        log_level="INFO"
    )
    
    # Create and activate composite agent
    agent = CompositeAgent(config)
    agent.activate()
    
    try:
        # Demo task management
        print("\n📝 Task Management Demo:")
        await agent.process_message("add task Review project proposal")
        await agent.process_message("add task Send client email")
        await agent.process_message("add task Update documentation")
        
        # Process tasks
        print("\n🔄 Processing Tasks:")
        await agent.process_message("process tasks")
        
        # Demo weather monitoring
        print("\n🌤️ Weather Monitoring Demo:")
        await agent.process_message("update weather")
        
        # Get comprehensive status
        print("\n📊 Final Status:")
        await agent.process_message("status")
        
    finally:
        # Clean shutdown
        agent.deactivate()
        print("\n✅ Demo completed!")


def demo_decorators():
    """Demonstrate decorator functionality."""
    print("\n🎭 Decorator Demo")
    print("=" * 30)
    
    config = AgentConfig(name="DecoratorDemo")
    agent = TaskAgent(config)
    agent.activate()
    
    # Add tasks to see logging and performance measurement
    agent.add_task("Test task 1", "high")
    agent.add_task("Test task 2", "medium")
    
    print(f"\n📊 Agent status: {agent.get_status()}")
    agent.deactivate()


if __name__ == "__main__":
    print("🤖 Professional Python Agent Development Examples")
    print("Chapter 2: Python for Agent Development")
    print("=" * 60)
    
    # Run decorator demo
    demo_decorators()
    
    # Run async demo
    print("\n" + "=" * 60)
    asyncio.run(demo_async_agents())