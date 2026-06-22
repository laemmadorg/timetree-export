"""Tests for data models."""

from datetime import datetime
from src.timetree_export.models import Calendar, Event, User, ExportData


def test_calendar_creation():
    """Test Calendar model creation."""
    calendar = Calendar(
        id="cal_123",
        name="Work Calendar",
        color="#FF5733",
        owner_id="user_456"
    )
    assert calendar.id == "cal_123"
    assert calendar.name == "Work Calendar"
    assert calendar.color == "#FF5733"
    assert calendar.owner_id == "user_456"
    assert calendar.is_public is False


def test_event_creation():
    """Test Event model creation."""
    start_time = datetime(2024, 1, 15, 10, 0, 0)
    end_time = datetime(2024, 1, 15, 11, 0, 0)
    
    event = Event(
        id="evt_789",
        title="Team Meeting",
        calendar_id="cal_123",
        start_time=start_time,
        end_time=end_time,
        description="Weekly team sync",
        location="Conference Room A"
    )
    assert event.id == "evt_789"
    assert event.title == "Team Meeting"
    assert event.calendar_id == "cal_123"
    assert event.start_time == start_time
    assert event.end_time == end_time
    assert event.description == "Weekly team sync"
    assert event.location == "Conference Room A"


def test_user_creation():
    """Test User model creation."""
    user = User(
        id="user_456",
        name="John Doe",
        email="john@example.com",
        avatar_url="https://example.com/avatar.jpg"
    )
    assert user.id == "user_456"
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.avatar_url == "https://example.com/avatar.jpg"


def test_export_data_creation():
    """Test ExportData container."""
    export_data = ExportData()
    assert len(export_data.calendars) == 0
    assert len(export_data.events) == 0
    assert len(export_data.users) == 0
    
    calendar = Calendar(id="cal_1", name="Test", color="#000000", owner_id="user_1")
    export_data.calendars.append(calendar)
    assert len(export_data.calendars) == 1
