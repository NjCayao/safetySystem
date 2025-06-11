import os
import cv2
import time
import logging
import uuid

# 🆕 CAMBIO: Usar las clases actualizadas que ya usan YAML
from client.db.local_storage import LocalStorage
from client.utils.file_manager import FileManager

logger = logging.getLogger('event_manager')

class EventManager:
    """
    Gestor centralizado de eventos detectados por los diferentes módulos.
    Maneja el almacenamiento local y prepara los eventos para sincronización.
    """
    def __init__(self):
        self.db = LocalStorage()
        self.file_manager = FileManager()
        
        logger.info("EventManager inicializado con configuración YAML")
    
    def register_event(self, event_type, event_data, frame=None, operator_id=None):
        """
        Registra un nuevo evento en el sistema.
        
        Args:
            event_type (str): Tipo de evento ('fatigue', 'cellphone', 'smoking', 'unrecognized_operator')
            event_data (dict): Datos específicos del evento
            frame (numpy.ndarray, optional): Imagen capturada del evento
            operator_id (int, optional): ID del operador implicado
            
        Returns:
            str: ID del evento registrado o None si falló
        """
        try:
            # Guardar imagen si está disponible
            image_path = None
            if frame is not None:
                # Convertir frame a formato de imagen
                _, img_encoded = cv2.imencode('.jpg', frame)
                # Guardar imagen localmente
                image_path = self.file_manager.save_image(img_encoded.tobytes(), event_type)
                
                if image_path:
                    logger.info(f"Imagen guardada para evento {event_type}: {image_path}")
                else:
                    logger.warning(f"No se pudo guardar la imagen para evento {event_type}")
            
            # Registrar evento en la base de datos local
            event_id = self.db.store_event(
                event_type=event_type,
                event_data=event_data,
                image_path=image_path,
                operator_id=operator_id
            )
            
            if event_id:
                logger.info(f"Evento {event_type} registrado con ID: {event_id}")
                return event_id
            else:
                logger.error(f"Error al registrar evento {event_type}")
                return None
                
        except Exception as e:
            logger.error(f"Excepción al registrar evento {event_type}: {str(e)}")
            return None
    
    def get_pending_events_count(self):
        """Obtener número de eventos pendientes de sincronización"""
        try:
            events = self.db.get_pending_events(1000000)  # Número alto para contar todos
            return len(events)
        except Exception as e:
            logger.error(f"Error obteniendo cuenta de eventos pendientes: {str(e)}")
            return 0
    
    def get_storage_stats(self):
        """Obtener estadísticas combinadas de almacenamiento"""
        try:
            # Estadísticas de archivos
            file_stats = self.file_manager.get_storage_stats()
            
            # Estadísticas de base de datos
            pending_count = self.get_pending_events_count()
            
            return {
                'files': file_stats,
                'pending_events': pending_count,
                'database_path': self.db.conn.execute("PRAGMA database_list").fetchone()[2] if hasattr(self.db, 'conn') else 'unknown'
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de almacenamiento: {str(e)}")
            return None
    
    def cleanup_storage(self, force=False):
        """Limpiar almacenamiento (imágenes y eventos antiguos)"""
        try:
            results = {
                'images_deleted': 0,
                'events_cleaned': False,
                'errors': []
            }
            
            # Limpiar imágenes
            if force:
                results['images_deleted'] = self.file_manager.force_cleanup()
            else:
                self.file_manager.cleanup_old_images()
            
            # Limpiar eventos antiguos de la base de datos
            try:
                results['events_cleaned'] = self.db.cleanup_old_events()
            except Exception as e:
                results['errors'].append(f"Error limpiando eventos: {str(e)}")
            
            logger.info(f"Limpieza de almacenamiento completada: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error en limpieza de almacenamiento: {str(e)}")
            return {'images_deleted': 0, 'events_cleaned': False, 'errors': [str(e)]}