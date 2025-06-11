# client/config/yaml_config_adapter.py
"""
Adaptador de configuración que lee desde config/production.yaml
en lugar del config.ini eliminado.
Mantiene compatibilidad con el código existente del cliente.
"""

import os
import yaml
import logging
from pathlib import Path

logger = logging.getLogger('yaml_config_adapter')

class YamlConfigAdapter:
    """
    Adaptador que emula ConfigParser pero lee desde YAML.
    Permite migrar desde config.ini a production.yaml sin cambiar todo el código.
    """
    
    def __init__(self, yaml_path=None):
        if yaml_path is None:
            # Buscar config/production.yaml desde la raíz del proyecto
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            yaml_path = project_root / 'config' / 'production.yaml'
        
        self.yaml_path = Path(yaml_path)
        self.config_data = {}
        self._load_yaml_config()
    
    def _load_yaml_config(self):
        """Carga la configuración desde el archivo YAML"""
        try:
            if self.yaml_path.exists():
                with open(self.yaml_path, 'r', encoding='utf-8') as f:
                    self.config_data = yaml.safe_load(f) or {}
                logger.info(f"Configuración YAML cargada desde: {self.yaml_path}")
            else:
                logger.error(f"Archivo YAML no encontrado: {self.yaml_path}")
                self.config_data = {}
        except Exception as e:
            logger.error(f"Error cargando configuración YAML: {e}")
            self.config_data = {}
    
    def get(self, section, key, fallback=None):
        """
        Obtiene un valor de configuración emulando ConfigParser.get()
        """
        try:
            # Mapear secciones de config.ini a estructura YAML
            section_mapping = {
                'SERVER': self._get_server_config,
                'DEVICE': self._get_device_config,
                'CONNECTION': self._get_connection_config,
                'STORAGE': self._get_storage_config,
                'SYNC': self._get_sync_config
            }
            
            if section in section_mapping:
                return section_mapping[section](key, fallback)
            else:
                logger.warning(f"Sección no mapeada: {section}")
                return fallback
                
        except Exception as e:
            logger.error(f"Error obteniendo {section}.{key}: {e}")
            return fallback
    
    def _get_server_config(self, key, fallback):
        """Mapea configuración de SERVER desde YAML"""
        sync_config = self.config_data.get('sync', {})
        
        mapping = {
            'api_url': sync_config.get('server_url', ''),
            'auth_endpoint': sync_config.get('auth_endpoint', '/auth/authenticate'),
            'events_endpoint': sync_config.get('events_endpoint', '/events/create'),
            'sync_batch_endpoint': sync_config.get('sync_batch_endpoint', '/sync/batch'),
            'sync_status_endpoint': sync_config.get('sync_status_endpoint', '/sync/status'),
            'sync_confirm_endpoint': sync_config.get('sync_confirm_endpoint', '/sync/confirm'),
            'upload_image_endpoint': sync_config.get('upload_image_endpoint', '/events/upload_image')
        }
        
        # Construir URL completa para api_url
        if key == 'api_url' and 'server_url' in sync_config:
            base_url = sync_config['server_url'].rstrip('/')
            return f"{base_url}/server/api/v1"
        
        return mapping.get(key, fallback)
    
    def _get_device_config(self, key, fallback):
        """Mapea configuración de DEVICE desde YAML (solo desde sección sync)"""
        # Todo viene de la sección sync (no hay duplicación)
        sync_config = self.config_data.get('sync', {})
        
        mapping = {
            'device_id': sync_config.get('device_id'),
            'api_key': sync_config.get('api_key'),
            'device_type': sync_config.get('device_type', 'raspberry_pi_5')
        }
        
        return mapping.get(key, fallback)
    
    def _get_connection_config(self, key, fallback):
        """Mapea configuración de CONNECTION desde YAML"""
        connection_config = self.config_data.get('connection', {})
        
        mapping = {
            'check_interval': connection_config.get('check_interval', 30),
            'retry_attempts': connection_config.get('retry_attempts', 3),
            'retry_delay': connection_config.get('retry_delay', 5)
        }
        
        return mapping.get(key, fallback)
    
    def _get_storage_config(self, key, fallback):
        """Mapea configuración de STORAGE desde YAML"""
        storage_config = self.config_data.get('storage', {})
        
        mapping = {
            'db_path': storage_config.get('db_path', 'client/db/local.db'),
            'max_stored_events': storage_config.get('max_stored_events', 1000),
            'max_stored_images': storage_config.get('max_stored_images', 100),
            'image_storage_path': storage_config.get('image_storage_path', 'client/images/')
        }
        
        return mapping.get(key, fallback)
    
    def _get_sync_config(self, key, fallback):
        """Mapea configuración de SYNC desde YAML"""
        sync_config = self.config_data.get('sync', {})
        
        mapping = {
            'batch_size': sync_config.get('batch_size', 20),
            'sync_interval': sync_config.get('auto_sync_interval', 300),
            'priority_types': sync_config.get('priority_types', 'fatigue,unrecognized_operator')
        }
        
        return mapping.get(key, fallback)
    
    def getint(self, section, key, fallback=0):
        """Obtiene un valor entero emulando ConfigParser.getint()"""
        try:
            value = self.get(section, key, fallback)
            return int(value) if value is not None else fallback
        except (ValueError, TypeError):
            return fallback
    
    def getfloat(self, section, key, fallback=0.0):
        """Obtiene un valor float emulando ConfigParser.getfloat()"""
        try:
            value = self.get(section, key, fallback)
            return float(value) if value is not None else fallback
        except (ValueError, TypeError):
            return fallback
    
    def getboolean(self, section, key, fallback=False):
        """Obtiene un valor booleano emulando ConfigParser.getboolean()"""
        try:
            value = self.get(section, key, fallback)
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return value.lower() in ('true', 'yes', '1', 'on')
            else:
                return bool(value) if value is not None else fallback
        except (ValueError, TypeError):
            return fallback
    
    def reload(self):
        """Recarga la configuración desde el archivo YAML"""
        self._load_yaml_config()
        logger.info("Configuración YAML recargada")

# Instancia global para compatibilidad
_global_config = None

def get_yaml_config():
    """Obtiene la instancia global del adaptador de configuración"""
    global _global_config
    if _global_config is None:
        _global_config = YamlConfigAdapter()
    return _global_config

def reload_config():
    """Recarga la configuración global"""
    global _global_config
    if _global_config:
        _global_config.reload()
    else:
        _global_config = YamlConfigAdapter()