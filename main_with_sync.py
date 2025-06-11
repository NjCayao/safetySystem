#!/usr/bin/env python3
import time
import signal
import sys
import logging

# Importar componentes
from main_system import SafetySystem
from sync_integrator import SyncIntegrator

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('safety_system_with_sync.log')
    ]
)

logger = logging.getLogger('main_with_sync')

class SafetySystemWithSync:
    """
    Sistema de prevención de accidentes con sincronización online/offline.
    Este sistema es un ejemplo de cómo integrar el sistema principal con
    la funcionalidad de sincronización usando adaptadores desde core/adapters/.
    """
    def __init__(self):
        logger.info("=== Iniciando Sistema de Prevención de Accidentes con Sincronización ===")
        
        # Inicializar integrador de sincronización (ya tiene los adaptadores desde core/adapters/)
        try:
            self.sync_integrator = SyncIntegrator()
            logger.info("✅ SyncIntegrator inicializado con adaptadores desde core/adapters/")
        except Exception as e:
            logger.error(f"❌ Error inicializando SyncIntegrator: {e}")
            self.sync_integrator = None
        
        # Inicializar sistema principal
        try:
            self.safety_system = SafetySystem()
            logger.info("✅ SafetySystem inicializado")
        except Exception as e:
            logger.error(f"❌ Error inicializando SafetySystem: {e}")
            self.safety_system = None
        
        # Configurar manejadores de señales
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)
        
        self.running = False
        
        # Mostrar información de adaptadores disponibles
        if self.sync_integrator:
            self._show_adapters_info()
    
    def _show_adapters_info(self):
        """Mostrar información de adaptadores disponibles"""
        logger.info("🔧 Información de adaptadores:")
        
        try:
            available_adapters = self.sync_integrator.get_available_adapters()
            adapters_info = self.sync_integrator.get_adapters_info()
            
            for adapter_name, adapter_instance in available_adapters.items():
                logger.info(f"  ✅ {adapter_name}: Disponible")
                
                # Mostrar información detallada si está disponible
                if adapter_name in adapters_info and 'location' in adapters_info[adapter_name]:
                    location = adapters_info[adapter_name]['location']
                    logger.info(f"     Ubicación: {location}")
            
            if not available_adapters:
                logger.warning("  ⚠️ No hay adaptadores disponibles")
            
        except Exception as e:
            logger.warning(f"Error obteniendo información de adaptadores: {e}")
    
    def start(self):
        """Iniciar el sistema completo"""
        logger.info("=== Iniciando sistema completo ===")
        
        # Iniciar integrador de sincronización
        if self.sync_integrator:
            try:
                self.sync_integrator.start()
                logger.info("✅ Servicios de sincronización iniciados")
            except Exception as e:
                logger.error(f"❌ Error iniciando sincronización: {e}")
        else:
            logger.warning("⚠️ Sincronización no disponible - continuando sin sincronización")
        
        # Aquí puedes modificar cómo el sistema principal usa los adaptadores
        # Por ejemplo, podrías modificar el bucle principal para usar los adaptadores
        # en lugar de los detectores originales
        
        if self.safety_system:
            # Integrar adaptadores con el sistema principal si es necesario
            self._integrate_adapters_with_main_system()
            
            # Iniciar sistema principal
            try:
                self.safety_system.start()
                logger.info("✅ Sistema principal iniciado")
            except Exception as e:
                logger.error(f"❌ Error iniciando sistema principal: {e}")
                return False
        else:
            logger.error("❌ No se puede iniciar - sistema principal no disponible")
            return False
        
        self.running = True
        logger.info("=== Sistema completo iniciado ===")
        
        # Imprimir instrucciones de uso
        self._print_usage_instructions()
        
        return True
    
    def _integrate_adapters_with_main_system(self):
        """Integrar adaptadores con el sistema principal"""
        if not self.sync_integrator:
            return
        
        try:
            # Obtener adaptadores disponibles
            available_adapters = self.sync_integrator.get_available_adapters()
            
            # Aquí podrías modificar el sistema principal para usar los adaptadores
            # Por ejemplo:
            # - Reemplazar detectores originales con adaptadores
            # - Añadir hooks para sincronización automática
            # - Configurar callbacks para eventos detectados
            
            logger.info(f"🔗 Integrando {len(available_adapters)} adaptadores con sistema principal")
            
            # Ejemplo de integración (esto dependería de cómo quieras estructurar la integración)
            if 'fatigue' in available_adapters:
                # self.safety_system.fatigue_detector = available_adapters['fatigue']
                logger.info("  🔗 Adaptador de fatiga listo para integración")
            
            if 'behavior' in available_adapters:
                # self.safety_system.behavior_detector = available_adapters['behavior']
                logger.info("  🔗 Adaptador de comportamiento listo para integración")
            
            if 'face_recognition' in available_adapters:
                # self.safety_system.face_recognizer = available_adapters['face_recognition']
                logger.info("  🔗 Adaptador de reconocimiento facial listo para integración")
            
        except Exception as e:
            logger.warning(f"Error integrando adaptadores: {e}")
    
    def _print_usage_instructions(self):
        """Imprimir instrucciones de uso"""
        print("\n" + "="*70)
        print("🚀 Sistema de Prevención de Accidentes con Sincronización Online/Offline")
        print("="*70)
        print("✅ El sistema está ejecutándose con funcionalidad de sincronización.")
        print("📡 Los eventos detectados se almacenarán localmente cuando no haya conexión")
        print("🔄 y se sincronizarán automáticamente cuando la conexión se restablezca.")
        print()
        print("🔧 Adaptadores cargados desde: core/adapters/")
        
        if self.sync_integrator:
            available = self.sync_integrator.get_available_adapters()
            for adapter_name in available.keys():
                print(f"  ✅ {adapter_name.title()}Adapter")
        
        print()
        print("⌨️  Presione Ctrl+C para detener el sistema.")
        print("="*70)
    
    def handle_exit(self, signum, frame):
        """Manejar señales de salida"""
        print(f"\n🛑 Cerrando el sistema (señal {signum})...")
        self.stop()
    
    def stop(self):
        """Detener el sistema completo"""
        if not self.running:
            return
            
        self.running = False
        
        # Detener sistema principal
        if self.safety_system:
            logger.info("🛑 Deteniendo sistema principal...")
            try:
                self.safety_system.stop()
                logger.info("✅ Sistema principal detenido")
            except Exception as e:
                logger.error(f"Error deteniendo sistema principal: {e}")
        
        # Detener integrador de sincronización
        if self.sync_integrator:
            logger.info("🛑 Deteniendo integrador de sincronización...")
            try:
                self.sync_integrator.stop()
                logger.info("✅ Integrador de sincronización detenido")
            except Exception as e:
                logger.error(f"Error deteniendo sincronización: {e}")
        
        logger.info("=== Sistema completo detenido ===")
        
        # Salir del programa
        sys.exit(0)
    
    def get_system_status(self):
        """Obtener estado completo del sistema"""
        status = {
            'running': self.running,
            'safety_system': self.safety_system is not None,
            'sync_integrator': self.sync_integrator is not None,
            'adapters': {}
        }
        
        if self.sync_integrator:
            try:
                status['sync_status'] = self.sync_integrator.get_sync_status()
                status['adapters'] = self.sync_integrator.get_available_adapters()
            except Exception as e:
                status['sync_error'] = str(e)
        
        return status
    
    def force_sync(self):
        """Forzar sincronización inmediata"""
        if self.sync_integrator:
            return self.sync_integrator.force_sync()
        else:
            logger.warning("No se puede forzar sincronización - integrador no disponible")
            return False

# Punto de entrada
if __name__ == "__main__":
    print("🚀 Iniciando Safety System con Sincronización...")
    print("📁 Adaptadores desde: core/adapters/")
    
    system = SafetySystemWithSync()
    try:
        if system.start():
            # Mantener el programa principal ejecutándose
            while system.running:
                try:
                    # Mostrar estado de sincronización cada 5 minutos
                    if int(time.time()) % 300 == 0:  # cada 5 minutos
                        if system.sync_integrator:
                            status = system.sync_integrator.get_sync_status()
                            logger.info(f"📊 Estado: "
                                      f"{'🟢 ONLINE' if status['is_online'] else '🔴 OFFLINE'}, "
                                      f"📤 {status['pending_events']} pendientes, "
                                      f"{'🔄 Sincronizando' if status['is_syncing'] else '⏸️ En espera'}")
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Error en bucle principal: {e}")
                    time.sleep(5)
        else:
            logger.error("❌ No se pudo iniciar el sistema")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Interrupción de usuario recibida")
    except Exception as e:
        logger.critical(f"❌ Error crítico: {e}")
        print(f"💥 Error crítico: {e}")
    finally:
        system.stop()
        print("👋 Sistema detenido completamente")