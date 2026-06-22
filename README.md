# TimeTree Export

**Export your TimeTree calendar data to CSV, JSON, and iCalendar formats.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

TimeTree Export is a command-line tool that allows you to export your calendar data from [TimeTree](https://timetreeapp.com) — a popular shared calendar application. Whether you want to back up your events, migrate to another calendar service, or analyze your schedule data, this tool provides an easy way to extract your TimeTree information.

### Features

- ✅ Export calendars and events from your TimeTree account
- ✅ Multiple output formats: **CSV**, **JSON**, and **iCalendar (ICS)**
- ✅ Export all calendars or filter by specific calendar ID
- ✅ Configurable date ranges for targeted exports
- ✅ Web scraping support using Playwright
- ✅ API-based export (when authentication tokens are available)
- ✅ Flexible configuration via YAML file

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

1. Clone this repository:
   ```bash
   git clone https://github.com/laemmadorg/timetree-export.git
   cd timetree-export
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers (required for web scraping):
   ```bash
   playwright install
   ```

## Quick Start

### 1. Configure Your Settings

Copy the example configuration file and edit it with your credentials:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` with your TimeTree account information:

```yaml
# TimeTree Export Configuration
authentication:
  email: "your_email@example.com"
  password: "your_password"
  csrf_token: ""  # Optional - for API access
  session_cookie: ""  # Optional - for API access

export:
  output_directory: "./output"
  formats:
    - csv
    - json
    - ical
  start_date: "2024-01-01"
  end_date: "2024-12-31"
  calendars: []  # Leave empty for all, or specify calendar IDs

scraper:
  headless: true  # Run browser in background
  timeout: 30000  # Page load timeout in milliseconds
```

### 2. Run the Export

Execute the main script:

```bash
python main.py
```

This will:
- Log in to your TimeTree account
- Scrape your calendar data
- Export events to CSV, JSON, and iCalendar files in the `./output` directory

### 3. Using the CLI

You can also use the command-line interface directly:

```bash
# Basic export with all formats
python -m src.timetree_export.cli

# Export to specific format
python -m src.timetree_export.cli --format csv
python -m src.timetree_export.cli --format json
python -m src.timetree_export.cli --format ical

# Export specific calendar
python -m src.timetree_export.cli --calendar YOUR_CALENDAR_ID

# Custom output directory
python -m src.timetree_export.cli --output ./my_exports

# Use custom config file
python -m src.timetree_export.cli --config my_config.yaml

# Verbose logging
python -m src.timetree_export.cli --verbose

# Combine options
python -m src.timetree_export.cli --format csv --calendar cal_123 --output ./backup
```

## CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output`, `-o` | Output directory for exported files | `./output` |
| `--format`, `-f` | Export format: csv, json, ical, or all | `all` |
| `--calendar`, `-c` | Specific calendar ID to export | All calendars |
| `--config` | Path to configuration file | `config.yaml` |
| `--verbose`, `-v` | Enable verbose logging | Disabled |

## Output Formats

### CSV Export

Creates a spreadsheet-compatible file with event data:

- **Filename**: `{calendar_name}_events.csv` or `all_events.csv`
- **Columns**: id, title, calendar_id, start_time, end_time, description, location, is_all_day

Example output:
```csv
id,title,calendar_id,start_time,end_time,description,location,is_all_day
abc123,Team Meeting,cal_456,2024-01-15T10:00:00,2024-01-15T11:00:00,Quarterly planning,,False
```

### JSON Export

Creates a structured JSON file with complete data:

- **Filename**: `timetree_export.json`
- **Includes**: Calendars, events, users, and export timestamp

Example structure:
```json
{
  "calendars": [
    {
      "id": "cal_456",
      "name": "Work Calendar",
      "color": "#FF5733",
      "owner_id": "user_789",
      "is_public": false,
      "description": "Team work calendar"
    }
  ],
  "events": [
    {
      "id": "abc123",
      "title": "Team Meeting",
      "calendar_id": "cal_456",
      "start_time": "2024-01-15T10:00:00",
      "end_time": "2024-01-15T11:00:00",
      "description": "Quarterly planning",
      "location": "",
      "attendees": ["user_789"],
      "is_all_day": false
    }
  ],
  "users": [...],
  "exported_at": "2024-01-20T12:00:00"
}
```

### iCalendar (ICS) Export

Creates a standard iCalendar file compatible with most calendar applications:

- **Filename**: `timetree_export.ics`
- **Format**: RFC 5545 compliant
- **Compatible with**: Google Calendar, Outlook, Apple Calendar, etc.

## How It Works

TimeTree Export uses two methods to access your data:

### 1. Web Scraping (Default)

Uses [Playwright](https://playwright.dev/) to automate a real browser session:
- Logs in to TimeTree with your credentials
- Navigates to your calendars and events
- Extracts data from the web interface
- Works even if the API changes

### 2. API Access (Optional)

Directly accesses TimeTree's API for faster, more reliable exports:
- Requires CSRF token and session cookie
- Faster than web scraping
- More reliable for large datasets
- See `REVERSE_ENGINEERING.md` for API details

## Configuration Reference

### Authentication Settings

| Setting | Required | Description |
|---------|----------|-------------|
| `email` | Yes | Your TimeTree account email |
| `password` | Yes | Your TimeTree account password |
| `csrf_token` | No | CSRF token for API access (from web session) |
| `session_cookie` | No | Session cookie for API access |

### Export Settings

| Setting | Required | Description |
|---------|----------|-------------|
| `output_directory` | No | Where to save exported files |
| `formats` | No | List of formats to export (csv, json, ical) |
| `start_date` | No | Start date for export (ISO format: YYYY-MM-DD) |
| `end_date` | No | End date for export (ISO format: YYYY-MM-DD) |
| `calendars` | No | Array of calendar IDs to export (empty = all) |

### Scraper Settings

| Setting | Required | Description |
|---------|----------|-------------|
| `headless` | No | Run browser invisibly (true/false) |
| `timeout` | No | Page load timeout in milliseconds |
| `login_confirmation_selector` | No | CSS selector to confirm successful login |

### API Settings

| Setting | Required | Description |
|---------|----------|-------------|
| `base_url` | No | TimeTree API base URL |
| `rate_limit_delay` | No | Delay between API requests in milliseconds |

## Examples

### Export Last 30 Days of Events

```yaml
# config.yaml
export:
  start_date: "2024-01-01"
  end_date: "2024-01-31"
  formats:
    - csv
    - json
```

### Export Only Work Calendar

```yaml
# config.yaml
export:
  calendars:
    - cal_work_123
  formats:
    - ical
```

### Export with Visible Browser

```yaml
# config.yaml
scraper:
  headless: false
```

## Troubleshooting

### Login Issues

- **Problem**: Login fails or times out
- **Solution**: 
  - Verify your email and password are correct
  - Check if TimeTree has changed their login page structure
  - Try setting `headless: false` to see the browser in action
  - Increase the `timeout` value in scraper settings

### No Data Exported

- **Problem**: Output files are empty or contain no events
- **Solution**:
  - Verify login was successful (check logs)
  - Ensure you have events in the specified date range
  - Try exporting without date range filters
  - Check if calendar IDs in config are correct

### Playwright Browser Issues

- **Problem**: Browser fails to start
- **Solution**:
  - Run `playwright install` to install required browsers
  - Ensure you have sufficient disk space
  - Check for missing system dependencies (on Linux)

### Rate Limiting

- **Problem**: Getting blocked or rate limited
- **Solution**:
  - Increase `rate_limit_delay` in API settings
  - Use web scraping with longer timeouts
  - Avoid running frequent exports
  - Respect TimeTree's terms of service

## Data Model

### Calendar

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique calendar identifier |
| `name` | string | Calendar display name |
| `color` | string | Hex color code (e.g., `#FF5733`) |
| `owner_id` | string | User ID of calendar owner |
| `is_public` | boolean | Whether calendar is publicly accessible |
| `description` | string | Calendar description (optional) |

### Event

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique event identifier |
| `title` | string | Event title |
| `calendar_id` | string | ID of parent calendar |
| `start_time` | datetime | Event start time (ISO 8601) |
| `end_time` | datetime | Event end time (ISO 8601) |
| `description` | string | Event description (optional) |
| `location` | string | Event location (optional) |
| `attendees` | array | List of user IDs attending |
| `is_all_day` | boolean | Whether event spans all day |

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy icalendar
   ```
4. Run tests:
   ```bash
   pytest tests/
   ```
5. Run linting:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/ tests/
   ```

## Legal Notice

- This tool is for **personal use only**
- Respect [TimeTree's Terms of Service](https://timetreeapp.com/terms)
- Do not use this tool to scrape data you don't have permission to access
- Do not overload TimeTree's servers with excessive requests
- Use at your own risk

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation framework
- [Pydantic](https://pydantic.dev/) - Data validation and settings management
- [TimeTree](https://timetreeapp.com) - The calendar service this tool exports from

---

**Questions or Issues?**

Please open an issue on [GitHub Issues](https://github.com/laemmadorg/timetree-export/issues) for bug reports, feature requests, or questions.
