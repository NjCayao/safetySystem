import logging
import logging.config
import os
from datetime import datetime

def setup_logging():
    """Configurar sistema de logging con configuración YAML"""
    
    # Intentar cargar configuración desde YAML
    try:
        from client.config.yaml_config_adapter import get_yaml_config
        config = get_yaml_config()
        
        # Obtener configuración de logging desde YAML
        log_level = config.get('LOGGING', 'level', 'INFO')
        file_max_size = config.getint('LOGGING', 'file_max_size', 10485760)  # 10MB default
        file_backup_count = config.getint('LOGGING', 'file_backup_count', 5)
        
        print(f"✅ Configuración de logging cargada desde YAML:")
        print(f"   Nivel: {log_level}")
        print(f"   Tamaño máximo archivo: {file_max_size // 1024 // 1024}MB")
        print(f"   Archivos de backup: {file_backup_count}")
        
    except Exception as e:
        # Fallback a valores por defecto si no se puede cargar YAML
        log_level = 'INFO'
        file_max_size = 10485760  # 10MB
        file_backup_count = 5
        print(f"⚠️ Error cargando configuración YAML para logging: {e}")
        print("   Usando valores por defecto")
    
    # Asegurar que existe el directorio de logs
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nombre de archivo con fecha
    log_file = os.path.join(log_dir, f"safety_system_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Configuración optimizada para Raspberry Pi
    config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'verbose',
                'filename': log_file,
                'maxBytes': file_max_size,
                'backupCount': file_backup_count,
                'encoding': 'utf8'
            },
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file'],
                'level': log_level,
                'propagate': False
            },
            # Loggers específicos con configuración desde YAML si está disponible
            'api_client': {
                'level': 'DEBUG',
                'propagate': True,
            },
            'local_storage': {
                'level': 'DEBUG',
                'propagate': True,
            },
            'connection': {
                'level': 'INFO',
                'propagate': True,
            },
            'sync': {
                'level': 'DEBUG',
                'propagate': True,
            },
            'file_manager': {
                'level': 'INFO',
                'propagate': True,
            },
            'event_manager': {
                'level': 'INFO',
                'propagate': True,
            },
            'yaml_config_adapter': {
                'level': 'INFO',
                'propagate': True,
            },
        }
    }
    
    # Intentar aplicar configuración específica por módulo desde YAML
    try:
        from client.config.yaml_config_adapter import get_yaml_config
        yaml_config = get_yaml_config()
        
        # Verificar si hay configuración específica de módulos en YAML
        modules_config = yaml_config.config_data.get('logging', {}).get('modules', {})
        
        for module_name, module_level in modules_config.items():
            if module_name in config_dict['loggers']:
                config_dict['loggers'][module_name]['level'] = module_level
                print(f"   Módulo {module_name}: {module_level}")
        
    except Exception:
        pass  # Usar configuración por defecto si hay error
    
    # Aplicar configuración
    logging.config.dictConfig(config_dict)
    
    # Logger principal
    main_logger = logging.getLogger('main')
    main_logger.info("=== Sistema de Logging Inicializado ===")
    main_logger.info(f"Archivo de log: {log_file}")
    main_logger.info(f"Nivel de logging: {log_level}")
    
    return main_logger

def get_logger(name):
    """Obtener logger con nombre específico"""
    return logging.getLogger(name)

def set_log_level(level):
    """Cambiar nivel de logging dinámicamente"""
    try:
        logging.getLogger().setLevel(getattr(logging, level.upper()))
        logging.getLogger('main').info(f"Nivel de logging cambiado a: {level.upper()}")
        return True
    except AttributeError:
        logging.getLogger('main').error(f"Nivel de logging inválido: {level}")
        return False

def log_system_info():
    """Registrar información del sistema al inicio"""
    logger = logging.getLogger('system_info')
    
    try:
        import platform
        import psutil
        
        logger.info("=== Información del Sistema ===")
        logger.info(f"Sistema operativo: {platform.system()} {platform.release()}")
        logger.info(f"Arquitectura: {platform.machine()}")
        logger.info(f"Python: {platform.python_version()}")
        
        # Información de memoria
        memory = psutil.virtual_memory()
        logger.info(f"Memoria total: {memory.total // 1024 // 1024} MB")
        logger.info(f"Memoria disponible: {memory.available // 1024 // 1024} MB")
        
        # Información de disco
        disk = psutil.disk_usage('/')
        logger.info(f"Espacio en disco total: {disk.total // 1024 // 1024 // 1024} GB")
        logger.info(f"Espacio en disco libre: {disk.free // 1024 // 1024 // 1024} GB")
        
    except Exception as e:
        logger.warning(f"Error obteniendo información del sistema: {e}")

def cleanup_old_logs(days_to_keep=30):
    """Limpiar logs antiguos"""
    logger = logging.getLogger('log_cleanup')
    
    try:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            return
        
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
        
        deleted_count = 0
        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                file_path = os.path.join(log_dir, filename)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Log antiguo eliminado: {filename}")
                    except OSError as e:
                        logger.warning(f"No se pudo eliminar {filename}: {e}")
        
        if deleted_count > 0:
            logger.info(f"Limpieza completada: {deleted_count} logs antiguos eliminados")
        else:
            logger.info("No hay logs antiguos para eliminar")
            
    except Exception as e:
        logger.error(f"Error durante limpieza de logs: {e}")