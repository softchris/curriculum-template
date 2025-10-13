"""
Pydantic Models and Data Validation Examples

Demonstrates professional data validation and serialization patterns
using Pydantic for AI agent development.
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Dict, Union, Literal
from datetime import datetime, date
from enum import Enum
import json


# =============================================================================
# Enums for Type Safety
# =============================================================================

class Priority(str, Enum):
    """Task priority levels with string enum for API compatibility."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    """Task status progression."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentRole(str, Enum):
    """Agent role types."""
    TASK_MANAGER = "task_manager"
    WEATHER_MONITOR = "weather_monitor"
    CHAT_ASSISTANT = "chat_assistant"
    API_INTEGRATION = "api_integration"


# =============================================================================
# Core Pydantic Models
# =============================================================================

class AgentConfiguration(BaseModel):
    """
    Comprehensive agent configuration with validation.
    Demonstrates Pydantic's powerful validation capabilities.
    """
    
    name: str = Field(..., min_length=1, max_length=100, description="Agent name")
    role: AgentRole = Field(..., description="Primary agent role")
    max_concurrent_tasks: int = Field(5, ge=1, le=50, description="Maximum concurrent tasks")
    timeout_seconds: float = Field(30.0, gt=0, le=300, description="Operation timeout")
    enabled_capabilities: List[str] = Field(default_factory=list, description="Enabled capabilities")
    api_keys: Dict[str, str] = Field(default_factory=dict, description="API keys by service")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        # Generate JSON schema
        schema_extra = {
            "example": {
                "name": "TaskBot",
                "role": "task_manager",
                "max_concurrent_tasks": 10,
                "timeout_seconds": 60.0,
                "enabled_capabilities": ["task_management", "scheduling"],
                "api_keys": {"weather_api": "your_api_key_here"},
                "log_level": "INFO"
            }
        }
    
    @validator('name')
    def validate_name(cls, v):
        """Ensure name contains only valid characters."""
        if not v.replace('_', '').replace('-', '').replace(' ', '').isalnum():
            raise ValueError('Name must contain only alphanumeric characters, spaces, hyphens, and underscores')
        return v.strip()
    
    @validator('enabled_capabilities')
    def validate_capabilities(cls, v):
        """Validate and normalize capability names."""
        valid_capabilities = {
            'task_management', 'weather_monitoring', 'chat_assistance',
            'api_integration', 'file_processing', 'email_handling'
        }
        
        normalized = []
        for capability in v:
            capability_clean = capability.lower().strip()
            if capability_clean not in valid_capabilities:
                raise ValueError(f'Unknown capability: {capability}. Valid options: {valid_capabilities}')
            normalized.append(capability_clean)
        
        return list(set(normalized))  # Remove duplicates


class TaskModel(BaseModel):
    """
    Comprehensive task model with rich validation.
    Shows advanced Pydantic patterns for data integrity.
    """
    
    id: Optional[str] = Field(None, description="Unique task identifier")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, max_length=2000, description="Detailed description")
    priority: Priority = Field(Priority.MEDIUM, description="Task priority level")
    status: TaskStatus = Field(TaskStatus.PENDING, description="Current task status")
    
    # Timing fields
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[datetime] = Field(None, description="Task deadline")
    started_at: Optional[datetime] = Field(None, description="When task processing started")
    completed_at: Optional[datetime] = Field(None, description="When task was completed")
    
    # Organization
    tags: List[str] = Field(default_factory=list, description="Task tags for organization")
    category: Optional[str] = Field(None, max_length=50, description="Task category")
    assigned_to: Optional[str] = Field(None, description="Agent or user assigned to task")
    
    # Estimation and tracking
    estimated_duration_minutes: float = Field(60.0, gt=0, le=10080, description="Estimated duration in minutes")  # Max 1 week
    actual_duration_minutes: Optional[float] = Field(None, ge=0, description="Actual time spent")
    progress_percentage: float = Field(0.0, ge=0, le=100, description="Completion percentage")
    
    # Metadata
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        """Pydantic configuration for the task model."""
        # Allow field names to be used as aliases
        allow_population_by_field_name = True
        
        # Validate assignments
        validate_assignment = True
        
        # Example for documentation
        schema_extra = {
            "example": {
                "title": "Review quarterly budget report",
                "description": "Analyze Q3 budget performance and prepare recommendations",
                "priority": "high",
                "due_date": "2024-01-15T17:00:00",
                "tags": ["finance", "quarterly", "analysis"],
                "category": "reporting",
                "estimated_duration_minutes": 120
            }
        }
    
    @validator('due_date')
    def validate_due_date(cls, v, values):
        """Ensure due date is not in the past."""
        if v and v < datetime.now():
            raise ValueError('Due date cannot be in the past')
        return v
    
    @validator('tags')
    def validate_and_normalize_tags(cls, v):
        """Clean and normalize tags."""
        if not v:
            return []
        
        normalized_tags = []
        for tag in v:
            # Clean and normalize
            clean_tag = tag.lower().strip().replace(' ', '_')
            if clean_tag and len(clean_tag) <= 30:  # Reasonable tag length limit
                normalized_tags.append(clean_tag)
        
        # Remove duplicates and return
        return list(set(normalized_tags))
    
    @validator('progress_percentage')
    def validate_progress(cls, v, values):
        """Ensure progress is consistent with status."""
        status = values.get('status')
        
        if status == TaskStatus.COMPLETED and v < 100:
            raise ValueError('Completed tasks must have 100% progress')
        elif status == TaskStatus.PENDING and v > 0:
            raise ValueError('Pending tasks should have 0% progress')
        
        return v
    
    @root_validator
    def validate_timing_consistency(cls, values):
        """Ensure timing fields are logically consistent."""
        created_at = values.get('created_at')
        started_at = values.get('started_at')
        completed_at = values.get('completed_at')
        due_date = values.get('due_date')
        
        # Check chronological order
        if started_at and created_at and started_at < created_at:
            raise ValueError('Task cannot be started before it was created')
        
        if completed_at and started_at and completed_at < started_at:
            raise ValueError('Task cannot be completed before it was started')
        
        if completed_at and created_at and completed_at < created_at:
            raise ValueError('Task cannot be completed before it was created')
        
        # Check due date consistency
        if due_date and completed_at and completed_at > due_date:
            # This is just a warning case, not an error
            pass
        
        return values
    
    def calculate_actual_duration(self) -> Optional[float]:
        """Calculate actual duration if task is completed."""
        if self.status == TaskStatus.COMPLETED and self.started_at and self.completed_at:
            duration_seconds = (self.completed_at - self.started_at).total_seconds()
            return duration_seconds / 60  # Convert to minutes
        return None
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date:
            return False
        return datetime.now() > self.due_date and self.status != TaskStatus.COMPLETED
    
    def time_until_due(self) -> Optional[float]:
        """Get hours until due date."""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.now()
        return delta.total_seconds() / 3600  # Convert to hours


class WeatherModel(BaseModel):
    """
    Weather data model with comprehensive validation.
    Demonstrates handling of external API data with Pydantic.
    """
    
    city: str = Field(..., min_length=1, max_length=100)
    country_code: str = Field(..., min_length=2, max_length=3, description="ISO country code")
    
    # Current conditions
    temperature_celsius: float = Field(..., ge=-100, le=60, description="Temperature in Celsius")
    temperature_fahrenheit: Optional[float] = Field(None, description="Temperature in Fahrenheit")
    condition: str = Field(..., description="Weather condition description")
    humidity_percent: int = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed_kmh: float = Field(0.0, ge=0, le=500, description="Wind speed in km/h")
    wind_direction: Optional[str] = Field(None, description="Wind direction (N, NE, E, etc.)")
    
    # Additional data
    pressure_hpa: Optional[float] = Field(None, ge=800, le=1200, description="Atmospheric pressure")
    visibility_km: Optional[float] = Field(None, ge=0, le=50, description="Visibility in kilometers")
    uv_index: Optional[int] = Field(None, ge=0, le=15, description="UV index")
    
    # Timestamps
    observed_at: datetime = Field(default_factory=datetime.now)
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    
    # Data source
    source: str = Field("unknown", description="Weather data source")
    source_url: Optional[str] = Field(None, description="Source API URL")
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        schema_extra = {
            "example": {
                "city": "New York",
                "country_code": "US",
                "temperature_celsius": 22.5,
                "condition": "Partly cloudy",
                "humidity_percent": 65,
                "wind_speed_kmh": 15.2,
                "wind_direction": "NW",
                "pressure_hpa": 1013.2,
                "uv_index": 6,
                "source": "WeatherAPI"
            }
        }
    
    @validator('temperature_fahrenheit', always=True)
    def calculate_fahrenheit(cls, v, values):
        """Auto-calculate Fahrenheit from Celsius if not provided."""
        if v is None and 'temperature_celsius' in values:
            celsius = values['temperature_celsius']
            return round(celsius * 9/5 + 32, 1)
        return v
    
    @validator('country_code')
    def validate_country_code(cls, v):
        """Ensure country code is uppercase."""
        return v.upper()
    
    @validator('condition')
    def validate_condition(cls, v):
        """Normalize weather condition."""
        return v.title()  # Title case
    
    @validator('wind_direction')
    def validate_wind_direction(cls, v):
        """Validate wind direction."""
        if v is None:
            return v
        
        valid_directions = {
            'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'
        }
        
        v_upper = v.upper()
        if v_upper not in valid_directions:
            raise ValueError(f'Invalid wind direction. Valid options: {valid_directions}')
        
        return v_upper
    
    def get_temperature_fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        if self.temperature_fahrenheit is not None:
            return self.temperature_fahrenheit
        return round(self.temperature_celsius * 9/5 + 32, 1)
    
    def is_comfortable_temperature(self) -> bool:
        """Check if temperature is in comfortable range (18-24°C)."""
        return 18 <= self.temperature_celsius <= 24


class AgentMessage(BaseModel):
    """
    Message model for agent communication.
    Demonstrates handling of conversational data.
    """
    
    id: Optional[str] = Field(None, description="Message ID")
    sender: str = Field(..., description="Message sender (user ID or agent name)")
    recipient: str = Field(..., description="Message recipient")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    message_type: Literal["text", "command", "response", "error", "system"] = "text"
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    
    # Message metadata
    priority: Priority = Priority.MEDIUM
    requires_response: bool = True
    context: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict)
    
    # Processing status
    is_processed: bool = False
    processing_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    
    class Config:
        """Configuration for message model."""
        validate_assignment = True
        
    @validator('content')
    def validate_content(cls, v):
        """Clean and validate message content."""
        # Strip whitespace
        v = v.strip()
        
        # Check for empty message
        if not v:
            raise ValueError('Message content cannot be empty')
        
        return v
    
    @validator('sender', 'recipient')
    def validate_participant_names(cls, v):
        """Validate sender and recipient names."""
        if not v.strip():
            raise ValueError('Sender and recipient names cannot be empty')
        return v.strip()
    
    def mark_processed(self, processing_time_ms: float = None, error: str = None) -> None:
        """Mark message as processed."""
        self.is_processed = True
        self.processed_at = datetime.now()
        self.processing_time_ms = processing_time_ms
        self.error_message = error


# =============================================================================
# Complex Nested Models
# =============================================================================

class AgentStatus(BaseModel):
    """
    Comprehensive agent status model.
    Demonstrates complex nested data structures with Pydantic.
    """
    
    agent_name: str = Field(..., description="Agent identifier")
    role: AgentRole = Field(..., description="Agent role")
    is_active: bool = Field(False, description="Whether agent is currently active")
    
    # Timing information
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    uptime_seconds: float = Field(0.0, ge=0, description="Total uptime in seconds")
    
    # Performance metrics
    tasks_processed: int = Field(0, ge=0, description="Total tasks processed")
    errors_count: int = Field(0, ge=0, description="Total errors encountered")
    average_response_time_ms: float = Field(0.0, ge=0, description="Average response time")
    
    # Current state
    active_tasks: List[TaskModel] = Field(default_factory=list, description="Currently active tasks")
    pending_messages: List[AgentMessage] = Field(default_factory=list, description="Pending messages")
    
    # Capabilities and configuration
    enabled_capabilities: List[str] = Field(default_factory=list)
    configuration: AgentConfiguration = Field(..., description="Agent configuration")
    
    # Resource usage
    memory_usage_mb: Optional[float] = Field(None, ge=0, description="Memory usage in MB")
    cpu_usage_percent: Optional[float] = Field(None, ge=0, le=100, description="CPU usage percentage")
    
    class Config:
        """Configuration for agent status model."""
        validate_assignment = True
    
    @validator('uptime_seconds', always=True)
    def calculate_uptime(cls, v, values):
        """Calculate uptime from creation time."""
        if 'created_at' in values:
            created_at = values['created_at']
            uptime = (datetime.now() - created_at).total_seconds()
            return max(uptime, 0)  # Ensure non-negative
        return v
    
    def get_task_summary(self) -> Dict[str, int]:
        """Get summary of tasks by status."""
        summary = {}
        for status in TaskStatus:
            count = len([task for task in self.active_tasks if task.status == status])
            summary[status.value] = count
        return summary
    
    def get_health_score(self) -> float:
        """Calculate agent health score (0-100)."""
        if self.tasks_processed == 0:
            return 100.0  # New agent, assume healthy
        
        error_rate = self.errors_count / self.tasks_processed
        health_score = max(0, 100 - (error_rate * 100))
        
        # Adjust for response time (penalize slow responses)
        if self.average_response_time_ms > 5000:  # 5 seconds
            health_score *= 0.8
        
        return round(health_score, 1)


# =============================================================================
# Validation Examples and Utility Functions
# =============================================================================

def create_sample_task() -> TaskModel:
    """Create a sample task with realistic data."""
    return TaskModel(
        title="Process customer feedback survey",
        description="Analyze responses from Q4 customer satisfaction survey and prepare summary report",
        priority=Priority.HIGH,
        due_date=datetime(2024, 1, 15, 17, 0),
        tags=["customer_service", "analytics", "quarterly"],
        category="analysis",
        estimated_duration_minutes=180
    )


def create_sample_weather() -> WeatherModel:
    """Create sample weather data."""
    return WeatherModel(
        city="San Francisco",
        country_code="US",
        temperature_celsius=18.5,
        condition="Partly cloudy",
        humidity_percent=72,
        wind_speed_kmh=12.5,
        wind_direction="NW",
        pressure_hpa=1015.3,
        uv_index=5,
        source="OpenWeatherMap"
    )


def validate_agent_data(data: dict) -> AgentConfiguration:
    """
    Demonstrate Pydantic validation with error handling.
    """
    try:
        config = AgentConfiguration(**data)
        print(f"✅ Valid agent configuration: {config.name}")
        return config
    except Exception as e:
        print(f"❌ Validation error: {e}")
        raise


def export_model_schemas():
    """Export JSON schemas for all models."""
    models = [
        AgentConfiguration,
        TaskModel,
        WeatherModel,
        AgentMessage,
        AgentStatus
    ]
    
    schemas = {}
    for model in models:
        schemas[model.__name__] = model.schema()
    
    return schemas


if __name__ == "__main__":
    print("🔍 Pydantic Models and Validation Demo")
    print("=" * 50)
    
    # Create sample task
    print("\n📝 Creating sample task:")
    task = create_sample_task()
    print(f"Task: {task.title}")
    print(f"Due: {task.due_date}")
    print(f"Tags: {task.tags}")
    
    # Test validation
    print("\n✅ Testing validation:")
    try:
        # This should work
        valid_config = {
            "name": "TestAgent",
            "role": "task_manager",
            "max_concurrent_tasks": 5,
            "enabled_capabilities": ["task_management", "scheduling"]
        }
        config = validate_agent_data(valid_config)
        
        # This should fail
        print("\n❌ Testing invalid data:")
        invalid_config = {
            "name": "",  # Empty name should fail
            "role": "invalid_role",  # Invalid role
            "max_concurrent_tasks": -1  # Negative value should fail
        }
        validate_agent_data(invalid_config)
        
    except Exception as e:
        print(f"Expected validation error: {e}")
    
    # Export schemas
    print("\n📋 Model schemas generated successfully!")
    schemas = export_model_schemas()
    print(f"Generated schemas for {len(schemas)} models")