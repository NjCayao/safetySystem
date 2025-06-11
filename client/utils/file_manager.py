import os
import time
import uuid
import shutil
import logging
from datetime import datetime

# 🆕 CAMBIO: Usar adaptador YAML en lugar de ConfigParser
from client.config.yaml_config_adapter import get_yaml_config

# Cargar configuración desde YAML
config = get_yaml_config()

logger = logging.getLogger('file_manager')

class FileManager:
    def __init__(self):
        self.base_path = config.get('STORAGE', 'image_storage_path')
        self.max_stored_images = config.getint('STORAGE', 'max_stored_images')
        
        # Crear directorio base si no existe
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)
        
        # Log de configuración cargada
        logger.info(f"FileManager inicializado:")
        logger.info(f"  Base path: {self.base_path}")
        logger.info(f"  Max stored images: {self.max_stored_images}")
    
    def save_image(self, image_data, event_type):
        """Guardar imagen en disco"""
        try:
            # Crear directorio para tipo de evento
            event_dir = os.path.join(self.base_path, event_type)
            if not os.path.exists(event_dir):
                os.makedirs(event_dir, exist_ok=True)
            
            # Crear directorio para fecha actual
            date_dir = os.path.join(event_dir, datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(date_dir):
                os.makedirs(date_dir, exist_ok=True)
            
            # Generar nombre único
            filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}.jpg"
            file_path = os.path.join(date_dir, filename)
            
            # Guardar archivo
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Imagen guardada: {file_path}")
            
            # Limpiar imágenes antiguas si es necesario
            self.cleanup_old_images()
            
            return file_path
            
        except Exception as e:
            logger.error(f"Error al guardar imagen: {str(e)}")
            return None
    
    def cleanup_old_images(self):
        """Limpiar imágenes antiguas para ahorrar espacio"""
        try:
            # Obtener lista de todas las imágenes
            all_images = []
            
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.join(root, file)
                        mtime = os.path.getmtime(full_path)
                        all_images.append((full_path, mtime))
            
            # Ordenar por fecha de modificación (más antiguo primero)
            all_images.sort(key=lambda x: x[1])
            
            # Eliminar imágenes antiguas si excedemos el límite
            if len(all_images) > self.max_stored_images:
                to_delete = all_images[:len(all_images) - self.max_stored_images]
                
                for path, _ in to_delete:
                    try:
                        os.remove(path)
                        logger.info(f"Imagen antigua eliminada: {path}")
                    except OSError as e:
                        logger.warning(f"No se pudo eliminar imagen {path}: {e}")
                
                # Limpiar directorios vacíos
                self._cleanup_empty_directories()
            
            return True
            
        except Exception as e:
            logger.error(f"Error durante limpieza de imágenes: {str(e)}")
            return False
    
    def _cleanup_empty_directories(self):
        """Eliminar directorios vacíos después de limpiar imágenes"""
        try:
            for root, dirs, files in os.walk(self.base_path, topdown=False):
                # Saltar el directorio base
                if root == self.base_path:
                    continue
                
                # Si el directorio está vacío, eliminarlo
                if not dirs and not files:
                    try:
                        os.rmdir(root)
                        logger.debug(f"Directorio vacío eliminado: {root}")
                    except OSError:
                        pass  # Ignorar errores de permisos
        except Exception as e:
            logger.warning(f"Error limpiando directorios vacíos: {e}")
    
    def get_image_path(self, event_id, event_type):
        """Obtener ruta de imagen basada en ID de evento"""
        try:
            event_dir = os.path.join(self.base_path, event_type)
            
            # Buscar recursivamente
            for root, dirs, files in os.walk(event_dir):
                for file in files:
                    if file.startswith(event_id):
                        return os.path.join(root, file)
            
            return None
            
        except Exception as e:
            logger.error(f"Error al buscar imagen: {str(e)}")
            return None
    
    def get_storage_stats(self):
        """Obtener estadísticas de almacenamiento"""
        try:
            stats = {
                'total_images': 0,
                'total_size_mb': 0,
                'images_by_type': {},
                'oldest_image': None,
                'newest_image': None
            }
            
            oldest_time = float('inf')
            newest_time = 0
            
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.join(root, file)
                        
                        # Contadores generales
                        stats['total_images'] += 1
                        file_size = os.path.getsize(full_path)
                        stats['total_size_mb'] += file_size / (1024 * 1024)
                        
                        # Estadísticas por tipo
                        event_type = os.path.basename(os.path.dirname(root))
                        if event_type not in stats['images_by_type']:
                            stats['images_by_type'][event_type] = 0
                        stats['images_by_type'][event_type] += 1
                        
                        # Fechas más antigua y nueva
                        mtime = os.path.getmtime(full_path)
                        if mtime < oldest_time:
                            oldest_time = mtime
                            stats['oldest_image'] = datetime.fromtimestamp(mtime).isoformat()
                        if mtime > newest_time:
                            newest_time = mtime
                            stats['newest_image'] = datetime.fromtimestamp(mtime).isoformat()
            
            # Redondear tamaño total
            stats['total_size_mb'] = round(stats['total_size_mb'], 2)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de almacenamiento: {str(e)}")
            return None
    
    def force_cleanup(self, keep_last_n=None):
        """Forzar limpieza manteniendo solo las últimas N imágenes"""
        try:
            if keep_last_n is None:
                keep_last_n = self.max_stored_images // 2  # Mantener la mitad por defecto
            
            # Obtener todas las imágenes ordenadas por fecha
            all_images = []
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.join(root, file)
                        mtime = os.path.getmtime(full_path)
                        all_images.append((full_path, mtime))
            
            # Ordenar por fecha (más recientes al final)
            all_images.sort(key=lambda x: x[1])
            
            # Eliminar todas excepto las últimas keep_last_n
            deleted_count = 0
            if len(all_images) > keep_last_n:
                to_delete = all_images[:-keep_last_n]
                
                for path, _ in to_delete:
                    try:
                        os.remove(path)
                        deleted_count += 1
                    except OSError as e:
                        logger.warning(f"No se pudo eliminar {path}: {e}")
                
                # Limpiar directorios vacíos
                self._cleanup_empty_directories()
            
            logger.info(f"Limpieza forzada completada: {deleted_count} imágenes eliminadas, {keep_last_n} mantenidas")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error en limpieza forzada: {str(e)}")
            return 0