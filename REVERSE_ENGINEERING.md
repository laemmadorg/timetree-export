# TimeTree Reverse Engineering Notes

## Overview

This document contains notes on reverse engineering the TimeTree API and web interface for the purpose of exporting calendar data.

## API Endpoints

### Authentication
- **Login**: `POST /api/v1/sessions`
  - Requires: `email`, `password`
  - Returns: Session cookie, CSRF token

### Calendars
- **List calendars**: `GET /api/v1/calendars`
  - Returns: Array of calendar objects
  - Each calendar has: `id`, `name`, `color`, `owner_id`, `is_public`

- **Get calendar**: `GET /api/v1/calendars/{id}`
  - Returns: Single calendar object with details

### Events
- **List events**: `GET /api/v1/calendars/{calendar_id}/events`
  - Parameters: `start_date`, `end_date` (ISO format: YYYY-MM-DD)
  - Returns: Array of event objects

- **Get event**: `GET /api/v1/events/{id}`
  - Returns: Single event object with full details

- **Create event**: `POST /api/v1/calendars/{calendar_id}/events`
  - Requires: CSRF token in headers
  - Body: Event data

### Users
- **Current user**: `GET /api/v1/me`
  - Returns: Authenticated user information

## Request Headers

All API requests require:
```
X-CSRF-Token: <csrf_token>
Cookie: _timetree_session=<session_cookie>
Content-Type: application/json
```

## Response Formats

### Calendar Object
```json
{
  "id": "string",
  "name": "string",
  "color": "#hexcolor",
  "owner_id": "string",
  "is_public": true,
  "description": "string or null",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### Event Object
```json
{
  "id": "string",
  "title": "string",
  "calendar_id": "string",
  "start_time": "ISO8601",
  "end_time": "ISO8601",
  "description": "string or null",
  "location": "string or null",
  "is_all_day": true,
  "attendees": ["user_id"],
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

## Web Interface

### DOM Structure

#### Calendar List
- Container: `.calendar-list` or `#calendars`
- Calendar items: `.calendar-item`
- Calendar name: `.calendar-name`
- Calendar ID: `data-calendar-id` attribute

#### Event List
- Container: `.event-list` or `.calendar-view`
- Event items: `.event-item` or `.event-card`
- Event title: `.event-title`
- Event time: `.event-time`
- Event ID: `data-event-id` attribute

#### Login Form
- Email input: `input[type="email"]` or `#email`
- Password input: `input[type="password"]` or `#password`
- Submit button: `button[type="submit"]`

## Authentication Flow

1. User submits email and password via login form
2. Server responds with:
   - `_timetree_session` cookie
   - CSRF token in response headers or body
3. Subsequent requests must include both cookie and CSRF token

## Rate Limiting

- TimeTree appears to have rate limiting
- Recommended: Add delay between requests (100-200ms)
- Too many requests may result in 429 or temporary ban

## Notes

- The API uses standard REST conventions
- All dates are in ISO 8601 format (UTC)
- Calendar colors are hex codes (e.g., "#FF5733")
- Event times include timezone information
- All-day events have `is_all_day: true` and may have date-only timestamps

## HAR File Analysis

The included `timetreeapp.com_Archive.har` file contains captured network requests that can be analyzed to understand:
- Exact request/response formats
- Headers used
- API endpoint URLs
- Authentication flow

Use tools like:
- HAR Viewer (https://toolbox.googleapps.com/apps/har_analyzer/)
- Postman (import HAR)
- Custom scripts to parse HAR JSON

## Legal Considerations

- Respect TimeTree's terms of service
- Do not overload their servers
- Use this for personal data export only
- Do not redistribute exported data without permission
