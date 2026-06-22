"""Command line interface for TimeTree Export."""

import argparse
import logging
import sys
from pathlib import Path

from .models import ExportData
from .exporter import TimeTreeExporter
from .scraper import TimeTreeScraper

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Export TimeTree calendar data to various formats"
    )
    
    # Authentication arguments
    parser.add_argument(
        '--email', '-e',
        type=str,
        default=None,
        help='TimeTree account email (overrides config file)'
    )
    
    parser.add_argument(
        '--password', '-p',
        type=str,
        default=None,
        help='TimeTree account password (overrides config file)'
    )
    
    # Action arguments
    parser.add_argument(
        '--list-calendars',
        action='store_true',
        help='List available calendars and exit (requires --email and --password)'
    )
    
    # Export arguments
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./output',
        help='Output directory for exported files'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'json', 'ical', 'all'],
        default='all',
        help='Export format (default: all)'
    )
    
    parser.add_argument(
        '--calendar', '-c',
        type=str,
        help='Specific calendar ID to export (default: all calendars)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def setup_logging(verbose: bool):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_config(config_path: str, email: str = None, password: str = None) -> dict:
    """Load configuration from file and override with CLI arguments."""
    import yaml
    from pathlib import Path
    
    config = {}
    
    # Try to load from config file
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f) or {}
    
    # Override with CLI arguments if provided
    if email:
        if 'authentication' not in config:
            config['authentication'] = {}
        config['authentication']['email'] = email
    
    if password:
        if 'authentication' not in config:
            config['authentication'] = {}
        config['authentication']['password'] = password
    
    return config


def list_calendars(email: str, password: str, headless: bool = True) -> list:
    """List available calendars for the given credentials."""
    with TimeTreeScraper(headless=headless) as scraper:
        if not scraper.login(email, password):
            logger.error("Login failed. Please check your credentials.")
            sys.exit(1)
        
        calendars = scraper.scrape_calendars()
        return calendars


def main():
    """Main CLI entry point."""
    args = parse_args()
    setup_logging(args.verbose)
    
    logger.info("Starting TimeTree Export CLI")
    
    # Handle --list-calendars mode
    if args.list_calendars:
        if not args.email or not args.password:
            logger.error("--list-calendars requires --email and --password")
            sys.exit(1)
        
        calendars = list_calendars(args.email, args.password, headless=not args.verbose)
        
        print("\nAvailable Calendars:")
        print("-" * 50)
        for cal in calendars:
            print(f"  ID: {cal.get('id', 'N/A')}")
            print(f"  Name: {cal.get('name', 'N/A')}")
            print()
        
        logger.info(f"Found {len(calendars)} calendars")
        sys.exit(0)
    
    # Load configuration
    config = load_config(args.config, args.email, args.password)
    
    # Validate we have credentials
    email = config.get('authentication', {}).get('email')
    password = config.get('authentication', {}).get('password')
    
    if not email or not password:
        logger.error("Email and password are required. Provide via --email/--password or config file.")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # For now, create sample data (will be replaced with real data from scraper/API)
    sample_data = ExportData()
    
    # Export based on format
    exporter = TimeTreeExporter()
    
    if args.format in ['csv', 'all']:
        exporter.export_to_csv(
            sample_data,
            output_path,
            args.calendar
        )
    
    if args.format in ['json', 'all']:
        exporter.export_to_json(sample_data, output_path)
    
    if args.format in ['ical', 'all']:
        exporter.export_to_ical(sample_data, output_path)
    
    logger.info(f"Export completed. Files saved to: {output_path.absolute()}")


if __name__ == "__main__":
    sys.exit(main())
