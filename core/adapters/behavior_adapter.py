import time
import logging

# 🆕 IMPORTS CORREGIDOS: Importar desde la raíz del proyecto
from behavior_detection_module import BehaviorDetectionModule  # Módulo principal en raíz
from client.utils.event_manager import EventManager

logger = logging.getLogger('behavior_adapter')

class BehaviorAdapter:
    """
    Adaptador para el detector de comportamientos que conecta con el sistema de sincronización.
    UBICACIÓN: core/adapters/behavior_adapter.py
    """
    def __init__(self):
        # Inicializar el detector original (desde raíz)
        self.detector = BehaviorDetectionModule()
        
        # Inicializar gestor de eventos (cliente)
        self.event_manager = EventManager()
        
        # Control de eventos
        self.last_cellphone_event = 0
        self.last_smoking_event = 0
        self.min_time_between_events = 60  # segundos
        
        logger.info("BehaviorAdapter inicializado desde core/adapters/")
    
    def detect_cellphone_and_sync(self, frame, operator_id=None):
        """
        Detecta uso de celular y registra el evento para sincronización.
        
        Args:
            frame: Imagen capturada de la cámara
            operator_id: ID del operador actual (opcional)
            
        Returns:
            dict: Resultado de la detección con información adicional
        """
        # Usar el detector original
        result = self.detector.detect_cellphone(frame)
        
        # Si se detecta uso de celular
        if result.get('cellphone_detected', False):
            # Evitar eventos duplicados
            if time.time() - self.last_cellphone_event > self.min_time_between_events:
                self.last_cellphone_event = time.time()
                
                # Preparar datos del evento
                event_data = {
                    'confidence': result.get('confidence', 0.0),
                    'bounding_box': result.get('bounding_box', [0, 0, 0, 0]),
                    'detection_time': time.time(),
                    'adapter_location': 'core/adapters/behavior_adapter.py'
                }
                
                # Registrar evento para sincronización
                event_id = self.event_manager.register_event(
                    event_type='cellphone',
                    event_data=event_data,
                    frame=frame,
                    operator_id=operator_id
                )
                
                # Añadir ID del evento al resultado
                result['event_id'] = event_id
                logger.warning(f"Uso de celular detectado. Evento registrado con ID: {event_id}")
        
        return result
    
    def detect_smoking_and_sync(self, frame, operator_id=None):
        """
        Detecta si está fumando y registra el evento para sincronización.
        
        Args:
            frame: Imagen capturada de la cámara
            operator_id: ID del operador actual (opcional)
            
        Returns:
            dict: Resultado de la detección con información adicional
        """
        # Usar el detector original
        result = self.detector.detect_smoking(frame)
        
        # Si se detecta que está fumando
        if result.get('smoking_detected', False):
            # Evitar eventos duplicados
            if time.time() - self.last_smoking_event > self.min_time_between_events:
                self.last_smoking_event = time.time()
                
                # Preparar datos del evento
                event_data = {
                    'confidence': result.get('confidence', 0.0),
                    'bounding_box': result.get('bounding_box', [0, 0, 0, 0]),
                    'detection_time': time.time(),
                    'adapter_location': 'core/adapters/behavior_adapter.py'
                }
                
                # Registrar evento para sincronización
                event_id = self.event_manager.register_event(
                    event_type='smoking',
                    event_data=event_data,
                    frame=frame,
                    operator_id=operator_id
                )
                
                # Añadir ID del evento al resultado
                result['event_id'] = event_id
                logger.warning(f"Fumando detectado. Evento registrado con ID: {event_id}")
        
        return result
    
    def detect_behaviors_and_sync(self, frame, face_locations=None, operator_id=None):
        """
        Detecta todos los comportamientos y sincroniza eventos.
        
        Args:
            frame: Imagen capturada de la cámara
            face_locations: Ubicaciones de rostros detectados
            operator_id: ID del operador actual (opcional)
            
        Returns:
            tuple: (detections, processed_frame, alerts)
        """
        # Usar el detector original para obtener comportamientos
        detections, processed_frame, alerts = self.detector.detect_behaviors(frame, face_locations)
        
        # Procesar alertas para sincronización
        for alert_type, behavior, value in alerts:
            # Determinar tipo de evento basado en el comportamiento
            if 'phone' in alert_type or 'cellphone' in behavior.lower():
                event_type = 'cellphone'
            elif 'smoking' in alert_type or 'cigarette' in behavior.lower():
                event_type = 'smoking'
            else:
                event_type = 'behavior'  # Tipo genérico
            
            # Preparar datos del evento
            event_data = {
                'alert_type': alert_type,
                'behavior': behavior,
                'value': value,
                'detection_time': time.time(),
                'adapter_location': 'core/adapters/behavior_adapter.py'
            }
            
            # Verificar cooldown específico por tipo
            last_event_key = f'last_{event_type}_event'
            if not hasattr(self, last_event_key):
                setattr(self, last_event_key, 0)
            
            last_event_time = getattr(self, last_event_key)
            
            if time.time() - last_event_time > self.min_time_between_events:
                # Registrar evento
                event_id = self.event_manager.register_event(
                    event_type=event_type,
                    event_data=event_data,
                    frame=frame,
                    operator_id=operator_id
                )
                
                # Actualizar tiempo del último evento
                setattr(self, last_event_key, time.time())
                
                logger.warning(f"Comportamiento {behavior} detectado. Evento {event_type} registrado con ID: {event_id}")
        
        return detections, processed_frame, alerts
    
    def get_detector(self):
        """Método para acceder directamente al detector original"""
        return self.detector
    
    def get_adapter_info(self):
        """Información del adaptador para debugging"""
        return {
            'name': 'BehaviorAdapter',
            'location': 'core/adapters/behavior_adapter.py',
            'detector_type': type(self.detector).__name__,
            'last_cellphone_event': self.last_cellphone_event,
            'last_smoking_event': self.last_smoking_event,
            'min_time_between_events': self.min_time_between_events
        }