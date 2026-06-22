"""Direct API client for TimeTree."""

import logging
from typing import Optional, Dict, Any

import requests

logger = logging.getLogger(__name__)


class TimeTreeAPIClient:
    """Client for TimeTree API."""

    BASE_URL = "https://timetreeapp.com/api/v1"

    def __init__(self, csrf_token: Optional[str] = None, session_cookie: Optional[str] = None):
        """Initialize the API client."""
        self.csrf_token = csrf_token
        self.session_cookie = session_cookie
        self.session = requests.Session()
        
        if session_cookie:
            self.session.cookies.set('_timetree_session', session_cookie)
        
        self.session.headers.update({
            'X-CSRF-Token': csrf_token or '',
            'Content-Type': 'application/json',
            'User-Agent': 'TimeTreeExport/0.1.0'
        })

    def get_calendars(self) -> Dict[str, Any]:
        """Get all calendars for the authenticated user."""
        response = self.session.get(f"{self.BASE_URL}/calendars")
        response.raise_for_status()
        return response.json()

    def get_calendar_events(self, calendar_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get events for a specific calendar within a date range."""
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        response = self.session.get(
            f"{self.BASE_URL}/calendars/{calendar_id}/events",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_event_details(self, event_id: str) -> Dict[str, Any]:
        """Get details for a specific event."""
        response = self.session.get(f"{self.BASE_URL}/events/{event_id}")
        response.raise_for_status()
        return response.json()

    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information."""
        response = self.session.get(f"{self.BASE_URL}/me")
        response.raise_for_status()
        return response.json()

    def set_csrf_token(self, csrf_token: str):
        """Set the CSRF token for subsequent requests."""
        self.csrf_token = csrf_token
        self.session.headers.update({'X-CSRF-Token': csrf_token})
