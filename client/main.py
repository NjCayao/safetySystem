import os
import time
import signal
import sys

# 🆕 CAMBIO: Usar adaptador YAML en lugar de ConfigParser
from client.config.yaml_config_adapter import get_yaml_config

# Importar componentes
from client.utils.logger import setup_logging
from client.db.local_storage import LocalStorage
from client.api.api_client import ApiClient
from client.utils.connection import ConnectionManager
from client.api.sync import SyncManager
from client.utils.file_manager import FileManager

# Cargar configuración desde YAML
config = get_yaml_config()

# Inicializar logger
logger = setup_logging()

class SafetySystemClient:
    def __init__(self):
        self.running = True
        
        # Imprimir información de configuración
        logger.info("=== Iniciando Safety System Client ===")
        logger.info(f"Configuración cargada desde YAML:")
        logger.info(f"  Device ID: {config.get('DEVICE', 'device_id')}")
        logger.info(f"  Server URL: {config.get('SERVER', 'api_url')}")
        logger.info(f"  Sync enabled: {config.get('SYNC', 'sync_interval')}s")
        
        # Inicializar componentes
        logger.info("Iniciando sistema de seguridad...")
        
        self.db = LocalStorage()
        logger.info("Almacenamiento local inicializado")
        
        self.api_client = ApiClient()
        logger.info("Cliente API inicializado")
        
        self.connection_manager = ConnectionManager(self.db, self.api_client)
        logger.info("Gestor de conexión inicializado")
        
        self.sync_manager = SyncManager(self.db, self.api_client, self.connection_manager)
        logger.info("Gestor de sincronización inicializado")
        
        self.file_manager = FileManager()
        logger.info("Gestor de archivos inicializado")
        
        # Configurar manejadores de señales
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)
        
        logger.info("Sistema de sincronización inicializado correctamente")
    
    def start(self):
        """Iniciar todos los servicios"""
        logger.info("=== Iniciando servicios de sincronización ===")
        
        # Iniciar monitoreo de conexión
        self.connection_manager.start_monitoring()
        logger.info("✅ Monitoreo de conexión iniciado")
        
        # Probar conectividad completa inicial
        logger.info("Probando conectividad inicial...")
        connectivity = self.connection_manager.test_full_connectivity()
        logger.info(f"Estado de conectividad inicial:")
        logger.info(f"  Internet: {'✅' if connectivity['internet'] else '❌'}")
        logger.info(f"  Servidor: {'✅' if connectivity['server'] else '❌'}")
        logger.info(f"  Autenticación: {'✅' if connectivity['authentication'] else '❌'}")
        
        # Esperar conexión inicial para intentar autenticación
        if connectivity['internet']:
            logger.info("Conexión disponible, intentando autenticación...")
            if self.api_client.authenticate():
                logger.info("✅ Autenticación inicial exitosa")
            else:
                logger.warning("⚠️ Autenticación inicial fallida - continuando en modo offline")
        else:
            logger.warning("⚠️ Sin conexión inicial - continuando en modo offline")
        
        # Iniciar sincronización automática
        self.sync_manager.start_auto_sync()
        logger.info("✅ Sincronización automática iniciada")
        
        # Mostrar estadísticas iniciales
        self._show_initial_stats()
        
        logger.info("=== Sistema iniciado completamente ===")
        logger.info("Presiona Ctrl+C para detener el sistema")
        
        # Bucle principal - mantener el sistema funcionando
        frame_count = 0
        last_status_time = time.time()
        
        try:
            while self.running:
                try:
                    frame_count += 1
                    current_time = time.time()
                    
                    # Mostrar estado cada 60 segundos
                    if current_time - last_status_time >= 60:
                        self._show_status_update(frame_count)
                        last_status_time = current_time
                        frame_count = 0
                    
                    # Pequeña pausa para no saturar CPU
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error en bucle principal: {str(e)}")
                    time.sleep(5)  # Pausa más larga en caso de error
            
        except KeyboardInterrupt:
            logger.info("Interrupción de usuario recibida")
        finally:
            self.stop()
    
    def _show_initial_stats(self):
        """Mostrar estadísticas iniciales del sistema"""
        try:
            # Estadísticas de eventos pendientes
            pending_events = len(self.db.get_pending_events(1000000))
            logger.info(f"📊 Eventos pendientes de sincronización: {pending_events}")
            
            # Estadísticas de almacenamiento
            storage_stats = self.file_manager.get_storage_stats()
            if storage_stats:
                logger.info(f"📁 Imágenes almacenadas: {storage_stats['total_images']}")
                logger.info(f"💾 Espacio usado: {storage_stats['total_size_mb']} MB")
            
            # Estado de conexión
            connection_status = self.connection_manager.get_status()
            if connection_status.get('last_sync'):
                logger.info(f"🔄 Última sincronización: {connection_status['last_sync']}")
            else:
                logger.info("🔄 Sin sincronizaciones previas")
                
        except Exception as e:
            logger.warning(f"Error mostrando estadísticas iniciales: {e}")
    
    def _show_status_update(self, frames_processed):
        """Mostrar actualización de estado cada minuto"""
        try:
            # Estado de conexión
            is_online = self.connection_manager.is_online()
            connection_status = "🟢 ONLINE" if is_online else "🔴 OFFLINE"
            
            # Estado de sincronización
            sync_status = self.sync_manager.get_sync_status()
            sync_info = f"Pendientes: {sync_status['pending_events']}"
            if sync_status['is_syncing']:
                sync_info += " (Sincronizando...)"
            
            # Estado de autenticación
            auth_status = "🔐 Autenticado" if self.api_client.is_token_valid() else "🔓 No autenticado"
            
            logger.info(f"📊 Estado del sistema:")
            logger.info(f"  Conexión: {connection_status}")
            logger.info(f"  Sincronización: {sync_info}")
            logger.info(f"  Autenticación: {auth_status}")
            logger.info(f"  Frames procesados: {frames_processed}")
            
        except Exception as e:
            logger.warning(f"Error mostrando actualización de estado: {e}")
    
    def handle_exit(self, signum, frame):
        """Manejar señales de salida"""
        logger.info(f"Señal {signum} recibida. Cerrando sistema...")
        self.stop()
    
    def stop(self):
        """Detener todos los servicios"""
        if not self.running:
            return
            
        self.running = False
        
        logger.info("=== Deteniendo servicios ===")
        
        # Detener servicios
        try:
            self.sync_manager.stop_auto_sync()
            logger.info("✅ Sincronización automática detenida")
        except Exception as e:
            logger.error(f"Error deteniendo sincronización: {e}")
        
        try:
            self.connection_manager.stop_monitoring()
            logger.info("✅ Monitoreo de conexión detenido")
        except Exception as e:
            logger.error(f"Error deteniendo monitoreo: {e}")
        
        # Cerrar conexiones
        try:
            self.db.close()
            logger.info("✅ Conexiones de base de datos cerradas")
        except Exception as e:
            logger.error(f"Error cerrando base de datos: {e}")
        
        # Estadísticas finales
        self._show_final_stats()
        
        logger.info("=== Sistema detenido correctamente ===")
    
    def _show_final_stats(self):
        """Mostrar estadísticas finales antes de cerrar"""
        try:
            # Último estado de sincronización
            sync_status = self.sync_manager.get_sync_status()
            logger.info(f"📊 Estadísticas finales:")
            logger.info(f"  Eventos pendientes: {sync_status['pending_events']}")
            
            # Última sincronización
            if sync_status['last_sync']:
                logger.info(f"  Última sincronización: {sync_status['last_sync']}")
            
            # Espacio de almacenamiento
            storage_stats = self.file_manager.get_storage_stats()
            if storage_stats:
                logger.info(f"  Imágenes totales: {storage_stats['total_images']}")
                logger.info(f"  Espacio usado: {storage_stats['total_size_mb']} MB")
                
        except Exception as e:
            logger.warning(f"Error mostrando estadísticas finales: {e}")
    
    def force_sync(self):
        """Forzar sincronización inmediata (para uso manual)"""
        logger.info("Forzando sincronización inmediata...")
        result = self.sync_manager.force_sync()
        if result:
            logger.info("✅ Sincronización forzada completada")
        else:
            logger.warning("⚠️ Error en sincronización forzada")
        return result
    
    def get_system_status(self):
        """Obtener estado completo del sistema (para APIs o debugging)"""
        try:
            return {
                'running': self.running,
                'connection': self.connection_manager.get_status(),
                'sync': self.sync_manager.get_sync_status(),
                'authentication': self.api_client.is_token_valid(),
                'storage': self.file_manager.get_storage_stats(),
                'device_id': config.get('DEVICE', 'device_id'),
                'server_url': config.get('SERVER', 'api_url')
            }
        except Exception as e:
            logger.error(f"Error obteniendo estado del sistema: {e}")
            return {'error': str(e)}

# Punto de entrada
if __name__ == "__main__":
    print("=== Safety System Client - Modo Sincronización ===")
    print("Sistema de sincronización online/offline para Raspberry Pi")
    print("Configuración cargada desde config/production.yaml")
    print("-" * 60)
    
    system = SafetySystemClient()
    try:
        system.start()
    except KeyboardInterrupt:
        print("\n👋 Interrupción de usuario")
    except Exception as e:
        logger.critical(f"Error crítico: {e}")
        print(f"❌ Error crítico: {e}")
    finally:
        system.stop()
        print("👋 Sistema detenido")