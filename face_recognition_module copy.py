import cv2
import face_recognition
import numpy as np
import pickle
import os
import logging
import pygame
import time

class FaceRecognitionModule:
    def __init__(self, operators_dir="operators", tolerance=0.6):
        self.operators_dir = operators_dir
        self.tolerance = tolerance
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.operators = {}
        self.logger = logging.getLogger('FaceRecognitionModule')

        # Inicializar pygame para audio
        pygame.mixer.init()
        self.ultimo_operador_id = None  # Para no repetir audio innecesariamente
        
        # Configuración para modo diurno/nocturno
        self.is_night_mode = False
        self.light_level = 0
        self.night_mode_threshold = 50  # Umbral para modo nocturno (0-255)
        
        # Deshabilitar sonidos si es necesario
        self.enable_sounds = False  # Cambiar a True para habilitar los sonidos
        
        # Personalización de colores según modo
        self.day_colors = {
            'name': (255, 0, 0),    # Blanco para nombres en modo día
            'landmarks': (0, 255, 255)  # Amarillo para puntos faciales en modo día
        }
        
        self.night_colors = {
            'name': (255, 0, 0),    # Gris claro para nombres en modo noche
            'landmarks': (0, 180, 180)  # Amarillo suave para puntos faciales en modo noche
        }

    def reproducir_audio(self, ruta):
        """Reproduce un archivo de audio si los sonidos están habilitados"""
        if not self.enable_sounds:
            return
            
        try:
            if os.path.exists(ruta):
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.play()
            else:
                self.logger.warning(f"Archivo de audio no encontrado: {ruta}")
        except Exception as e:
            self.logger.error(f"Error al reproducir audio: {e}")

    def load_operators(self):
        """Carga operadores desde archivo de encodings"""
        encodings_file = os.path.join(self.operators_dir, "encodings.pkl")

        if not os.path.exists(encodings_file):
            self.logger.warning(f"Archivo de encodings no encontrado: {encodings_file}")
            return False

        try:
            with open(encodings_file, 'rb') as f:
                data = pickle.load(f)
                self.known_face_encodings = data['encodings']
                self.known_face_names = data['names']
                self.known_face_ids = data['ids']
                self.operators = data['operators']

            self.logger.info(f"Operadores cargados: {len(self.operators)}")
            return True

        except Exception as e:
            self.logger.error(f"Error al cargar operadores: {str(e)}")
            return False

    def identify_operator(self, frame):
        """Identifica al operador en el frame actual"""
        if not self.known_face_encodings:
            return None
            
        # Detectar condiciones de iluminación para modo día/noche
        self._detect_lighting_conditions(frame)

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)

        if not face_locations:
            return None

        try:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding,
                    tolerance=self.tolerance
                )

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    operator_id = self.known_face_ids[best_match_index]
                    operator_info = self.operators[operator_id].copy()
                    operator_info['confidence'] = 1 - face_distances[best_match_index]

                    top, right, bottom, left = face_locations[0]
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    operator_info['face_location'] = (top, right, bottom, left)

                    # Reproducir audio solo si es un nuevo operador
                    if self.ultimo_operador_id != operator_id:
                        self.reproducir_audio("audio/bienvenido.mp3")
                        self.ultimo_operador_id = operator_id

                    return operator_info

            # Si nadie fue reconocido
            self.ultimo_operador_id = None
            self.reproducir_audio("audio/no_registrado.mp3")

        except Exception as e:
            self.logger.error(f"Error en reconocimiento facial: {str(e)}")

        return None
        
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
        
        # Notificar cambio de modo solo en el log (no en pantalla)
        if previous_mode != self.is_night_mode:
            mode_str = "NOCTURNO" if self.is_night_mode else "DIURNO"
            self.logger.info(f"Cambio a modo {mode_str} (Nivel de luz: {self.light_level:.1f})")

    def draw_operator_info(self, frame, operator_info):
        """Dibuja información del operador en el frame, sin recuadro facial"""
        # Seleccionar colores según el modo (día/noche)
        colors = self.night_colors if self.is_night_mode else self.day_colors
        
        if operator_info and 'face_location' in operator_info:
            top, right, bottom, left = operator_info['face_location']
            
            # Ya no dibujamos el recuadro facial
            # cv2.rectangle(frame, (left, top), (right, bottom), colors['face_box'], 2)

            # Dibujar puntos faciales (excluyendo ojos)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_landmarks_list = face_recognition.face_landmarks(rgb_frame)

            for landmarks in face_landmarks_list:
                for feature, puntos in landmarks.items():
                    # Saltarse los ojos ("left_eye" y "right_eye")
                    if feature == "left_eye" or feature == "right_eye":
                        continue
                        
                    # Dibujar los demás puntos faciales
                    for (x, y) in puntos:
                        cv2.circle(frame, (x, y), 2, colors['landmarks'], -1)

            # Dibujar nombre al costado del rostro
            name_text = operator_info['name']
            cv2.putText(frame, name_text, (right + 10, top + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors['name'], 2)
                        
            # Dibujar nivel de confianza (opcional)
            confidence_text = f"Confianza: {operator_info['confidence']:.2f}"
            cv2.putText(frame, confidence_text, (right + 10, top + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors['name'], 1)
                        
        else:
            # Mensaje si no se reconoce operador
            cv2.putText(frame, "Operador no reconocido", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)