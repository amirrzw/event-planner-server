# tasks/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure the directory exists
log_directory = os.path.dirname(__file__)
log_file = os.path.join(log_directory, 'task_logs.txt')

# Create a custom logger
logger = logging.getLogger('tasks')

# Set the log level
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)

# Set the log level for handlers
file_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(file_handler)
