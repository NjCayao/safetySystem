import cv2
import numpy as np
import os
import logging
import time
from collections import deque
from alarm_module import AlarmModule

class BehaviorDetectionModule:
    def __init__(self, model_dir="models", audio_dir="audio", confidence_threshold=0.4):
        """
        Inicializa el módulo con todas las variables configurables al inicio
        """
        self.model_dir = model_dir
        self.audio_dir = audio_dir
        
        # === VARIABLES CONFIGURABLES DESDE PANEL WEB ===
        
        # Configuración de confianza para detección
        self.confidence_threshold = confidence_threshold  # Umbral de confianza diurno
        self.night_confidence_threshold = 0.35  # Umbral de confianza nocturno
        
        # Configuración de iluminación
        self.night_mode_threshold = 50  # Umbral para determinar modo nocturno (0-255)
        self.night_image_alpha = 1.3  # Factor de brillo para modo nocturno
        self.night_image_beta = 40  # Offset de brillo para modo nocturno
        
        # Configuración de tiempos para celular
        self.phone_alert_threshold_1 = 3  # Segundos para primera alerta
        self.phone_alert_threshold_2 = 7  # Segundos para alerta crítica
        
        # Configuración para detección de cigarro
        self.cigarette_pattern_window = 30  # Ventana de tiempo en segundos
        self.cigarette_pattern_threshold = 3  # Número de detecciones para patrón
        self.cigarette_continuous_threshold = 7  # Segundos para alerta continua anormal
        
        # Configuración de proximidad facial
        self.face_proximity_factor = 2  # Factor de distancia para determinar proximidad
        
        # Configuración de limpieza de detecciones
        self.detection_timeout = 1.0  # Segundos sin detección para limpiar comportamiento
        
        # Configuración de colores para visualización
        self.colors = {
            "cell phone": (0, 0, 255),    # Rojo para celular
            "cigarette": (0, 165, 255)    # Naranja para cigarro
        }
        
        # Configuración de tamaños de fuente y posiciones
        self.font_scale = 0.6
        self.font_thickness = 2
        self.timer_x_offset = 200  # Píxeles desde el borde derecho
        self.timer_y_center_ratio = 0.5  # Posición vertical (0.5 = centro)
        
        # Configuración de audio
        self.audio_enabled = True  # Habilitar/deshabilitar audio
        self.audio_keys = {
            "phone_3s": "telefono",      # Clave para alarm_module
            "phone_7s": "comportamiento10s",
            "smoking_pattern": "cigarro",
            "smoking_7s": "comportamiento10s"
        }
        
        # Configuración de alertas visuales
        self.alert_overlay_alpha = 0.3  # Transparencia de overlay de alerta
        self.alert_height = 60  # Altura de la barra de alerta
        
        # === FIN DE VARIABLES CONFIGURABLES ===
        
        # Inicialización del modelo y estado interno
        self.net = None
        self.classes = None
        self.target_classes = {
            "cell phone": {"id": None, "color": self.colors["cell phone"]},
            "cigarette": {"id": None, "color": self.colors["cigarette"]}
        }
        self.logger = logging.getLogger('BehaviorDetectionModule')
        
        # Inicializar módulo de alarma
        self.alarm = AlarmModule(audio_dir)
        # Inicializar el módulo de alarma
        if not self.alarm.initialize():
            self.logger.warning("No se pudo inicializar el módulo de alarma en BehaviorDetection")
        
        # Estado interno del módulo
        self.is_night_mode = False
        self.light_level = 0
        
        # Seguimiento de tiempo para comportamientos
        self.behavior_start_times = {}
        self.behavior_durations = {}
        self.last_detection_times = {}
        
        # Para detección de cigarro por frecuencia
        self.cigarette_detections = deque(maxlen=30)
        
        # Estados de reporte (usando nombres de BD)
        self.report_states = {
            "phone_3s": False,
            "phone_7s": False,
            "smoking_pattern": False,
            "smoking_7s": False
        }
        
        # Control de audio
        self.audio_states = {
            "phone_3s": False,
            "phone_7s": False,
            "smoking_pattern": False,
            "smoking_7s": False
        }
    
    def update_config(self, config_dict):
        """
        Actualiza la configuración del módulo desde un diccionario
        Útil para actualización desde panel web
        
        Args:
            config_dict: Diccionario con las configuraciones a actualizar
        """
        # Actualizar umbrales de confianza
        if 'confidence_threshold' in config_dict:
            self.confidence_threshold = config_dict['confidence_threshold']
        if 'night_confidence_threshold' in config_dict:
            self.night_confidence_threshold = config_dict['night_confidence_threshold']
        
        # Actualizar configuración de iluminación
        if 'night_mode_threshold' in config_dict:
            self.night_mode_threshold = config_dict['night_mode_threshold']
        if 'night_image_alpha' in config_dict:
            self.night_image_alpha = config_dict['night_image_alpha']
        if 'night_image_beta' in config_dict:
            self.night_image_beta = config_dict['night_image_beta']
        
        # Actualizar tiempos de alerta
        if 'phone_alert_threshold_1' in config_dict:
            self.phone_alert_threshold_1 = config_dict['phone_alert_threshold_1']
        if 'phone_alert_threshold_2' in config_dict:
            self.phone_alert_threshold_2 = config_dict['phone_alert_threshold_2']
        
        # Actualizar configuración de cigarro
        if 'cigarette_pattern_window' in config_dict:
            self.cigarette_pattern_window = config_dict['cigarette_pattern_window']
        if 'cigarette_pattern_threshold' in config_dict:
            self.cigarette_pattern_threshold = config_dict['cigarette_pattern_threshold']
        if 'cigarette_continuous_threshold' in config_dict:
            self.cigarette_continuous_threshold = config_dict['cigarette_continuous_threshold']
        
        # Actualizar otros parámetros
        if 'face_proximity_factor' in config_dict:
            self.face_proximity_factor = config_dict['face_proximity_factor']
        if 'detection_timeout' in config_dict:
            self.detection_timeout = config_dict['detection_timeout']
        if 'audio_enabled' in config_dict:
            self.audio_enabled = config_dict['audio_enabled']
        
        # Actualizar colores
        if 'colors' in config_dict:
            self.colors.update(config_dict['colors'])
            # Actualizar colores en target_classes
            self.target_classes["cell phone"]["color"] = self.colors["cell phone"]
            self.target_classes["cigarette"]["color"] = self.colors["cigarette"]
        
        self.logger.info("Configuración actualizada desde panel web")
    
    def get_config(self):
        """
        Retorna la configuración actual del módulo
        Útil para mostrar en panel web
        
        Returns:
            dict: Diccionario con toda la configuración actual
        """
        return {
            'confidence_threshold': self.confidence_threshold,
            'night_confidence_threshold': self.night_confidence_threshold,
            'night_mode_threshold': self.night_mode_threshold,
            'night_image_alpha': self.night_image_alpha,
            'night_image_beta': self.night_image_beta,
            'phone_alert_threshold_1': self.phone_alert_threshold_1,
            'phone_alert_threshold_2': self.phone_alert_threshold_2,
            'cigarette_pattern_window': self.cigarette_pattern_window,
            'cigarette_pattern_threshold': self.cigarette_pattern_threshold,
            'cigarette_continuous_threshold': self.cigarette_continuous_threshold,
            'face_proximity_factor': self.face_proximity_factor,
            'detection_timeout': self.detection_timeout,
            'audio_enabled': self.audio_enabled,
            'colors': self.colors,
            'is_night_mode': self.is_night_mode,
            'light_level': self.light_level
        }
    
    def initialize(self):
        """Inicializa el modelo de detección YOLO"""
        # Rutas a los archivos del modelo
        config_file = os.path.join(self.model_dir, "yolov3.cfg")
        weights_file = os.path.join(self.model_dir, "yolov3.weights")
        classes_file = os.path.join(self.model_dir, "coco.names")
        
        # Verificar si existen los archivos
        if not os.path.exists(config_file):
            self.logger.error(f"No se encontró el archivo de configuración: {config_file}")
            return False
        
        if not os.path.exists(weights_file):
            self.logger.error(f"No se encontró el archivo de pesos: {weights_file}")
            return False
        
        if not os.path.exists(classes_file):
            self.logger.error(f"No se encontró el archivo de clases: {classes_file}")
            return False
        
        try:
            # Cargar nombres de clases
            with open(classes_file, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]
            
            # Mapear IDs de clases objetivo
            for i, class_name in enumerate(self.classes):
                if class_name in self.target_classes:
                    self.target_classes[class_name]["id"] = i
            
            # Si "cigarette" no está en el conjunto de datos COCO, usar "bottle" como sustituto
            if self.target_classes["cigarette"]["id"] is None:
                for i, class_name in enumerate(self.classes):
                    if class_name == "bottle":
                        self.logger.info("'cigarette' no está en COCO, usando 'bottle' como sustituto")
                        self.target_classes["cigarette"]["id"] = i
                        break
            
            # Cargar la red neuronal
            self.net = cv2.dnn.readNetFromDarknet(config_file, weights_file)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            
            self.logger.info("Modelo YOLO cargado correctamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al cargar modelo YOLO: {str(e)}")
            return False
    
    def detect_behaviors(self, frame, face_locations=None):
        """
        Detecta comportamientos peligrosos en el frame
        
        Args:
            frame: Imagen donde detectar objetos
            face_locations: Lista de ubicaciones de rostros para verificar proximidad
            
        Returns:
            detections: Lista de comportamientos detectados
            frame: Frame con anotaciones
            alerts: Lista de alertas que necesitan ser manejadas por el sistema principal
        """
        alerts = []
        current_time = time.time()
        
        # Verificar que el modelo esté cargado
        if self.net is None or self.classes is None:
            if not self.initialize():
                return [], frame, alerts
        
        # Detectar condiciones de iluminación
        self._detect_lighting_conditions(frame)
        
        # Mejorar la imagen según las condiciones de iluminación
        enhanced_frame = self._enhance_image(frame)
        
        # Agregar indicador de modo
        frame = self._draw_mode_indicator(frame)
        
        height, width = enhanced_frame.shape[:2]
        
        # Crear blob desde la imagen mejorada
        blob = cv2.dnn.blobFromImage(enhanced_frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        
        # Pasar blob por la red
        self.net.setInput(blob)
        
        # Obtener capas de salida
        output_layers_names = self.net.getUnconnectedOutLayersNames()
        layer_outputs = self.net.forward(output_layers_names)
        
        # Inicializar listas
        boxes = []
        confidences = []
        class_ids = []
        
        # Determinar umbral de confianza según el modo
        current_threshold = self.night_confidence_threshold if self.is_night_mode else self.confidence_threshold
        
        # Procesar cada detección
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                # Filtrar por confianza y clases objetivo
                target_ids = [info["id"] for info in self.target_classes.values() if info["id"] is not None]
                if confidence > current_threshold and class_id in target_ids:
                    # Calcular coordenadas del objeto
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Coordenadas de la esquina superior izquierda
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Aplicar non-maximum suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, current_threshold, 0.4)
        
        detections = []
        detected_behaviors = set()
        
        # Verificar si hay detecciones
        if len(boxes) > 0 and len(indexes) > 0:
            try:
                # En OpenCV 4.5.4+, indexes es un vector de 1 dimensión
                if isinstance(indexes, np.ndarray) and indexes.ndim == 1:
                    indexes_flat = indexes
                else:
                    # En versiones anteriores, indexes es un vector anidado
                    indexes_flat = indexes.flatten()
                
                for i in indexes_flat:
                    x, y, w, h = boxes[i]
                    class_id = class_ids[i]
                    confidence = confidences[i]
                    
                    # Verificar si es una clase objetivo
                    for target_name, target_info in self.target_classes.items():
                        if target_info["id"] == class_id:
                            # Si hay rostros detectados, verificar proximidad
                            if face_locations:
                                near_face = False
                                for face_location in face_locations:
                                    # Convertir a coordenadas (x, y, w, h)
                                    if len(face_location) == 4:  # (top, right, bottom, left)
                                        top, right, bottom, left = face_location
                                        face_x = left
                                        face_y = top
                                        face_w = right - left
                                        face_h = bottom - top
                                        
                                        # Calcular centros
                                        obj_center_x = x + w/2
                                        obj_center_y = y + h/2
                                        face_center_x = face_x + face_w/2
                                        face_center_y = face_y + face_h/2
                                        
                                        # Calcular distancia entre centros
                                        distance_val = np.sqrt((obj_center_x - face_center_x)**2 + 
                                                            (obj_center_y - face_center_y)**2)
                                        
                                        # Normalizar por tamaño del rostro
                                        face_diag = np.sqrt(face_w**2 + face_h**2)
                                        
                                        # Objetos cerca del rostro
                                        if distance_val < face_diag * self.face_proximity_factor:
                                            near_face = True
                                            break
                                
                                if not near_face:
                                    continue
                            
                            # Comportamiento detectado
                            detected_behaviors.add(target_name)
                            
                            # Actualizar tiempos de detección
                            self.last_detection_times[target_name] = current_time
                            
                            # Dibujar rectángulo
                            color = target_info["color"]
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                            
                            # Añadir etiqueta
                            label = f"{target_name}: {confidence:.2f}"
                            cv2.putText(frame, label, (x, y - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            
                            # Añadir a detecciones
                            detections.append((target_name, confidence))
            except Exception as e:
                self.logger.error(f"Error al procesar detecciones: {str(e)}")
        
        # Procesar comportamientos detectados
        for behavior in detected_behaviors:
            if behavior == "cell phone":
                # Manejo de teléfono celular (detección por tiempo continuo)
                alerts.extend(self._process_cellphone_behavior(behavior, current_time))
            elif behavior == "cigarette":
                # Manejo de cigarro (detección por frecuencia)
                alerts.extend(self._process_cigarette_behavior(behavior, current_time))
        
        # Limpiar comportamientos no detectados
        self._cleanup_undetected_behaviors(detected_behaviors, current_time)
        
        # Dibujar contador de tiempo en pantalla
        frame = self._draw_behavior_timers(frame)
        
        return detections, frame, alerts
    
    def _process_cellphone_behavior(self, behavior, current_time):
        """Procesa comportamiento de uso de celular"""
        alerts = []
        
        # Iniciar contador si es primera detección
        if behavior not in self.behavior_start_times:
            self.behavior_start_times[behavior] = current_time
            self.behavior_durations[behavior] = 0
        
        # Actualizar duración
        self.behavior_durations[behavior] = current_time - self.behavior_start_times[behavior]
        duration = self.behavior_durations[behavior]
        
        # Alertas según duración (usando nombres de BD)
        if duration >= self.phone_alert_threshold_1 and not self.report_states["phone_3s"]:
            alerts.append(("phone_3s", behavior, duration))
            self.report_states["phone_3s"] = True
            
            # Reproducir audio si está habilitado
            if self.audio_enabled and not self.audio_states["phone_3s"]:
                self.alarm.play_alarm_threaded(self.audio_keys["phone_3s"])
                self.audio_states["phone_3s"] = True
        
        if duration >= self.phone_alert_threshold_2 and not self.report_states["phone_7s"]:
            alerts.append(("phone_7s", behavior, duration))
            self.report_states["phone_7s"] = True
            
            # Reproducir audio crítico si está habilitado
            if self.audio_enabled and not self.audio_states["phone_7s"]:
                self.alarm.play_alarm_threaded(self.audio_keys["phone_7s"])
                self.audio_states["phone_7s"] = True
        
        return alerts
    
    def _process_cigarette_behavior(self, behavior, current_time):
        """Procesa comportamiento de fumar (por frecuencia)"""
        alerts = []
        
        # Agregar detección actual
        self.cigarette_detections.append(current_time)
        
        # Limpiar detecciones antiguas (fuera de la ventana de tiempo)
        while self.cigarette_detections and (current_time - self.cigarette_detections[0]) > self.cigarette_pattern_window:
            self.cigarette_detections.popleft()
        
        # Contar detecciones en ventana
        detection_count = len(self.cigarette_detections)
        
        # Alerta por patrón de frecuencia (usando nombres de BD)
        if detection_count >= self.cigarette_pattern_threshold and not self.report_states["smoking_pattern"]:
            alerts.append(("smoking_pattern", behavior, detection_count))
            self.report_states["smoking_pattern"] = True
            
            # Reproducir audio si está habilitado
            if self.audio_enabled and not self.audio_states["smoking_pattern"]:
                self.alarm.play_alarm_threaded(self.audio_keys["smoking_pattern"])
                self.audio_states["smoking_pattern"] = True
        
        # También mantener duración para detección continua anormal
        if behavior not in self.behavior_start_times:
            self.behavior_start_times[behavior] = current_time
            self.behavior_durations[behavior] = 0
        
        self.behavior_durations[behavior] = current_time - self.behavior_start_times[behavior]
        duration = self.behavior_durations[behavior]
        
        # Alerta por duración continua anormal
        if duration >= self.cigarette_continuous_threshold and not self.report_states["smoking_7s"]:
            alerts.append(("smoking_7s", behavior, duration))
            self.report_states["smoking_7s"] = True
            
            # Reproducir audio crítico si está habilitado
            if self.audio_enabled and not self.audio_states["smoking_7s"]:
                self.alarm.play_alarm_threaded(self.audio_keys["smoking_7s"])
                self.audio_states["smoking_7s"] = True
        
        return alerts
    
    def _cleanup_undetected_behaviors(self, detected_behaviors, current_time):
        """Limpia comportamientos que ya no se detectan"""
        behaviors_to_remove = []
        
        for behavior in self.behavior_start_times:
            if behavior not in detected_behaviors:
                # Verificar si ha pasado suficiente tiempo sin detección
                if behavior in self.last_detection_times:
                    time_since_last = current_time - self.last_detection_times[behavior]
                    if time_since_last > self.detection_timeout:
                        behaviors_to_remove.append(behavior)
        
        # Limpiar comportamientos
        for behavior in behaviors_to_remove:
            if behavior in self.behavior_start_times:
                del self.behavior_start_times[behavior]
            if behavior in self.behavior_durations:
                del self.behavior_durations[behavior]
            
            # Resetear estados de reporte y audio para el comportamiento
            if behavior == "cell phone":
                self.report_states["phone_3s"] = False
                self.report_states["phone_7s"] = False
                self.audio_states["phone_3s"] = False
                self.audio_states["phone_7s"] = False
            elif behavior == "cigarette":
                self.report_states["smoking_pattern"] = False
                self.report_states["smoking_7s"] = False
                self.audio_states["smoking_pattern"] = False
                self.audio_states["smoking_7s"] = False
    
    def _draw_behavior_timers(self, frame):
        """Dibuja contadores de tiempo en pantalla"""
        h, w = frame.shape[:2]
        y_offset = int(h * self.timer_y_center_ratio)  # Centro vertical configurable
        x_position = w - self.timer_x_offset  # Lado derecho configurable
        
        # Fondo semitransparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (x_position - 10, y_offset - 40), 
                     (w - 10, y_offset + 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Mostrar duración de celular
        if "cell phone" in self.behavior_durations:
            duration = self.behavior_durations["cell phone"]
            color = self._get_timer_color(duration)
            text = f"Celular: {duration:.1f}s"
            cv2.putText(frame, text, (x_position, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, color, self.font_thickness)
        
        # Mostrar información de cigarro
        if "cigarette" in self.behavior_durations or len(self.cigarette_detections) > 0:
            y_offset += 30
            
            # Mostrar conteo de detecciones
            detection_count = len(self.cigarette_detections)
            color = (0, 255, 255) if detection_count < self.cigarette_pattern_threshold else (0, 0, 255)
            text = f"Cigarro: {detection_count} en {self.cigarette_pattern_window}s"
            cv2.putText(frame, text, (x_position, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, color, self.font_thickness)
            
            # Si hay duración continua, mostrarla también
            if "cigarette" in self.behavior_durations:
                duration = self.behavior_durations["cigarette"]
                if duration > 1.0:  # Solo mostrar si es significativo
                    y_offset += 25
                    color = self._get_timer_color(duration)
                    text = f"Continuo: {duration:.1f}s"
                    cv2.putText(frame, text, (x_position, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, self.font_scale * 0.8, color, self.font_thickness)
        
        return frame
    
    def _get_timer_color(self, duration):
        """Obtiene color según duración"""
        if duration < self.phone_alert_threshold_1:
            return (0, 255, 0)  # Verde
        elif duration < self.phone_alert_threshold_2:
            return (0, 255, 255)  # Amarillo
        else:
            return (0, 0, 255)  # Rojo
    
    def _detect_lighting_conditions(self, frame):
        """Detecta las condiciones de iluminación y determina si es modo nocturno"""
        # Convertir a escala de grises si no lo está
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
            
        # Calcular nivel promedio de iluminación (0-255)
        self.light_level = np.mean(gray)
        
        # Determinar si estamos en modo nocturno
        previous_mode = self.is_night_mode
        self.is_night_mode = self.light_level < self.night_mode_threshold
        
        # Notificar cambio de modo
        if previous_mode != self.is_night_mode:
            mode_str = "NOCTURNO" if self.is_night_mode else "DIURNO"
            self.logger.info(f"Cambio a modo {mode_str} (Nivel de luz: {self.light_level:.1f})")
    
    def _enhance_image(self, frame):
        """Mejora la imagen según condiciones de iluminación"""
        # Convertir a escala de grises si no lo está
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # En modo nocturno, aplicar más mejoras para infrarrojo
            if self.is_night_mode:
                # Normalizar histograma para mejorar contraste en IR
                enhanced_gray = cv2.equalizeHist(gray)
                
                # Reducir ruido para imágenes IR
                enhanced_gray = cv2.GaussianBlur(enhanced_gray, (5, 5), 0)
                
                # Convertir de nuevo a color
                enhanced = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)
                
                # Aumentar brillo y contraste con valores configurables
                enhanced = cv2.convertScaleAbs(enhanced, alpha=self.night_image_alpha, beta=self.night_image_beta)
            else:
                # En modo diurno, mejora de contraste más suave
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced_gray = clahe.apply(gray)
                
                # Convertir de nuevo a color
                enhanced = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)
        else:
            # Si ya está en escala de grises
            if self.is_night_mode:
                enhanced = cv2.equalizeHist(frame)
                enhanced = cv2.GaussianBlur(enhanced, (5, 5), 0)
                enhanced = cv2.convertScaleAbs(enhanced, alpha=self.night_image_alpha, beta=self.night_image_beta)
            else:
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(frame)
                
            # Convertir a color para detección
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        
        return enhanced
    
    def _draw_mode_indicator(self, frame):
        """Dibuja indicador de modo (día/noche)"""
        h, w = frame.shape[:2]
        mode_str = "MODO NOCTURNO" if self.is_night_mode else "MODO DIURNO"
        mode_color = (0, 150, 255) if self.is_night_mode else (255, 200, 0)
        
        # Ubicar en esquina superior izquierda
        x, y = 10, 30
        
        # Fondo semitransparente para el indicador
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-5, y-20), (x+180, y+10), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Agregar texto
        cv2.putText(frame, mode_str, (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, mode_color, 2)
        
        # Mostrar nivel de luz
        light_text = f"Luz: {self.light_level:.0f}"
        cv2.putText(frame, light_text, (x, y+30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def draw_behavior_alert(self, frame, behavior, confidence):
        """Dibuja una alerta visual para un comportamiento peligroso"""
        # Mostrar alerta en pantalla
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], self.alert_height), (0, 0, 200), -1)
        cv2.addWeighted(overlay, self.alert_overlay_alpha, frame, 1 - self.alert_overlay_alpha, 0, frame)
        
        # Mensaje de alerta
        alert_text = f"¡ALERTA! {behavior.upper()} DETECTADO"
        cv2.putText(frame, alert_text, (frame.shape[1]//2 - 200, self.alert_height//2 + 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        
        return frame