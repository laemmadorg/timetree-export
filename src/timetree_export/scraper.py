"""Web scraper for TimeTree using Playwright."""

import logging
from typing import Optional

from playwright.sync_api import sync_playwright, Browser, Page, Playwright

logger = logging.getLogger(__name__)


class TimeTreeScraper:
    """Scraper for TimeTree web interface."""

    def __init__(self, headless: bool = True):
        """Initialize the scraper."""
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright: Optional[Playwright] = None

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def start(self):
        """Start the browser."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        logger.info("Browser started")

    def stop(self):
        """Stop the browser."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser stopped")

    def login(self, email: str, password: str) -> bool:
        """Login to TimeTree."""
        if not self.page:
            raise RuntimeError("Browser not started")

        self.page.goto("https://timetreeapp.com")
        
        # Fill in login form
        self.page.fill('input[type="email"]', email)
        self.page.fill('input[type="password"]', password)
        self.page.click('button[type="submit"]')
        
        # Wait for navigation
        self.page.wait_for_load_state("networkidle")
        
        # Check if login was successful
        if "dashboard" in self.page.url or "calendars" in self.page.url:
            logger.info("Login successful")
            return True
        
        logger.warning("Login may have failed")
        return False

    def scrape_calendars(self) -> list:
        """Scrape calendar list."""
        if not self.page:
            raise RuntimeError("Browser not started")
        
        # Navigate to calendars page
        self.page.goto("https://timetreeapp.com/calendars")
        self.page.wait_for_load_state("networkidle")
        
        # Extract calendar data
        calendars = []
        calendar_elements = self.page.query_selector_all('.calendar-item')
        
        for element in calendar_elements:
            name = element.query_selector('.calendar-name').inner_text()
            calendar_id = element.get_attribute('data-calendar-id')
            calendars.append({
                'id': calendar_id,
                'name': name
            })
        
        logger.info(f"Scraped {len(calendars)} calendars")
        return calendars

    def scrape_events(self, calendar_id: str) -> list:
        """Scrape events from a specific calendar."""
        if not self.page:
            raise RuntimeError("Browser not started")
        
        # Navigate to calendar view
        self.page.goto(f"https://timetreeapp.com/calendars/{calendar_id}")
        self.page.wait_for_load_state("networkidle")
        
        # Extract event data
        events = []
        event_elements = self.page.query_selector_all('.event-item')
        
        for element in event_elements:
            title = element.query_selector('.event-title').inner_text()
            start_time = element.get_attribute('data-start-time')
            end_time = element.get_attribute('data-end-time')
            
            events.append({
                'title': title,
                'start_time': start_time,
                'end_time': end_time
            })
        
        logger.info(f"Scraped {len(events)} events from calendar {calendar_id}")
        return events
