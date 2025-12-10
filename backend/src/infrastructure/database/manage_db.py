#!/usr/bin/env python3
"""
Database management utilities.
Provides commands for creating, dropping, and resetting database tables.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.connection import engine, Base, create_tables
from src.core.logger import setup_logger
import logging

def create_all_tables():
    """Create all database tables"""
    logger = logging.getLogger(__name__)
    try:
        logger.info("Creating all database tables...")
        create_tables()
        logger.info("All tables created successfully!")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise

def drop_all_tables():
    """Drop all database tables"""
    logger = logging.getLogger(__name__)
    try:
        logger.warning("Dropping all database tables...")
        
        # Import all models to ensure they are registered
        from src.shared.models.user import User
        from src.shared.models.product import Product, ProductImage
        from src.shared.models.order import Order, OrderItem, CartItem
        from src.shared.models.payments import Customer
        
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully!")
    except Exception as e:
        logger.error(f"Failed to drop tables: {e}")
        raise

def reset_database():
    """Drop and recreate all database tables"""
    logger = logging.getLogger(__name__)
    logger.warning("Resetting database - this will delete all data!")
    
    drop_all_tables()
    create_all_tables()
    
    logger.info("Database reset completed!")

def check_tables():
    """Check which tables exist in the database"""
    logger = logging.getLogger(__name__)
    
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            logger.info(f"Found {len(tables)} tables in database:")
            for table in sorted(tables):
                logger.info(f"  - {table}")
        else:
            logger.info("No tables found in database")
            
    except Exception as e:
        logger.error(f"Failed to check tables: {e}")
        raise

def main():
    """Main function to handle command line arguments"""
    setup_logger()
    
    parser = argparse.ArgumentParser(description="Database management utilities")
    parser.add_argument(
        "command",
        choices=["create", "drop", "reset", "check"],
        help="Command to execute"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force execution without confirmation (for drop/reset commands)"
    )
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_all_tables()
        
    elif args.command == "drop":
        if not args.force:
            confirm = input("This will delete all tables and data. Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                print("Operation cancelled.")
                return
        drop_all_tables()
        
    elif args.command == "reset":
        if not args.force:
            confirm = input("This will delete all tables and data, then recreate them. Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                print("Operation cancelled.")
                return
        reset_database()
        
    elif args.command == "check":
        check_tables()

if __name__ == "__main__":
    main()
