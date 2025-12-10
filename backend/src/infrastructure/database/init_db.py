#!/usr/bin/env python3
"""
Database initialization script.
This script can be run independently to create database tables.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.connection import init_database
from src.core.logger import setup_logger
import logging

def main():
    """Initialize the database tables"""
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting database initialization...")
        init_database()
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
