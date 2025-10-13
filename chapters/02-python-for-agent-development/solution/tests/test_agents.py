"""
Tests for Python agent implementations.
Demonstrates how to test async agents and decorators.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.python_agents import (
    BaseAgent, TaskAgent, WeatherMonitorAgent, CompositeAgent,
    AgentConfig, log_agent_action, validate_agent_state, measure_performance
)


class TestAgentConfig:
    """Test agent configuration validation."""
    
    def test_valid_config_creation(self):
        """Test creating valid agent configuration."""
        config = AgentConfig(
            name="TestAgent",
            max_concurrent_tasks=5,
            timeout_seconds=30.0,
            enabled_capabilities=["test_capability"]
        )
        
        assert config.name == "TestAgent"
        assert config.max_concurrent_tasks == 5
        assert config.timeout_seconds == 30.0
        assert "test_capability" in config.enabled_capabilities
    
    def test_default_values(self):
        """Test that default values are applied correctly."""
        config = AgentConfig(name="MinimalAgent")
        
        assert config.max_concurrent_tasks == 5
        assert config.timeout_seconds == 30.0
        assert config.enabled_capabilities == []
        assert config.log_level == "INFO"


class TestBaseAgent:
    """Test base agent functionality."""
    
    def test_agent_creation(self):
        """Test basic agent creation and initialization."""
        config = AgentConfig(name="TestAgent")
        agent = BaseAgent(config)
        
        assert agent.name == "TestAgent"
        assert agent.is_active is False
        assert agent.config == config
        assert isinstance(agent.created_at, datetime)
    
    def test_agent_activation(self):
        """Test agent activation and deactivation."""
        config = AgentConfig(name="TestAgent")
        agent = BaseAgent(config)
        
        # Test activation
        agent.activate()
        assert agent.is_active is True
        
        # Test deactivation
        agent.deactivate()
        assert agent.is_active is False
    
    def test_agent_status(self):
        """Test agent status reporting."""
        config = AgentConfig(name="StatusAgent")
        agent = BaseAgent(config)
        agent.activate()
        
        status = agent.get_status()
        
        assert status["name"] == "StatusAgent"
        assert status["is_active"] is True
        assert "uptime_seconds" in status
        assert "metrics" in status
        assert status["capabilities"] == []


class TestTaskAgent:
    """Test task agent functionality."""
    
    def test_task_creation(self):
        """Test adding tasks to agent."""
        config = AgentConfig(name="TaskBot")
        agent = TaskAgent(config)
        agent.activate()
        
        task = agent.add_task("Test task", "high", 60.0)
        
        assert task.description == "Test task"
        assert task.priority == "high"
        assert task.estimated_duration == 60.0
        assert task.status == "pending"
        assert task.id in agent.tasks
    
    def test_invalid_priority(self):
        """Test that invalid priority raises error."""
        config = AgentConfig(name="TaskBot")
        agent = TaskAgent(config)
        agent.activate()
        
        with pytest.raises(ValueError, match="Invalid priority"):
            agent.add_task("Bad task", "invalid_priority")
    
    @pytest.mark.asyncio
    async def test_task_processing(self):
        """Test processing individual tasks."""
        config = AgentConfig(name="TaskBot")
        agent = TaskAgent(config)
        agent.activate()
        
        # Add a task
        task = agent.add_task("Process me", "medium", 0.1)  # Short duration for test
        
        # Process the task
        result = await agent.process_task(task.id)
        
        assert result is not None
        assert "Completed task" in result
        assert agent.tasks[task.id].status == "completed"
        assert agent.tasks[task.id].completed_at is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_task_processing(self):
        """Test processing multiple tasks concurrently."""
        config = AgentConfig(name="TaskBot", max_concurrent_tasks=2)
        agent = TaskAgent(config)
        agent.activate()
        
        # Add multiple tasks
        agent.add_task("Task 1", "high", 0.1)
        agent.add_task("Task 2", "medium", 0.1)
        agent.add_task("Task 3", "low", 0.1)
        
        # Process all tasks
        start_time = datetime.now()
        results = await agent.process_all_pending()
        end_time = datetime.now()
        
        # Check results
        assert len(results) == 3
        assert all("Completed task" in result for result in results)
        
        # Verify concurrent execution (should be faster than sequential)
        total_time = (end_time - start_time).total_seconds()
        assert total_time < 0.5  # Should be much faster than 0.3s sequential
    
    def test_task_summary(self):
        """Test task summary generation."""
        config = AgentConfig(name="TaskBot")
        agent = TaskAgent(config)
        agent.activate()
        
        # Add tasks
        agent.add_task("Task 1", "high")
        agent.add_task("Task 2", "medium")
        
        summary = agent.get_task_summary()
        
        assert summary["total_tasks"] == 2
        assert summary["pending"] == 2
        assert summary["completed"] == 0
        assert summary["completion_rate"] == 0.0


class TestWeatherMonitorAgent:
    """Test weather monitoring agent."""
    
    @pytest.mark.asyncio
    async def test_weather_data_fetch(self):
        """Test fetching weather data for a city."""
        config = AgentConfig(name="WeatherBot")
        agent = WeatherMonitorAgent(config, ["TestCity"])
        agent.activate()
        
        weather_data = await agent.fetch_weather_data("TestCity")
        
        assert weather_data is not None
        assert weather_data.city == "TestCity"
        assert isinstance(weather_data.temperature, float)
        assert weather_data.condition in ["sunny", "cloudy", "partly cloudy", "rainy", "snowy", "foggy"]
        assert 0 <= weather_data.humidity <= 100
    
    @pytest.mark.asyncio
    async def test_update_all_cities(self):
        """Test updating weather for multiple cities."""
        config = AgentConfig(name="WeatherBot")
        cities = ["City1", "City2", "City3"]
        agent = WeatherMonitorAgent(config, cities)
        agent.activate()
        
        results = await agent.update_all_cities()
        
        # Should get results for most cities (allowing for simulated failures)
        assert len(results) >= len(cities) * 0.7  # At least 70% success rate
        
        for city, weather_data in results.items():
            assert city in cities
            assert weather_data.city == city
    
    def test_weather_summary(self):
        """Test weather summary generation."""
        config = AgentConfig(name="WeatherBot")
        agent = WeatherMonitorAgent(config, ["TestCity"])
        agent.activate()
        
        # Initially no data
        summary = agent.get_weather_summary()
        assert "No weather data available" in summary
        
        # After adding data
        from src.python_agents import WeatherData
        test_weather = WeatherData(
            city="TestCity",
            temperature=72.0,
            condition="sunny",
            humidity=50,
            wind_speed=10.0
        )
        agent.weather_cache["TestCity"] = test_weather
        
        summary = agent.get_weather_summary()
        assert "TestCity" in summary
        assert "72.0°F" in summary
        assert "sunny" in summary


class TestCompositeAgent:
    """Test composite agent functionality."""
    
    @pytest.mark.asyncio
    async def test_message_processing(self):
        """Test natural language message processing."""
        config = AgentConfig(name="CompositeBot")
        agent = CompositeAgent(config)
        agent.activate()
        
        # Test task-related message
        response = await agent.process_message("add task Test the system")
        assert "Added task" in response
        
        # Test status message
        response = await agent.process_message("status")
        assert "Agent Status" in response
        
        agent.deactivate()
    
    @pytest.mark.asyncio
    async def test_component_activation(self):
        """Test that all components are activated properly."""
        config = AgentConfig(name="CompositeBot")
        agent = CompositeAgent(config)
        
        # Components should be inactive initially
        assert not agent.task_agent.is_active
        assert not agent.weather_agent.is_active
        
        # Activate composite agent
        agent.activate()
        
        # All components should be active
        assert agent.is_active
        assert agent.task_agent.is_active
        assert agent.weather_agent.is_active
        
        # Deactivate
        agent.deactivate()
        
        # All components should be inactive
        assert not agent.is_active
        assert not agent.task_agent.is_active
        assert not agent.weather_agent.is_active


class TestDecorators:
    """Test agent decorator functionality."""
    
    def test_log_agent_action_decorator(self):
        """Test the logging decorator."""
        
        class TestAgent:
            def __init__(self):
                self.name = "TestAgent"
            
            @log_agent_action
            def test_method(self):
                return "success"
        
        agent = TestAgent()
        
        # Test that method still works
        result = agent.test_method()
        assert result == "success"
    
    def test_validate_agent_state_decorator(self):
        """Test the state validation decorator."""
        
        class TestAgent:
            def __init__(self):
                self.name = "TestAgent"
                self.is_active = False
            
            @validate_agent_state
            def protected_method(self):
                return "success"
        
        agent = TestAgent()
        
        # Should raise error when inactive
        with pytest.raises(RuntimeError, match="not active"):
            agent.protected_method()
        
        # Should work when active
        agent.is_active = True
        result = agent.protected_method()
        assert result == "success"
    
    def test_measure_performance_decorator(self):
        """Test the performance measurement decorator."""
        
        class TestAgent:
            @measure_performance
            def timed_method(self):
                import time
                time.sleep(0.01)  # Small delay for measurement
                return "timed"
        
        agent = TestAgent()
        result = agent.timed_method()
        
        assert result == "timed"
        # The decorator should print timing info (tested manually)


@pytest.mark.asyncio
async def test_agent_integration():
    """Integration test for complete agent workflow."""
    config = AgentConfig(
        name="IntegrationTest",
        max_concurrent_tasks=2,
        enabled_capabilities=["task_management", "weather_monitoring"]
    )
    
    agent = CompositeAgent(config)
    agent.activate()
    
    try:
        # Add multiple tasks
        await agent.process_message("add task Integration test task 1")
        await agent.process_message("add task Integration test task 2")
        
        # Process tasks
        await agent.process_message("process tasks")
        
        # Check weather
        await agent.process_message("update weather")
        
        # Verify final state
        status = agent.get_comprehensive_status()
        assert status["main_agent"]["is_active"]
        assert status["task_summary"]["total_tasks"] == 2
        
    finally:
        agent.deactivate()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])