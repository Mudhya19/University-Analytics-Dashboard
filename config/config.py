"""
Configuration module untuk University Dashboard
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    APP_TITLE = os.getenv("APP_TITLE", "University Analytics Dashboard")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
class DatabaseConfig:
    """Database configuration"""
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PATH = os.getenv("DB_PATH", "./database/university.db")
    
class StreamlitConfig:
    """Streamlit-specific configuration"""
    SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
    LOGGER_LEVEL = os.getenv("STREAMLIT_LOGGER_LEVEL", "info")

class DataConfig:
    """Data configuration"""
    DATA_SOURCE = os.getenv("DATA_SOURCE", "local")
    DATA_PATH = os.getenv("DATA_PATH", "./database/data")
