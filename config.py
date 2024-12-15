import os

# Centralized configuration for MySQL credentials
class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')  # Default to 'localhost' if env var not set
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'BuK0uSk1971')
    MYSQL_DB = os.getenv('MYSQL_DB', 'craftastic')
