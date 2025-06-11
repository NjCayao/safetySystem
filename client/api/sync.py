import uuid
import time
import logging
import threading
from datetime import datetime, timedelta

# 🆕 CAMBIO: Usar adaptador YAML en lugar de ConfigParser
from client.config.yaml_config_adapter import get_yaml_config

# Cargar configuración desde YAML
config = get_yaml_config()

logger = logging.getLogger('sync')

class SyncManager:
    def __init__(self, db, api_client, connection_manager):
        self.db = db
        self.api_client = api_client
        self.connection_manager = connection_manager
        self.sync_interval = config.getint('SYNC', 'sync_interval')
        self.batch_size = config.getint('SYNC', 'batch_size')
        self.is_running = False
        self.thread = None
        self.is_syncing = False
        
        # Log de configuración cargada
        logger.info(f"SyncManager inicializado:")
        logger.info(f"  Sync interval: {self.sync_interval}s")
        logger.info(f"  Batch size: {self.batch_size}")
    
    def start_auto_sync(self):
        """Iniciar sincronización automática en un hilo separado"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._sync_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Sincronización automática iniciada")
    
    def stop_auto_sync(self):
        """Detener sincronización automática"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
            logger.info("Sincronización automática detenida")
    
    def _sync_loop(self):
        """Bucle principal de sincronización automática"""
        while self.is_running:
            if self.connection_manager.is_online():
                try:
                    self.sync_pending_events()
                except Exception as e:
                    logger.error(f"Error durante sincronización automática: {str(e)}")
            
            # Dormir hasta el próximo intento
            time.sleep(self.sync_interval)
    
    def sync_pending_events(self):
        """Sincronizar eventos pendientes"""
        if self.is_syncing:
            logger.info("Ya hay una sincronización en progreso")
            return False
        
        try:
            self.is_syncing = True
            
            # Verificar conexión
            if not self.connection_manager.is_online():
                logger.warning("No hay conexión a internet. Sincronización cancelada.")
                self.is_syncing = False
                return False
            
            # Asegurar autenticación
            if not self.api_client.ensure_authenticated():
                logger.error("No se pudo autenticar con el servidor")
                self.is_syncing = False
                return False
            
            # Obtener eventos pendientes
            events = self.db.get_pending_events(self.batch_size)
            
            if not events:
                logger.info("No hay eventos pendientes para sincronizar")
                self.is_syncing = False
                return True
            
            # Crear lote de sincronización
            event_ids = [event['local_id'] for event in events]
            batch_id = self.db.create_sync_batch(event_ids)
            
            if not batch_id:
                logger.error("Error al crear lote de sincronización")
                self.is_syncing = False
                return False
            
            # Preparar eventos para enviar
            events_to_send = []
            for event in events:
                # Preparar datos del evento para API
                api_event = {
                    'event_type': event['event_type'],
                    'operator_id': event['operator_id'],
                    'event_time': event['event_time'],
                    'data': event['event_data'],
                    'has_image': bool(event['image_path']),
                    'local_id': event['local_id']
                }
                events_to_send.append(api_event)
            
            # Enviar lote al servidor
            logger.info(f"Enviando lote {batch_id} con {len(events_to_send)} eventos")
            success, response = self.api_client.sync_batch(batch_id, events_to_send)
            
            if success:
                # Marcar lote como enviado
                self.db.mark_batch_as_sent(batch_id)
                
                # Subir imágenes si existen
                for event in events:
                    if event['image_path']:
                        # El evento en el servidor tiene un ID diferente, necesitamos mapearlo
                        if response and 'data' in response:
                            # Buscar id del servidor correspondiente al local_id
                            for server_event in response['data'].get('events', []):
                                if server_event.get('local_id') == event['local_id']:
                                    server_id = server_event.get('id')
                                    if server_id:
                                        self.api_client.upload_image(server_id, event['image_path'])
                
                # Confirmar lote
                if self.api_client.confirm_sync(batch_id):
                    self.db.mark_batch_as_confirmed(batch_id)
                    self.db.update_last_sync_time()
                    
                    # Limpiar eventos antiguos
                    self.db.cleanup_old_events()
                    
                    logger.info(f"Lote {batch_id} sincronizado y confirmado exitosamente")
                    
                    # Si aún hay eventos pendientes, programar próxima sincronización
                    pending = self.db.get_pending_events(1)
                    if pending:
                        logger.info(f"Aún hay eventos pendientes. Próxima sincronización en {self.sync_interval} segundos")
                
                self.is_syncing = False
                return True
            else:
                logger.error(f"Error al sincronizar lote: {response}")
                self.is_syncing = False
                return False
                
        except Exception as e:
            logger.error(f"Excepción durante sincronización: {str(e)}")
            self.is_syncing = False
            return False
    
    def force_sync(self):
        """Forzar sincronización inmediata"""
        return self.sync_pending_events()
    
    def get_sync_status(self):
        """Obtener estado de sincronización"""
        connection_status = self.connection_manager.get_status()
        
        # Contar eventos pendientes
        pending = len(self.db.get_pending_events(1000000)) # Número alto para contar todos
        
        return {
            'is_online': connection_status['is_online'],
            'last_sync': connection_status['last_sync'],
            'pending_events': pending,
            'is_syncing': self.is_syncing
        }