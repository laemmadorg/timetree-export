#!/usr/bin/env python3
"""Timetree Export - Main entry point for exporting TimeTree data."""

import logging
from pathlib import Path

from src.timetree_export.cli import main as cli_main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    logger.info("Starting TimeTree Export")
    cli_main()


if __name__ == "__main__":
    main()
