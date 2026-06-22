"""Data models for TimeTree export."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Calendar:
    """Represents a TimeTree calendar."""
    id: str
    name: str
    color: str
    owner_id: str
    is_public: bool = False
    description: Optional[str] = None


@dataclass
class Event:
    """Represents a TimeTree event."""
    id: str
    title: str
    calendar_id: str
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    location: Optional[str] = None
    attendees: List[str] = field(default_factory=list)
    is_all_day: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class User:
    """Represents a TimeTree user."""
    id: str
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None


@dataclass
class ExportData:
    """Container for exported data."""
    calendars: List[Calendar] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    users: List[User] = field(default_factory=list)
