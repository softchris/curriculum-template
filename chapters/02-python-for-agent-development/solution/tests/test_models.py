"""
Tests for Pydantic models and data validation.
Demonstrates comprehensive testing of data models.
"""

import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from src.pydantic_models import (
    AgentConfiguration, TaskModel, WeatherModel, AgentMessage, AgentStatus,
    Priority, TaskStatus, AgentRole
)


class TestAgentConfiguration:
    """Test agent configuration model."""
    
    def test_valid_configuration(self):
        """Test creating valid agent configuration."""
        config = AgentConfiguration(
            name="TestAgent",
            role=AgentRole.TASK_MANAGER,
            max_concurrent_tasks=10,
            timeout_seconds=60.0,
            enabled_capabilities=["task_management", "scheduling"],
            api_keys={"weather": "test_key"},
            log_level="DEBUG"
        )
        
        assert config.name == "TestAgent"
        assert config.role == AgentRole.TASK_MANAGER
        assert config.max_concurrent_tasks == 10
        assert config.timeout_seconds == 60.0
        assert "task_management" in config.enabled_capabilities
        assert config.api_keys["weather"] == "test_key"
        assert config.log_level == "DEBUG"
    
    def test_default_values(self):
        """Test that default values are applied correctly."""
        config = AgentConfiguration(
            name="MinimalAgent",
            role=AgentRole.CHAT_ASSISTANT
        )
        
        assert config.max_concurrent_tasks == 5
        assert config.timeout_seconds == 30.0
        assert config.enabled_capabilities == []
        assert config.api_keys == {}
        assert config.log_level == "INFO"
    
    def test_name_validation(self):
        """Test name validation logic."""
        # Valid names
        valid_names = ["TestAgent", "My_Agent", "Agent-123", "Agent Name"]
        for name in valid_names:
            config = AgentConfiguration(name=name, role=AgentRole.TASK_MANAGER)
            assert config.name == name.strip()
        
        # Invalid names should raise validation error
        invalid_names = ["Agent@123", "Agent#", "Agent$pecial"]
        for name in invalid_names:
            with pytest.raises(ValidationError):
                AgentConfiguration(name=name, role=AgentRole.TASK_MANAGER)
    
    def test_capabilities_validation(self):
        """Test capabilities validation and normalization."""
        # Valid capabilities
        config = AgentConfiguration(
            name="TestAgent",
            role=AgentRole.TASK_MANAGER,
            enabled_capabilities=["Task_Management", "CHAT_ASSISTANCE", "api_integration"]
        )
        
        # Should be normalized to lowercase
        assert "task_management" in config.enabled_capabilities
        assert "chat_assistance" in config.enabled_capabilities
        assert "api_integration" in config.enabled_capabilities
        
        # Invalid capabilities should raise error
        with pytest.raises(ValidationError):
            AgentConfiguration(
                name="TestAgent",
                role=AgentRole.TASK_MANAGER,
                enabled_capabilities=["invalid_capability"]
            )
    
    def test_field_constraints(self):
        """Test field constraint validation."""
        # max_concurrent_tasks constraints
        with pytest.raises(ValidationError):
            AgentConfiguration(
                name="TestAgent",
                role=AgentRole.TASK_MANAGER,
                max_concurrent_tasks=0  # Should be >= 1
            )
        
        with pytest.raises(ValidationError):
            AgentConfiguration(
                name="TestAgent",
                role=AgentRole.TASK_MANAGER,
                max_concurrent_tasks=100  # Should be <= 50
            )
        
        # timeout_seconds constraints
        with pytest.raises(ValidationError):
            AgentConfiguration(
                name="TestAgent",
                role=AgentRole.TASK_MANAGER,
                timeout_seconds=0  # Should be > 0
            )


class TestTaskModel:
    """Test task data model."""
    
    def test_valid_task_creation(self):
        """Test creating valid task."""
        future_date = datetime.now() + timedelta(days=7)
        
        task = TaskModel(
            title="Test Task",
            description="This is a test task for validation",
            priority=Priority.HIGH,
            due_date=future_date,
            tags=["test", "validation"],
            category="testing",
            estimated_duration_minutes=120
        )
        
        assert task.title == "Test Task"
        assert task.description == "This is a test task for validation"
        assert task.priority == Priority.HIGH
        assert task.status == TaskStatus.PENDING
        assert task.due_date == future_date
        assert "test" in task.tags
        assert "validation" in task.tags
        assert task.category == "testing"
        assert task.estimated_duration_minutes == 120
        assert task.progress_percentage == 0.0
    
    def test_default_values(self):
        """Test default field values."""
        task = TaskModel(
            title="Minimal Task",
            description="Just title and description"
        )
        
        assert task.priority == Priority.MEDIUM
        assert task.status == TaskStatus.PENDING
        assert task.tags == []
        assert task.estimated_duration_minutes == 60.0
        assert task.progress_percentage == 0.0
        assert isinstance(task.created_at, datetime)
    
    def test_due_date_validation(self):
        """Test due date validation."""
        # Past due date should raise error
        past_date = datetime.now() - timedelta(days=1)
        
        with pytest.raises(ValidationError, match="Due date cannot be in the past"):
            TaskModel(
                title="Past Task",
                description="This task has a past due date",
                due_date=past_date
            )
    
    def test_tags_normalization(self):
        """Test tag cleaning and normalization."""
        task = TaskModel(
            title="Tagged Task",
            description="Task with various tags",
            tags=["Test Tag", "URGENT", "  spaced  ", "test tag"]  # Duplicates and spacing
        )
        
        # Should be normalized to lowercase, underscored, and deduplicated
        assert "test_tag" in task.tags
        assert "urgent" in task.tags
        assert "spaced" in task.tags
        assert len(task.tags) == 3  # Duplicates removed
    
    def test_progress_validation(self):
        """Test progress percentage validation."""
        # Completed task with less than 100% progress should fail
        with pytest.raises(ValidationError):
            TaskModel(
                title="Bad Task",
                description="Completed but not 100%",
                status=TaskStatus.COMPLETED,
                progress_percentage=50
            )
        
        # Pending task with progress should fail
        with pytest.raises(ValidationError):
            TaskModel(
                title="Bad Task",
                description="Pending but has progress",
                status=TaskStatus.PENDING,
                progress_percentage=25
            )
    
    def test_timing_consistency_validation(self):
        """Test timing field consistency."""
        now = datetime.now()
        
        # started_at before created_at should fail
        with pytest.raises(ValidationError):
            TaskModel(
                title="Bad Timing",
                description="Started before created",
                created_at=now,
                started_at=now - timedelta(minutes=10)
            )
        
        # completed_at before started_at should fail
        with pytest.raises(ValidationError):
            TaskModel(
                title="Bad Timing",
                description="Completed before started",
                started_at=now,
                completed_at=now - timedelta(minutes=5)
            )
    
    def test_utility_methods(self):
        """Test task utility methods."""
        now = datetime.now()
        future_date = now + timedelta(hours=2)
        past_date = now - timedelta(hours=1)
        
        # Test is_overdue
        overdue_task = TaskModel(
            title="Overdue Task",
            description="This task is overdue",
            due_date=past_date,
            status=TaskStatus.PENDING
        )
        assert overdue_task.is_overdue() is True
        
        completed_overdue_task = TaskModel(
            title="Completed Overdue",
            description="Was overdue but completed",
            due_date=past_date,
            status=TaskStatus.COMPLETED
        )
        assert completed_overdue_task.is_overdue() is False
        
        # Test time_until_due
        future_task = TaskModel(
            title="Future Task",
            description="Due in the future",
            due_date=future_date
        )
        time_until = future_task.time_until_due()
        assert time_until is not None
        assert 1.5 < time_until < 2.5  # Should be around 2 hours
        
        # Test calculate_actual_duration
        completed_task = TaskModel(
            title="Completed Task",
            description="Task with duration",
            status=TaskStatus.COMPLETED,
            started_at=now - timedelta(minutes=30),
            completed_at=now
        )
        duration = completed_task.calculate_actual_duration()
        assert duration is not None
        assert 29 < duration < 31  # Should be around 30 minutes


class TestWeatherModel:
    """Test weather data model."""
    
    def test_valid_weather_creation(self):
        """Test creating valid weather data."""
        weather = WeatherModel(
            city="New York",
            country_code="us",
            temperature_celsius=22.5,
            condition="partly cloudy",
            humidity_percent=65,
            wind_speed_kmh=15.2,
            wind_direction="nw",
            pressure_hpa=1013.2,
            uv_index=6,
            source="TestAPI"
        )
        
        assert weather.city == "New York"
        assert weather.country_code == "US"  # Should be uppercase
        assert weather.temperature_celsius == 22.5
        assert weather.condition == "Partly Cloudy"  # Should be title case
        assert weather.humidity_percent == 65
        assert weather.wind_direction == "NW"  # Should be uppercase
        assert weather.source == "TestAPI"
    
    def test_temperature_conversion(self):
        """Test automatic Fahrenheit calculation."""
        weather = WeatherModel(
            city="Test City",
            country_code="US",
            temperature_celsius=0.0,  # Freezing point
            condition="cold",
            humidity_percent=50
        )
        
        # Should auto-calculate Fahrenheit
        assert weather.temperature_fahrenheit == 32.0
        assert weather.get_temperature_fahrenheit() == 32.0
        
        # Test manual Fahrenheit
        weather_manual = WeatherModel(
            city="Test City",
            country_code="US",
            temperature_celsius=0.0,
            temperature_fahrenheit=35.0,  # Manual override
            condition="cold",
            humidity_percent=50
        )
        
        assert weather_manual.temperature_fahrenheit == 35.0
    
    def test_wind_direction_validation(self):
        """Test wind direction validation."""
        # Valid directions
        valid_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                           "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        
        for direction in valid_directions:
            weather = WeatherModel(
                city="Test",
                country_code="US",
                temperature_celsius=20,
                condition="test",
                humidity_percent=50,
                wind_direction=direction.lower()  # Test case conversion
            )
            assert weather.wind_direction == direction.upper()
        
        # Invalid direction should raise error
        with pytest.raises(ValidationError):
            WeatherModel(
                city="Test",
                country_code="US",
                temperature_celsius=20,
                condition="test",
                humidity_percent=50,
                wind_direction="INVALID"
            )
    
    def test_field_constraints(self):
        """Test field constraint validation."""
        # Temperature constraints
        with pytest.raises(ValidationError):
            WeatherModel(
                city="Test",
                country_code="US",
                temperature_celsius=-150,  # Too cold
                condition="frozen",
                humidity_percent=50
            )
        
        # Humidity constraints
        with pytest.raises(ValidationError):
            WeatherModel(
                city="Test",
                country_code="US",
                temperature_celsius=20,
                condition="test",
                humidity_percent=150  # Too high
            )
        
        # Wind speed constraints
        with pytest.raises(ValidationError):
            WeatherModel(
                city="Test",
                country_code="US",
                temperature_celsius=20,
                condition="test",
                humidity_percent=50,
                wind_speed_kmh=600  # Too fast
            )
    
    def test_utility_methods(self):
        """Test weather utility methods."""
        # Comfortable temperature
        comfortable_weather = WeatherModel(
            city="Comfortable",
            country_code="US",
            temperature_celsius=21,  # Comfortable range
            condition="nice",
            humidity_percent=50
        )
        assert comfortable_weather.is_comfortable_temperature() is True
        
        # Uncomfortable temperature
        hot_weather = WeatherModel(
            city="Hot",
            country_code="US",
            temperature_celsius=35,  # Too hot
            condition="hot",
            humidity_percent=80
        )
        assert hot_weather.is_comfortable_temperature() is False


class TestAgentMessage:
    """Test agent message model."""
    
    def test_valid_message_creation(self):
        """Test creating valid message."""
        message = AgentMessage(
            sender="user123",
            recipient="agent456",
            content="Hello, can you help me with a task?",
            message_type="text",
            priority=Priority.MEDIUM,
            requires_response=True
        )
        
        assert message.sender == "user123"
        assert message.recipient == "agent456"
        assert message.content == "Hello, can you help me with a task?"
        assert message.message_type == "text"
        assert message.priority == Priority.MEDIUM
        assert message.requires_response is True
        assert message.is_processed is False
    
    def test_content_validation(self):
        """Test message content validation."""
        # Empty content should fail
        with pytest.raises(ValidationError):
            AgentMessage(
                sender="user",
                recipient="agent",
                content=""
            )
        
        # Whitespace-only content should fail
        with pytest.raises(ValidationError):
            AgentMessage(
                sender="user",
                recipient="agent",
                content="   "
            )
        
        # Content with leading/trailing whitespace should be trimmed
        message = AgentMessage(
            sender="user",
            recipient="agent",
            content="  Hello world!  "
        )
        assert message.content == "Hello world!"
    
    def test_message_processing(self):
        """Test message processing workflow."""
        message = AgentMessage(
            sender="user",
            recipient="agent",
            content="Test message"
        )
        
        # Initially not processed
        assert message.is_processed is False
        assert message.processed_at is None
        assert message.processing_time_ms is None
        
        # Mark as processed
        message.mark_processed(processing_time_ms=150.5)
        
        assert message.is_processed is True
        assert message.processed_at is not None
        assert message.processing_time_ms == 150.5
        assert message.error_message is None
        
        # Mark with error
        error_message = AgentMessage(
            sender="user",
            recipient="agent",
            content="Error test"
        )
        error_message.mark_processed(error="Something went wrong")
        
        assert error_message.error_message == "Something went wrong"


class TestAgentStatus:
    """Test agent status model."""
    
    def test_valid_status_creation(self):
        """Test creating valid agent status."""
        config = AgentConfiguration(
            name="StatusAgent",
            role=AgentRole.TASK_MANAGER
        )
        
        status = AgentStatus(
            agent_name="StatusAgent",
            role=AgentRole.TASK_MANAGER,
            is_active=True,
            tasks_processed=10,
            errors_count=1,
            average_response_time_ms=250.5,
            configuration=config
        )
        
        assert status.agent_name == "StatusAgent"
        assert status.role == AgentRole.TASK_MANAGER
        assert status.is_active is True
        assert status.tasks_processed == 10
        assert status.errors_count == 1
        assert status.average_response_time_ms == 250.5
        assert status.configuration == config
    
    def test_health_score_calculation(self):
        """Test agent health score calculation."""
        config = AgentConfiguration(name="Test", role=AgentRole.TASK_MANAGER)
        
        # Perfect health (no errors)
        perfect_status = AgentStatus(
            agent_name="Perfect",
            role=AgentRole.TASK_MANAGER,
            tasks_processed=100,
            errors_count=0,
            average_response_time_ms=100,
            configuration=config
        )
        assert perfect_status.get_health_score() == 100.0
        
        # Some errors
        error_status = AgentStatus(
            agent_name="Errors",
            role=AgentRole.TASK_MANAGER,
            tasks_processed=100,
            errors_count=10,  # 10% error rate
            average_response_time_ms=100,
            configuration=config
        )
        assert error_status.get_health_score() == 90.0
        
        # Slow response time penalty
        slow_status = AgentStatus(
            agent_name="Slow",
            role=AgentRole.TASK_MANAGER,
            tasks_processed=100,
            errors_count=0,
            average_response_time_ms=6000,  # 6 seconds (slow)
            configuration=config
        )
        assert slow_status.get_health_score() == 80.0  # 20% penalty
    
    def test_task_summary(self):
        """Test task summary generation."""
        from src.pydantic_models import TaskModel, TaskStatus
        
        config = AgentConfiguration(name="Test", role=AgentRole.TASK_MANAGER)
        
        # Create some test tasks
        tasks = [
            TaskModel(title="Task 1", description="Pending", status=TaskStatus.PENDING),
            TaskModel(title="Task 2", description="In Progress", status=TaskStatus.IN_PROGRESS),
            TaskModel(title="Task 3", description="Completed", status=TaskStatus.COMPLETED),
            TaskModel(title="Task 4", description="Completed", status=TaskStatus.COMPLETED),
        ]
        
        status = AgentStatus(
            agent_name="TaskAgent",
            role=AgentRole.TASK_MANAGER,
            active_tasks=tasks,
            configuration=config
        )
        
        summary = status.get_task_summary()
        
        assert summary[TaskStatus.PENDING.value] == 1
        assert summary[TaskStatus.IN_PROGRESS.value] == 1
        assert summary[TaskStatus.COMPLETED.value] == 2
        assert summary[TaskStatus.FAILED.value] == 0
        assert summary[TaskStatus.CANCELLED.value] == 0


def test_model_json_serialization():
    """Test that all models can be serialized to/from JSON."""
    from src.pydantic_models import export_model_schemas
    
    # Test schema export
    schemas = export_model_schemas()
    
    # Should have schemas for all main models
    expected_models = [
        "AgentConfiguration",
        "TaskModel", 
        "WeatherModel",
        "AgentMessage",
        "AgentStatus"
    ]
    
    for model_name in expected_models:
        assert model_name in schemas
        assert "properties" in schemas[model_name]
        assert "required" in schemas[model_name]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])