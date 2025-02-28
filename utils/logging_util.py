# File: /utils/logging_util.py
# Logging utility for Sentigee

import os
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name, log_file=None, level=logging.INFO):
    """Set up a logger that writes to both console and file if specified.
    
    Args:
        name (str): Logger name
        log_file (str, optional): Path to log file. Defaults to None.
        level (int, optional): Logging level. Defaults to logging.INFO.
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    simple_formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        # Ensure directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        # Create rotating file handler (10MB max file size, keep last 5 files)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_mail_relay_logger():
    """Get logger for mail relay operations"""
    log_file = os.path.join('opt', 'sentigee', 'logs', 'mail_relay.log')
    return setup_logger('mail_relay', log_file)

def get_system_logger():
    """Get logger for system operations"""
    log_file = os.path.join('opt', 'sentigee', 'logs', 'system.log')
    return setup_logger('system', log_file)

def get_admin_logger():
    """Get logger for admin operations"""
    log_file = os.path.join('opt', 'sentigee', 'logs', 'admin.log')
    return setup_logger('admin', log_file)

def get_auth_logger():
    """Get logger for authentication operations"""
    log_file = os.path.join('opt', 'sentigee', 'logs', 'auth.log')
    return setup_logger('auth', log_file)

def get_api_logger():
    """Get logger for API operations"""
    log_file = os.path.join('opt', 'sentigee', 'logs', 'api.log')
    return setup_logger('api', log_file)

def get_feature_logger(feature_name):
    """Get logger for a specific feature"""
    log_file = os.path.join('opt', 'sentigee', 'logs', f'{feature_name}.log')
    return setup_logger(f'feature_{feature_name}', log_file)
