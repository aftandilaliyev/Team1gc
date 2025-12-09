from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.shared.config.cfg import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# SQLAlchemy setup with MySQL
SQLALCHEMY_DATABASE_URL = settings.get_database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """Create all tables in the database"""
    try:
        # Import all models to ensure they are registered with Base
        from src.shared.models.user import User
        from src.shared.models.product import Product, ProductImage
        from src.shared.models.order import Order, OrderItem, CartItem
        from src.shared.models.payments import Customer
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def init_database():
    """Initialize the database with tables and any initial data"""
    create_tables()
    
    # You can add initial data seeding here if needed
    # For example:
    # seed_initial_data()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
