import time
import threading
import logging
import signal
import sys

# Importar el sistema principal
from main_system import SafetySystem

# Importar componentes de sincronización
from client.utils.logger import setup_logging
from client.db.local_storage import LocalStorage
from client.api.api_client import ApiClient
from client.utils.connection import ConnectionManager
from client.api.sync import SyncManager

# 🆕 IMPORTS CORREGIDOS: Importar adaptadores desde nueva ubicación core/adapters/
from core.adapters.fatigue_adapter import FatigueAdapter
from core.adapters.behavior_adapter import BehaviorAdapter
from core.adapters.face_recognition_adapter import FaceRecognitionAdapter

logger = logging.getLogger('sync_integrator')

class SyncIntegrator:
    """
    Integrador que añade sincronización online/offline al sistema principal.
    """
    def __init__(self):
        # Inicializar logger
        setup_logging()
        logger.info("=== Iniciando Integrador de Sincronización ===")
        
        # Inicializar componentes de sincronización
        self.db = LocalStorage()
        self.api_client = ApiClient()
        self.connection_manager = ConnectionManager(self.db, self.api_client)
        self.sync_manager = SyncManager(self.db, self.api_client, self.connection_manager)
        
        # 🆕 ADAPTADORES DESDE NUEVA UBICACIÓN: core/adapters/
        logger.info("Inicializando adaptadores desde core/adapters/...")
        
        try:
            self.fatigue_adapter = FatigueAdapter()
            logger.info("✅ FatigueAdapter inicializado desde core/adapters/")
        except Exception as e:
            logger.error(f"❌ Error inicializando FatigueAdapter: {e}")
            self.fatigue_adapter = None
        
        try:
            self.behavior_adapter = BehaviorAdapter()
            logger.info("✅ BehaviorAdapter inicializado desde core/adapters/")
        except Exception as e:
            logger.error(f"❌ Error inicializando BehaviorAdapter: {e}")
            self.behavior_adapter = None
        
        try:
            self.face_recognition_adapter = FaceRecognitionAdapter()
            logger.info("✅ FaceRecognitionAdapter inicializado desde core/adapters/")
        except Exception as e:
            logger.error(f"❌ Error inicializando FaceRecognitionAdapter: {e}")
            self.face_recognition_adapter = None
        
        # Sistema principal (mantener referencia si es necesario)
        self.safety_system = None
        
        # Estado del integrador
        self.running = False
        
        # Configurar manejadores de señales
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)
        
        # Log de inicialización completada
        adapters_count = sum(1 for adapter in [self.fatigue_adapter, self.behavior_adapter, self.face_recognition_adapter] if adapter is not None)
        logger.info(f"🎯 Integrador inicializado: {adapters_count}/3 adaptadores disponibles")
    
    def start(self):
        """
        Inicia los servicios de sincronización.
        Este método debe llamarse antes de iniciar el sistema principal.
        """
        logger.info("=== Iniciando servicios de sincronización ===")
        
        # Iniciar monitoreo de conexión
        self.connection_manager.start_monitoring()
        logger.info("✅ Monitoreo de conexión iniciado")
        
        # Probar conectividad inicial
        connectivity = self.connection_manager.test_full_connectivity()
        logger.info("🌐 Estado de conectividad:")
        logger.info(f"  Internet: {'✅' if connectivity['internet'] else '❌'}")
        logger.info(f"  Servidor: {'✅' if connectivity['server'] else '❌'}")
        logger.info(f"  Autenticación: {'✅' if connectivity['authentication'] else '❌'}")
        
        # Iniciar sincronización automática
        self.sync_manager.start_auto_sync()
        logger.info("✅ Sincronización automática iniciada")
        
        self.running = True
        logger.info("=== Integrador de sincronización iniciado correctamente ===")
        
        return True
    
    def handle_exit(self, signum, frame):
        """Manejar señales de salida"""
        logger.info(f"Señal {signum} recibida. Cerrando sistema de sincronización...")
        self.stop()
    
    def stop(self):
        """Detener los servicios de sincronización"""
        if not self.running:
            return
            
        self.running = False
        
        # Detener servicios de sincronización
        logger.info("=== Deteniendo servicios de sincronización ===")
        
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
            logger.info("✅ Conexiones cerradas")
        except Exception as e:
            logger.error(f"Error cerrando base de datos: {e}")
        
        logger.info("=== Integrador de sincronización detenido correctamente ===")
    
    # 🆕 MÉTODOS MEJORADOS: Acceso a adaptadores con verificación
    def get_fatigue_adapter(self):
        """Obtener el adaptador de fatiga"""
        if self.fatigue_adapter is None:
            logger.warning("FatigueAdapter no está disponible")
        return self.fatigue_adapter
    
    def get_behavior_adapter(self):
        """Obtener el adaptador de comportamientos"""
        if self.behavior_adapter is None:
            logger.warning("BehaviorAdapter no está disponible")
        return self.behavior_adapter
    
    def get_face_recognition_adapter(self):
        """Obtener el adaptador de reconocimiento facial"""
        if self.face_recognition_adapter is None:
            logger.warning("FaceRecognitionAdapter no está disponible")
        return self.face_recognition_adapter
    
    def get_available_adapters(self):
        """Obtener lista de adaptadores disponibles"""
        available = {}
        
        if self.fatigue_adapter:
            available['fatigue'] = self.fatigue_adapter
        if self.behavior_adapter:
            available['behavior'] = self.behavior_adapter
        if self.face_recognition_adapter:
            available['face_recognition'] = self.face_recognition_adapter
        
        return available
    
    def get_adapters_info(self):
        """Obtener información detallada de todos los adaptadores"""
        info = {}
        
        try:
            if self.fatigue_adapter and hasattr(self.fatigue_adapter, 'get_adapter_info'):
                info['fatigue'] = self.fatigue_adapter.get_adapter_info()
        except Exception as e:
            info['fatigue'] = {'error': str(e)}
        
        try:
            if self.behavior_adapter and hasattr(self.behavior_adapter, 'get_adapter_info'):
                info['behavior'] = self.behavior_adapter.get_adapter_info()
        except Exception as e:
            info['behavior'] = {'error': str(e)}
        
        try:
            if self.face_recognition_adapter and hasattr(self.face_recognition_adapter, 'get_adapter_info'):
                info['face_recognition'] = self.face_recognition_adapter.get_adapter_info()
        except Exception as e:
            info['face_recognition'] = {'error': str(e)}
        
        return info
    
    # Método para verificar estado de sincronización
    def get_sync_status(self):
        """
        Obtener estado actual de la sincronización.
        
        Returns:
            dict: Estado de la sincronización con información adicional
        """
        base_status = {
            'is_online': self.connection_manager.is_online(),
            'pending_events': len(self.db.get_pending_events(1000000)),
            'is_syncing': self.sync_manager.is_syncing,
            'last_sync': self.db.get_connection_status().get('last_sync')
        }
        
        # Añadir información de adaptadores
        base_status['adapters'] = {
            'fatigue': self.fatigue_adapter is not None,
            'behavior': self.behavior_adapter is not None,
            'face_recognition': self.face_recognition_adapter is not None
        }
        
        return base_status
    
    def force_sync(self):
        """Forzar sincronización inmediata"""
        logger.info("🔄 Forzando sincronización inmediata...")
        result = self.sync_manager.force_sync()
        if result:
            logger.info("✅ Sincronización forzada exitosa")
        else:
            logger.warning("⚠️ Error en sincronización forzada")
        return result
    
    def test_adapters(self):
        """Probar funcionamiento de todos los adaptadores"""
        logger.info("🧪 Probando adaptadores...")
        
        # Usar la función de prueba del módulo adapters
        try:
            from core.adapters import test_adapters
            results = test_adapters()
            
            for adapter_name, result in results.items():
                if result['status'] == 'success':
                    logger.info(f"✅ {adapter_name}: OK")
                else:
                    logger.error(f"❌ {adapter_name}: {result['error']}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error probando adaptadores: {e}")
            return {'error': str(e)}