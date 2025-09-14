#!/usr/bin/env python3
"""
Pigeonhole Configuration Management
Centralized configuration handling with validation and environment support
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import logging

@dataclass
class BrandingConfig:
    """Branding configuration settings"""
    name: str = "PIGEONHOLE MEDIA CENTER"
    tagline: str = "Professional Streaming Solutions"
    primary_color: str = "#FF6B35"
    secondary_color: str = "#1E3A8A"
    accent_color: str = "#10B981"
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#B0B0B0"
    background: str = "#1A1A1A"

@dataclass
class PerformanceConfig:
    """Performance optimization settings"""
    buffer_factor: float = 4.0
    cache_size: int = 209715200  # 200MB default
    concurrent_streams: int = 3
    enable_hardware_acceleration: bool = True
    network_timeout: int = 30

@dataclass
class DeviceProfile:
    """Device-specific configuration profile"""
    name: str
    privacy_level: str = "medium"
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    enabled_services: List[str] = field(default_factory=list)
    disabled_services: List[str] = field(default_factory=list)
    restrictions: Dict[str, bool] = field(default_factory=dict)

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.logger = self._setup_logging()
        self._config_cache = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        # Check for environment variable first
        env_path = os.getenv('PIGEONHOLE_CONFIG')
        if env_path and os.path.exists(env_path):
            return env_path
        
        # Check common locations
        possible_paths = [
            "M:/pigeonhole_config.yaml",
            "./config/pigeonhole.yaml",
            os.path.expanduser("~/.pigeonhole/config.yaml")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Return default path
        return "M:/pigeonhole_config.yaml"
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('pigeonhole')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_config(self) -> None:
        """Load configuration from file with defaults"""
        default_config = self._get_default_config()
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    if self.config_path.endswith('.json'):
                        user_config = json.load(f)
                    else:
                        user_config = yaml.safe_load(f)
                
                # Deep merge user config with defaults
                self._config_cache = self._deep_merge(default_config, user_config or {})
                self.logger.info(f"Configuration loaded from {self.config_path}")
                
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                self._config_cache = default_config
        else:
            self.logger.warning(f"Config file not found: {self.config_path}, using defaults")
            self._config_cache = default_config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'branding': {
                'name': 'PIGEONHOLE MEDIA CENTER',
                'tagline': 'Professional Streaming Solutions',
                'primary_color': '#FF6B35',
                'secondary_color': '#1E3A8A',
                'accent_color': '#10B981',
                'text_primary': '#FFFFFF',
                'text_secondary': '#B0B0B0',
                'background': '#1A1A1A'
            },
            'device_profiles': {
                'corporate': {
                    'privacy_level': 'high',
                    'performance': {
                        'buffer_factor': 4.0,
                        'cache_size': 209715200,
                        'concurrent_streams': 3,
                        'enable_hardware_acceleration': True,
                        'network_timeout': 30
                    },
                    'disabled_services': ['webserver', 'airplay', 'upnp'],
                    'enabled_services': ['zeroconf'],
                    'restrictions': {
                        'corporate_branding': True,
                        'restricted_settings': True,
                        'enable_logging': False
                    }
                },
                'home': {
                    'privacy_level': 'medium',
                    'performance': {
                        'buffer_factor': 3.0,
                        'cache_size': 157286400,
                        'concurrent_streams': 2,
                        'enable_hardware_acceleration': True,
                        'network_timeout': 30
                    },
                    'enabled_services': ['webserver', 'zeroconf', 'airplay'],
                    'disabled_services': [],
                    'restrictions': {
                        'family_filters': True,
                        'easy_setup': True,
                        'enable_logging': True
                    }
                }
            },
            'streaming': {
                'essential_addons': [
                    'plugin.video.youtube',
                    'plugin.video.umbrella',
                    'plugin.video.thecrew',
                    'plugin.video.daddylive'
                ],
                'repositories': [
                    'repository.thecrew',
                    'repository.umbrella'
                ]
            },
            'deployment': {
                'adb_timeout': 30,
                'retry_attempts': 3,
                'parallel_deployments': True,
                'backup_existing': True
            }
        }
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_branding_config(self) -> BrandingConfig:
        """Get branding configuration as dataclass"""
        branding_dict = self._config_cache.get('branding', {})
        return BrandingConfig(**branding_dict)
    
    def get_device_profile(self, profile_name: str) -> Optional[DeviceProfile]:
        """Get device profile configuration"""
        profiles = self._config_cache.get('device_profiles', {})
        profile_data = profiles.get(profile_name)
        
        if not profile_data:
            self.logger.warning(f"Profile '{profile_name}' not found")
            return None
        
        # Convert performance dict to PerformanceConfig
        perf_data = profile_data.get('performance', {})
        performance = PerformanceConfig(**perf_data)
        
        return DeviceProfile(
            name=profile_name,
            privacy_level=profile_data.get('privacy_level', 'medium'),
            performance=performance,
            enabled_services=profile_data.get('enabled_services', []),
            disabled_services=profile_data.get('disabled_services', []),
            restrictions=profile_data.get('restrictions', {})
        )
    
    def get_streaming_config(self) -> Dict[str, Any]:
        """Get streaming configuration"""
        return self._config_cache.get('streaming', {})
    
    def get_deployment_config(self) -> Dict[str, Any]:
        """Get deployment configuration"""
        return self._config_cache.get('deployment', {})
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key with dot notation support"""
        keys = key.split('.')
        value = self._config_cache
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value by key with dot notation support"""
        keys = key.split('.')
        config = self._config_cache
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def save_config(self, path: Optional[str] = None) -> bool:
        """Save current configuration to file"""
        save_path = path or self.config_path
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config_cache, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Configuration saved to {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Validate branding colors
        branding = self._config_cache.get('branding', {})
        color_fields = ['primary_color', 'secondary_color', 'accent_color']
        
        for field in color_fields:
            color = branding.get(field, '')
            if not color.startswith('#') or len(color) != 7:
                issues.append(f"Invalid color format for branding.{field}: {color}")
        
        # Validate device profiles
        profiles = self._config_cache.get('device_profiles', {})
        for profile_name, profile_data in profiles.items():
            privacy_level = profile_data.get('privacy_level')
            if privacy_level not in ['low', 'medium', 'high']:
                issues.append(f"Invalid privacy_level in profile {profile_name}: {privacy_level}")
        
        return issues
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        self._load_config()

# Global configuration instance
config_manager = ConfigManager()

def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    return config_manager