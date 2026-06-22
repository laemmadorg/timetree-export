"""Web scraper for TimeTree using Playwright."""

import logging
from typing import Optional

from playwright.sync_api import sync_playwright, Browser, Page, Playwright, TimeoutError as PlaywrightTimeoutError

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
        # Set a reasonable timeout
        self.page.set_default_timeout(60000)  # 60 seconds
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

        logger.info("Navigating to TimeTree login page...")
        self.page.goto("https://timetreeapp.com")
        
        # Wait for page to load
        self.page.wait_for_load_state("networkidle")
        
        # Try multiple selectors for email input
        email_selectors = [
            'input[type="email"]',
            'input[name="email"]',
            '#email',
            'input[autocomplete="email"]',
            'input[autocomplete="username"]',
            'input[id*="email"]',
            'input[name*="email"]',
        ]
        
        email_field = None
        for selector in email_selectors:
            try:
                email_field = self.page.query_selector(selector)
                if email_field:
                    logger.info(f"Found email field with selector: {selector}")
                    break
            except Exception:
                continue
        
        if not email_field:
            logger.error("Could not find email input field on login page")
            logger.info("Page HTML snapshot:")
            logger.info(self.page.content()[:2000])  # Log first 2000 chars of page
            return False
        
        # Try multiple selectors for password input
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            '#password',
            'input[autocomplete="current-password"]',
            'input[autocomplete="password"]',
            'input[id*="password"]',
            'input[name*="password"]',
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                password_field = self.page.query_selector(selector)
                if password_field:
                    logger.info(f"Found password field with selector: {selector}")
                    break
            except Exception:
                continue
        
        if not password_field:
            logger.error("Could not find password input field on login page")
            return False
        
        # Fill in login form
        logger.info("Filling login form...")
        email_field.fill(email)
        password_field.fill(password)
        
        # Try multiple selectors for submit button
        submit_selectors = [
            'button[type="submit"]',
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'button:has-text("Sign in")',
            'input[type="submit"]',
            '[type="submit"]',
        ]
        
        submit_button = None
        for selector in submit_selectors:
            try:
                submit_button = self.page.query_selector(selector)
                if submit_button:
                    logger.info(f"Found submit button with selector: {selector}")
                    break
            except Exception:
                continue
        
        if not submit_button:
            logger.error("Could not find submit button on login page")
            return False
        
        # Click submit and wait for navigation
        logger.info("Submitting login form...")
        with self.page.expect_navigation():
            submit_button.click()
        
        # Wait for navigation to complete
        try:
            self.page.wait_for_load_state("networkidle", timeout=60000)
        except PlaywrightTimeoutError:
            logger.warning("Page load timed out, continuing anyway")
        
        # Check if login was successful by looking for dashboard/calendar elements
        logger.info(f"Current URL: {self.page.url}")
        
        # Check for successful login indicators
        success_indicators = [
            "dashboard" in self.page.url,
            "calendars" in self.page.url,
            self.page.query_selector('.dashboard') is not None,
            self.page.query_selector('.calendar-list') is not None,
            self.page.query_selector('[data-testid="dashboard"]') is not None,
        ]
        
        if any(success_indicators):
            logger.info("Login successful")
            return True
        
        # Check for login error messages
        error_indicators = [
            self.page.query_selector('.error') is not None,
            self.page.query_selector('[role="alert"]') is not None,
            self.page.query_selector('text="Invalid"') is not None,
            self.page.query_selector('text="incorrect"') is not None,
        ]
        
        if any(error_indicators):
            logger.error("Login failed - invalid credentials or error on page")
            return False
        
        logger.warning("Login status unclear - page may have changed structure")
        logger.info("Page content sample:")
        logger.info(self.page.content()[:2000])
        return False

    def scrape_calendars(self) -> list:
        """Scrape calendar list."""
        if not self.page:
            raise RuntimeError("Browser not started")
        
        # Navigate to calendars page
        logger.info("Navigating to calendars page...")
        self.page.goto("https://timetreeapp.com/calendars")
        
        try:
            self.page.wait_for_load_state("networkidle", timeout=60000)
        except PlaywrightTimeoutError:
            logger.warning("Calendars page load timed out, continuing anyway")
        
        # Extract calendar data - try multiple selectors
        calendars = []
        calendar_selectors = [
            '.calendar-item',
            '.calendar-card',
            '[data-calendar-id]',
            '[data-testid="calendar"]',
            'a[href*="/calendars/"]',
        ]
        
        for selector in calendar_selectors:
            try:
                calendar_elements = self.page.query_selector_all(selector)
                if calendar_elements:
                    logger.info(f"Found {len(calendar_elements)} calendar elements with selector: {selector}")
                    break
            except Exception:
                continue
        else:
            logger.warning("No calendar elements found with any selector")
            calendar_elements = []
        
        for element in calendar_elements:
            # Try to extract name
            name = None
            name_selectors = [
                '.calendar-name',
                '.name',
                'h2',
                'h3',
                '[data-testid="calendar-name"]',
            ]
            for name_sel in name_selectors:
                try:
                    name_elem = element.query_selector(name_sel)
                    if name_elem:
                        name = name_elem.inner_text().strip()
                        break
                except Exception:
                    continue
            
            # Try to extract ID
            calendar_id = None
            id_selectors = [
                'data-calendar-id',
                'data-id',
                'data-testid',
            ]
            for id_attr in id_selectors:
                try:
                    calendar_id = element.get_attribute(id_attr)
                    if calendar_id:
                        break
                except Exception:
                    continue
            
            # If no ID from attributes, try href
            if not calendar_id:
                try:
                    href = element.get_attribute('href')
                    if href and '/calendars/' in href:
                        # Extract ID from URL
                        parts = href.split('/calendars/')
                        if len(parts) > 1:
                            calendar_id = parts[1].split('/')[0].split('?')[0]
                except Exception:
                    pass
            
            if name or calendar_id:
                calendars.append({
                    'id': calendar_id or 'unknown',
                    'name': name or 'Unnamed Calendar'
                })
        
        logger.info(f"Scraped {len(calendars)} calendars")
        return calendars

    def scrape_events(self, calendar_id: str) -> list:
        """Scrape events from a specific calendar."""
        if not self.page:
            raise RuntimeError("Browser not started")
        
        # Navigate to calendar view
        logger.info(f"Navigating to calendar {calendar_id}...")
        self.page.goto(f"https://timetreeapp.com/calendars/{calendar_id}")
        
        try:
            self.page.wait_for_load_state("networkidle", timeout=60000)
        except PlaywrightTimeoutError:
            logger.warning("Calendar page load timed out, continuing anyway")
        
        # Extract event data
        events = []
        event_selectors = [
            '.event-item',
            '.event-card',
            '[data-event-id]',
            '[data-testid="event"]',
        ]
        
        for selector in event_selectors:
            try:
                event_elements = self.page.query_selector_all(selector)
                if event_elements:
                    logger.info(f"Found {len(event_elements)} event elements with selector: {selector}")
                    break
            except Exception:
                continue
        else:
            logger.warning("No event elements found with any selector")
            event_elements = []
        
        for element in event_elements:
            # Try to extract title
            title = None
            title_selectors = [
                '.event-title',
                '.title',
                'h3',
                'h4',
                '[data-testid="event-title"]',
            ]
            for title_sel in title_selectors:
                try:
                    title_elem = element.query_selector(title_sel)
                    if title_elem:
                        title = title_elem.inner_text().strip()
                        break
                except Exception:
                    continue
            
            # Try to extract times
            start_time = element.get_attribute('data-start-time') or ''
            end_time = element.get_attribute('data-end-time') or ''
            
            # If no data attributes, try to extract from text
            if not start_time or not end_time:
                try:
                    time_elem = element.query_selector('.event-time')
                    if time_elem:
                        time_text = time_elem.inner_text()
                        # Simple parsing - this would need improvement
                        if ' - ' in time_text:
                            parts = time_text.split(' - ')
                            if len(parts) >= 2:
                                start_time = parts[0]
                                end_time = parts[1]
                except Exception:
                    pass
            
            events.append({
                'title': title or 'Untitled Event',
                'start_time': start_time,
                'end_time': end_time
            })
        
        logger.info(f"Scraped {len(events)} events from calendar {calendar_id}")
        return events
