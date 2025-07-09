"""
Configuration management for the Telegram bot.
Handles environment variables and settings.
"""

import os
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        self.load_config()
        self.validate_config()
    
    def load_config(self):
        """Load configuration from environment variables"""
        # Load .env file if it exists
        env_file = Path('.env')
        if env_file.exists():
            logger.info("Loading .env file...")
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#') and '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
                        logger.info(f"Loaded {key} from .env file")
        
        # Telegram API credentials
        self.API_ID = self.get_env_int('API_ID', 'TELEGRAM_API_ID')
        self.API_HASH = self.get_env_str('API_HASH', 'TELEGRAM_API_HASH')
        self.BOT_TOKEN = self.get_env_str('BOT_TOKEN', 'BOT_TOKENS', 'TELEGRAM_BOT_TOKEN')
        
        # Bot settings
        self.BOT_NAME = os.getenv('BOT_NAME', 'Telegram Bot')
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # Logging level
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Database settings (if needed)
        self.DATABASE_URL = os.getenv('DATABASE_URL', '')
        
        # Session settings
        self.SESSION_NAME = os.getenv('SESSION_NAME', 'telegram_bot')
        
        logger.info("Configuration loaded successfully")
    
    def get_env_str(self, *keys: str) -> Optional[str]:
        """Get string environment variable with multiple key options"""
        for key in keys:
            value = os.getenv(key)
            if value:
                # Если это список токенов, берем первый
                if key == 'BOT_TOKENS' and ',' in value:
                    return value.split(',')[0].strip()
                return value
        return None
    
    def get_env_int(self, *keys: str) -> Optional[int]:
        """Get integer environment variable with multiple key options"""
        for key in keys:
            value = os.getenv(key)
            if value:
                try:
                    return int(value)
                except ValueError:
                    logger.warning(f"Invalid integer value for {key}: {value}")
        return None
    
    def validate_config(self):
        """Validate required configuration values"""
        errors = []
        
        if not self.API_ID:
            errors.append("API_ID is required")
        
        if not self.API_HASH:
            errors.append("API_HASH is required")
        
        if not self.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")
        
        if errors:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            raise ValueError("Required configuration values are missing")
        
        logger.info("Configuration validation passed")
    
    def get_session_path(self) -> str:
        """Get the session file path"""
        return f"{self.SESSION_NAME}.session"
    
    def __str__(self) -> str:
        """String representation of config (without sensitive data)"""
        return f"Config(API_ID={self.API_ID}, BOT_NAME={self.BOT_NAME}, DEBUG={self.DEBUG})"
