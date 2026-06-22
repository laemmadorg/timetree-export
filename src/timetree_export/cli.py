"""Command line interface for TimeTree Export."""

import argparse
import logging
import sys
from pathlib import Path

from .models import ExportData
from .exporter import TimeTreeExporter

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Export TimeTree calendar data to various formats"
    )
    
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


def main():
    """Main CLI entry point."""
    args = parse_args()
    setup_logging(args.verbose)
    
    logger.info("Starting TimeTree Export CLI")
    
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
