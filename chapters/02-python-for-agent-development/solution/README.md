# Python for Agent Development - Solution Code

This directory contains comprehensive examples demonstrating the Python techniques covered in Chapter 2: Python for Agent Development.

## Overview

The solution demonstrates professional Python patterns for building AI agents:

- **Object-oriented design** with clean inheritance and composition
- **Asynchronous programming** for responsive, concurrent agent behavior  
- **Type hints** for robust, self-documenting code
- **Decorators** for clean separation of concerns
- **Modern Python tooling** including Pydantic for data validation

## Files Structure

```
solution/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── demo.py                   # Quick demonstration script
├── quickstart.py            # Simple getting started example
├── src/
│   ├── python_agents.py     # Complete agent implementations
│   └── pydantic_models.py   # Data validation examples
└── tests/
    ├── test_agents.py       # Agent functionality tests
    └── test_models.py       # Pydantic model tests
```

## Installation and Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Quick Demo

```bash
python demo.py
```

### 3. Try the Interactive Examples

```bash
python quickstart.py
```

### 4. Run Tests

```bash
python -m pytest tests/ -v
```

## Key Examples

### Basic Agent Structure

The `BaseAgent` class demonstrates professional agent architecture:

```python
from src.python_agents import BaseAgent, AgentConfig

# Create agent configuration
config = AgentConfig(
    name="MyAgent",
    max_concurrent_tasks=5,
    enabled_capabilities=["task_management"]
)

# Create and activate agent
agent = BaseAgent(config)
agent.activate()

# Check status
status = agent.get_status()
print(f"Agent {status['name']} is {'active' if status['is_active'] else 'inactive'}")
```

### Async Task Processing

The `TaskAgent` shows how to handle multiple tasks concurrently:

```python
import asyncio
from src.python_agents import TaskAgent, AgentConfig

async def demo_async_tasks():
    config = AgentConfig(name="TaskBot", max_concurrent_tasks=3)
    agent = TaskAgent(config)
    agent.activate()
    
    # Add multiple tasks
    agent.add_task("Process data", "high")
    agent.add_task("Send email", "medium") 
    agent.add_task("Update docs", "low")
    
    # Process all tasks concurrently
    results = await agent.process_all_pending()
    print(f"Processed {len(results)} tasks")

# Run the async demo
asyncio.run(demo_async_tasks())
```

### Data Validation with Pydantic

The `pydantic_models.py` file shows robust data validation:

```python
from src.pydantic_models import TaskModel, Priority

# Create validated task
task = TaskModel(
    title="Review budget report",
    description="Analyze Q4 budget performance",
    priority=Priority.HIGH,
    estimated_duration_minutes=120
)

# Automatic validation catches errors
try:
    invalid_task = TaskModel(
        title="",  # Empty title - will raise ValidationError
        description="Test"
    )
except ValueError as e:
    print(f"Validation error: {e}")
```

### Professional Decorators

The codebase includes several useful decorators:

```python
from src.python_agents import log_agent_action, validate_agent_state, measure_performance

class MyAgent:
    def __init__(self):
        self.is_active = False
    
    @log_agent_action
    def activate(self):
        self.is_active = True
    
    @validate_agent_state
    @measure_performance
    async def process_data(self, data):
        # This method will:
        # 1. Check if agent is active
        # 2. Measure execution time
        # 3. Log the operation
        await asyncio.sleep(1)  # Simulate work
        return "Processed"
```

## Advanced Examples

### Composite Agent Architecture

The `CompositeAgent` combines multiple capabilities:

```python
from src.python_agents import CompositeAgent, AgentConfig

async def demo_composite_agent():
    config = AgentConfig(
        name="SuperAgent",
        enabled_capabilities=["task_management", "weather_monitoring"]
    )
    
    agent = CompositeAgent(config)
    agent.activate()
    
    # Process natural language commands
    await agent.process_message("add task Review project proposal")
    await agent.process_message("update weather")
    await agent.process_message("process tasks")
    
    agent.deactivate()

asyncio.run(demo_composite_agent())
```

### Weather Monitoring with Retry Logic

The `WeatherMonitorAgent` demonstrates resilient async operations:

```python
from src.python_agents import WeatherMonitorAgent, AgentConfig

async def demo_weather_monitoring():
    config = AgentConfig(name="WeatherBot", timeout_seconds=10)
    cities = ["New York", "London", "Tokyo", "Sydney"]
    
    agent = WeatherMonitorAgent(config, cities)
    agent.activate()
    
    # Update all cities concurrently with retry logic
    weather_data = await agent.update_all_cities()
    
    # Get summary and alerts
    print(agent.get_weather_summary())
    alerts = agent.get_alerts(temp_threshold=32, wind_threshold=20)
    for alert in alerts:
        print(alert)

asyncio.run(demo_weather_monitoring())
```

## Testing

The test suite demonstrates how to test async agents:

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_agents.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Best Practices Demonstrated

### 1. Type Safety
- Comprehensive type hints throughout
- Pydantic models for data validation
- Protocol definitions for duck typing

### 2. Error Handling
- Graceful failure handling in async operations
- Retry logic with exponential backoff
- Proper exception propagation

### 3. Code Organization
- Clear separation of concerns
- Composition over inheritance where appropriate
- Modular, testable design

### 4. Performance Optimization
- Async/await for I/O-bound operations
- Concurrent task processing
- Connection pooling patterns

### 5. Monitoring and Observability
- Comprehensive logging decorators
- Performance measurement
- Health checks and status reporting

## Common Patterns

### Agent Lifecycle Management

```python
# Always follow this pattern
agent = SomeAgent(config)
try:
    agent.activate()
    # Do work with agent
    result = await agent.do_something()
finally:
    agent.deactivate()  # Ensure cleanup
```

### Error Handling in Async Methods

```python
async def robust_method(self):
    try:
        result = await some_async_operation()
        return result
    except asyncio.TimeoutError:
        self.logger.warning("Operation timed out")
        return None
    except Exception as e:
        self.logger.error(f"Unexpected error: {e}")
        self.metrics["errors_count"] += 1
        raise
```

### Data Validation Pattern

```python
# Always validate input data
def process_task_data(self, raw_data: dict) -> TaskModel:
    try:
        # Pydantic handles validation automatically
        task = TaskModel(**raw_data)
        return task
    except ValidationError as e:
        self.logger.error(f"Invalid task data: {e}")
        raise ValueError(f"Invalid task data: {e}")
```

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure to install dependencies with `pip install -r requirements.txt`

2. **Async Runtime Errors**: Always use `asyncio.run()` for top-level async calls

3. **Validation Errors**: Check Pydantic model definitions for field constraints

4. **Agent Not Responding**: Ensure agent is activated before calling methods

### Debug Mode

Enable detailed logging by setting the log level:

```python
config = AgentConfig(name="DebugAgent", log_level="DEBUG")
```

## Next Steps

After understanding these examples:

1. **Experiment** with different agent configurations
2. **Extend** the agents with new capabilities
3. **Test** your changes with the provided test suite
4. **Profile** performance using the measurement decorators

This foundation prepares you for the advanced agent architectures covered in Chapter 3!