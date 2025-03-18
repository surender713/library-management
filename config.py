"""
Configuration settings for the Library Management System.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'library_management')
}

# Application settings
APP_NAME = "Library Management System"
VERSION = "1.0.0"
MAX_BOOKS_PER_USER = 3
DEFAULT_BORROW_DURATION_DAYS = 14 