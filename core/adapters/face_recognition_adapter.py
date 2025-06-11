import time
import logging

# 🆕 IMPORTS CORREGIDOS: Importar desde la raíz del proyecto
from face_recognition_module import FaceRecognitionModule  # Módulo principal en raíz
from client.utils.event_manager import EventManager

logger = logging.getLogger('face_recognition_adapter')

class FaceRecognitionAdapter:
    """
    Adaptador para el reconocedor facial que conecta con el sistema de sincronización.
    UBICACIÓN: core/adapters/face_recognition_adapter.py
    """
    def __init__(self):
        # Inicializar el reconocedor original (desde raíz)
        self.recognizer = FaceRecognitionModule()
        
        # Inicializar gestor de eventos (cliente)
        self.event_manager = EventManager()
        
        # Control de eventos
        self.last_unrecognized_event = 0
        self.min_time_between_events = 60  # segundos
        
        logger.info("FaceRecognitionAdapter inicializado desde core/adapters/")
    
    def recognize_and_sync(self, frame):
        """
        Reconoce la cara del operador y registra eventos de operador no reconocido.
        
        Args:
            frame: Imagen capturada de la cámara
            
        Returns:
            dict: Resultado del reconocimiento con información adicional
        """
        # Usar el reconocedor original
        result = self.recognizer.identify_operator(frame)
        
        # Si no se reconoce al operador
        if not result or not result.get('recognized', False):
            # Evitar eventos duplicados
            if time.time() - self.last_unrecognized_event > self.min_time_between_events:
                self.last_unrecognized_event = time.time()
                
                # Preparar datos del evento
                event_data = {
                    'face_detected': result.get('face_detected', False) if result else False,
                    'confidence': result.get('confidence', 0.0) if result else 0.0,
                    'detection_time': time.time(),
                    'adapter_location': 'core/adapters/face_recognition_adapter.py'
                }
                
                # Registrar evento para sincronización
                event_id = self.event_manager.register_event(
                    event_type='unrecognized_operator',
                    event_data=event_data,
                    frame=frame
                )
                
                # Añadir ID del evento al resultado
                if result is None:
                    result = {}
                result['event_id'] = event_id
                logger.warning(f"Operador no reconocido. Evento registrado con ID: {event_id}")
        
        return result
    
    def identify_operator_and_sync(self, frame):
        """
        Alias para maintain compatibility. Método principal de reconocimiento.
        
        Args:
            frame: Imagen capturada de la cámara
            
        Returns:
            dict: Resultado del reconocimiento con información adicional
        """
        return self.recognize_and_sync(frame)
    
    def load_operators(self):
        """Cargar operadores en el reconocedor"""
        try:
            return self.recognizer.load_operators()
        except Exception as e:
            logger.error(f"Error cargando operadores: {e}")
            return False
    
    def draw_operator_info(self, frame, operator_info):
        """Dibujar información del operador en el frame"""
        try:
            return self.recognizer.draw_operator_info(frame, operator_info)
        except Exception as e:
            logger.error(f"Error dibujando información del operador: {e}")
            return frame
    
    def get_recognizer(self):
        """Método para acceder directamente al reconocedor original"""
        return self.recognizer
    
    def get_operators_count(self):
        """Obtener número de operadores cargados"""
        try:
            if hasattr(self.recognizer, 'operators'):
                return len(self.recognizer.operators)
            return 0
        except Exception as e:
            logger.error(f"Error obteniendo conteo de operadores: {e}")
            return 0
    
    def get_adapter_info(self):
        """Información del adaptador para debugging"""
        return {
            'name': 'FaceRecognitionAdapter',
            'location': 'core/adapters/face_recognition_adapter.py',
            'recognizer_type': type(self.recognizer).__name__,
            'last_unrecognized_event': self.last_unrecognized_event,
            'min_time_between_events': self.min_time_between_events,
            'operators_loaded': self.get_operators_count()
        }
    
    def reset_event_timers(self):
        """Resetear timers de eventos para testing"""
        self.last_unrecognized_event = 0
        logger.info("Timers de eventos reseteados")