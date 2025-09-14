#!/usr/bin/env python3
"""
Pigeonhole Logging Configuration
Centralized logging setup with multiple handlers and formatters
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if hasattr(record, 'levelname') and record.levelname in self.COLORS:
            colored_levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
            )
            record.levelname = colored_levelname
        
        return super().format(record)

class PigeonholeLogger:
    """Centralized logging manager for Pigeonhole applications"""
    
    def __init__(self, log_dir: str = "M:/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler for all logs
        log_file = self.log_dir / f"pigeonhole_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Error file handler for errors only
        error_file = self.log_dir / f"pigeonhole_errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,   # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        # Add handlers to root logger
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
        
        # Set specific logger levels
        logging.getLogger('PIL').setLevel(logging.WARNING)  # Reduce PIL verbosity
        logging.getLogger('urllib3').setLevel(logging.WARNING)  # Reduce requests verbosity
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger with the specified name"""
        return logging.getLogger(name)
    
    def set_level(self, level: str) -> None:
        """Set global logging level"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_map:
            logging.getLogger().setLevel(level_map[level.upper()])
        else:
            raise ValueError(f"Invalid log level: {level}")
    
    def enable_debug(self) -> None:
        """Enable debug logging"""
        self.set_level('DEBUG')
        
        # Update console handler to show debug messages
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                handler.setLevel(logging.DEBUG)
    
    def disable_console(self) -> None:
        """Disable console logging (file only)"""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                root_logger.removeHandler(handler)
    
    def log_system_info(self):
        """Log system information for debugging"""
        logger = self.get_logger('pigeonhole.system')
        
        logger.info("=== Pigeonhole System Information ===")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Platform: {sys.platform}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Log directory: {self.log_dir}")
        
        # Log environment variables (filtered)
        env_vars = ['PATH', 'PIGEONHOLE_CONFIG', 'PYTHONPATH']
        for var in env_vars:
            value = os.getenv(var, 'Not set')
            logger.debug(f"Environment {var}: {value}")

# Global logger instance
_logger_instance: Optional[PigeonholeLogger] = None

def setup_logging(log_dir: str = "M:/logs", debug: bool = False) -> PigeonholeLogger:
    """Setup global logging configuration"""
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = PigeonholeLogger(log_dir)
        
        if debug:
            _logger_instance.enable_debug()
        
        # Log system info on first setup
        _logger_instance.log_system_info()
    
    return _logger_instance

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance (sets up logging if not already done)"""
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = setup_logging()
    
    return _logger_instance.get_logger(name)

# Convenience functions
def log_error(message: str, logger_name: str = 'pigeonhole'):
    """Log an error message"""
    get_logger(logger_name).error(message)

def log_warning(message: str, logger_name: str = 'pigeonhole'):
    """Log a warning message"""
    get_logger(logger_name).warning(message)

def log_info(message: str, logger_name: str = 'pigeonhole'):
    """Log an info message"""
    get_logger(logger_name).info(message)

def log_debug(message: str, logger_name: str = 'pigeonhole'):
    """Log a debug message"""
    get_logger(logger_name).debug(message)