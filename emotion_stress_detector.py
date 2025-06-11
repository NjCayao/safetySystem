import time
import cv2
import numpy as np
from collections import deque
from scipy.spatial import distance

# 🆕 NUEVO: Importar sistema de configuración
try:
    from config.config_manager import get_config, has_gui
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("Sistema de configuración no disponible para EmotionStressDetector, usando valores por defecto")

class EmotionStressDetector:
    """
    🎭 Detector avanzado de emociones, estrés y estados psicológicos
    Módulo independiente para análisis completo del estado emocional del operador
    """
    
    def __init__(self):
        """Inicializa el detector con configuración externa"""
        
        # 🆕 NUEVO: Cargar configuración externa
        if CONFIG_AVAILABLE:
            self.config = {
                # Configuración de expresiones
                'expression_enabled': get_config('emotion.expression_enabled', True),
                'expression_sensitivity': get_config('emotion.expression_sensitivity', 0.7),
                'expression_memory_frames': get_config('emotion.expression_memory_frames', 10),
                'expression_threshold': get_config('emotion.expression_threshold', 0.65),
                
                # Configuración de fatiga emocional
                'fatigue_enabled': get_config('emotion.fatigue_enabled', True),
                'fatigue_ear_threshold': get_config('emotion.fatigue_ear_threshold', 0.25),
                'fatigue_time_window': get_config('emotion.fatigue_time_window', 60),
                
                # Configuración de estrés
                'stress_enabled': get_config('emotion.stress_enabled', True),
                'stress_facial_tension_threshold': get_config('emotion.stress_facial_tension_threshold', 0.6),
                'stress_micro_movement_threshold': get_config('emotion.stress_micro_movement_threshold', 0.3),
                'stress_time_window': get_config('emotion.stress_time_window', 30),
                
                # 🆕 NUEVAS: Configuraciones expandidas
                'anxiety_enabled': get_config('emotion.anxiety_enabled', True),
                'concentration_enabled': get_config('emotion.concentration_enabled', True),
                'mood_tracking_enabled': get_config('emotion.mood_tracking_enabled', True),
                'wellness_score_enabled': get_config('emotion.wellness_score_enabled', True),
                
                # Configuración visual
                'show_debug_info': get_config('emotion.show_debug_info', True),
                'show_emotion_history': get_config('emotion.show_emotion_history', True),
            }
            
            self.show_gui = has_gui()
            print(f"✅ EmotionStressDetector - Configuración cargada")
        else:
            # Fallback valores por defecto
            self.config = {
                'expression_enabled': True, 'expression_sensitivity': 0.7,
                'expression_memory_frames': 10, 'expression_threshold': 0.65,
                'fatigue_enabled': True, 'fatigue_ear_threshold': 0.25, 'fatigue_time_window': 60,
                'stress_enabled': True, 'stress_facial_tension_threshold': 0.6,
                'stress_micro_movement_threshold': 0.3, 'stress_time_window': 30,
                'anxiety_enabled': True, 'concentration_enabled': True,
                'mood_tracking_enabled': True, 'wellness_score_enabled': True,
                'show_debug_info': True, 'show_emotion_history': True,
            }
            self.show_gui = True
            print("⚠️ EmotionStressDetector usando configuración por defecto")
        
        # Variables de estado para expresiones
        self.expression_history = deque(maxlen=self.config['expression_memory_frames'])
        self.current_expression = "neutral"
        self.expression_confidence = 0.0
        
        # Variables de estado para fatiga emocional
        self.fatigue_percentage = 0
        self.blink_counter = 0
        self.blink_history = []
        self.last_blink_time = time.time()
        self.ear_history = deque(maxlen=30)
        
        # Variables de estado para estrés
        self.stress_percentage = 0
        self.facial_movement_history = deque(maxlen=20)
        self.last_landmarks = None
        
        # 🆕 NUEVAS: Variables expandidas
        self.anxiety_level = 0
        self.concentration_score = 100
        self.mood_history = deque(maxlen=50)  # Historial de estados de ánimo
        self.wellness_score = 100
        
        # Para análisis temporal
        self.emotion_timeline = deque(maxlen=100)  # Últimos 100 análisis
        self.stress_timeline = deque(maxlen=100)
        
        # Colores para visualización
        self.colors = {
            'happy': (0, 255, 0),      # Verde - Feliz
            'sad': (255, 0, 0),        # Azul - Triste  
            'angry': (0, 0, 255),      # Rojo - Enojado
            'surprised': (0, 255, 255), # Amarillo - Sorprendido
            'neutral': (255, 255, 255), # Blanco - Neutral
            'stress_low': (0, 255, 0),   # Verde - Estrés bajo
            'stress_medium': (0, 165, 255), # Naranja - Estrés medio
            'stress_high': (0, 0, 255),     # Rojo - Estrés alto
        }
        
        # Para logs en modo headless
        self._last_log_time = 0
        
        print("=== Detector de Emociones y Estrés Inicializado ===")
        print(f"Expresiones: {'✅' if self.config['expression_enabled'] else '❌'}")
        print(f"Fatiga emocional: {'✅' if self.config['fatigue_enabled'] else '❌'}")
        print(f"Estrés: {'✅' if self.config['stress_enabled'] else '❌'}")
        print(f"Ansiedad: {'✅' if self.config['anxiety_enabled'] else '❌'}")
        print(f"Concentración: {'✅' if self.config['concentration_enabled'] else '❌'}")
        print(f"GUI: {'✅' if self.show_gui else '❌'}")
    
    def analyze_complete_emotional_state(self, frame, face_landmarks):
        """
        🎭 MÉTODO PRINCIPAL: Analiza el estado emocional completo
        
        Args:
            frame: Imagen actual
            face_landmarks: Landmarks faciales detectados
            
        Returns:
            dict: Estado emocional completo del operador
        """
        current_time = time.time()
        
        if not face_landmarks:
            return self._get_default_emotional_state()
        
        # Análisis individual de cada componente
        emotional_state = {}
        
        # 😊 Análisis de expresiones básicas
        if self.config['expression_enabled']:
            expression, confidence = self._analyze_facial_expression(face_landmarks)
            emotional_state.update({
                'expression': expression,
                'expression_confidence': confidence
            })
        
        # 😴 Análisis de fatiga emocional
        if self.config['fatigue_enabled']:
            fatigue_level = self._analyze_emotional_fatigue(face_landmarks, current_time)
            emotional_state['fatigue_percentage'] = fatigue_level
        
        # 😰 Análisis de estrés
        if self.config['stress_enabled']:
            stress_level = self._analyze_stress_indicators(face_landmarks)
            emotional_state['stress_percentage'] = stress_level
        
        # 🆕 NUEVOS ANÁLISIS EXPANDIDOS
        
        # 😟 Análisis de ansiedad
        if self.config['anxiety_enabled']:
            anxiety_level = self._analyze_anxiety_indicators(face_landmarks)
            emotional_state['anxiety_level'] = anxiety_level
        
        # 🎯 Análisis de concentración
        if self.config['concentration_enabled']:
            concentration_score = self._analyze_concentration_level(face_landmarks)
            emotional_state['concentration_score'] = concentration_score
        
        # 📊 Tracking de estado de ánimo
        if self.config['mood_tracking_enabled']:
            mood_state = self._track_mood_changes(emotional_state)
            emotional_state['mood_state'] = mood_state
        
        # 💚 Score de bienestar general
        if self.config['wellness_score_enabled']:
            wellness_score = self._calculate_wellness_score(emotional_state)
            emotional_state['wellness_score'] = wellness_score
        
        # Guardar en timeline para análisis temporal
        self._update_emotional_timeline(emotional_state, current_time)
        
        return emotional_state
    
    def _analyze_facial_expression(self, face_landmarks):
        """😊 Analiza expresiones faciales básicas"""
        try:
            # Características de la boca
            mouth_width = self._distance_between_points(
                face_landmarks['top_lip'][0], face_landmarks['top_lip'][6]
            )
            
            lip_distance = self._average_distance_between_curves(
                face_landmarks['top_lip'], face_landmarks['bottom_lip']
            )
            
            mouth_height = self._distance_between_points(
                self._midpoint(face_landmarks['top_lip'][3], face_landmarks['top_lip'][4]),
                self._midpoint(face_landmarks['bottom_lip'][3], face_landmarks['bottom_lip'][4])
            )
            
            mouth_aspect_ratio = mouth_height / mouth_width if mouth_width > 0 else 0
            
            # Características de las cejas
            eyebrow_eye_dist = self._calculate_eyebrow_eye_distance(face_landmarks)
            
            # Normalización
            face_width = self._distance_between_points(
                face_landmarks['chin'][0], face_landmarks['chin'][16]
            )
            
            norm_mouth_ratio = mouth_aspect_ratio / face_width * 100
            norm_lip_distance = lip_distance / face_width * 100
            norm_eyebrow_dist = eyebrow_eye_dist / face_width * 100
            
            # Clasificación de expresiones
            expression = "neutral"
            confidence = 0.6
            
            if norm_mouth_ratio < 0.5 and norm_lip_distance < 1.0:
                expression = "happy"
                confidence = 0.8
            elif norm_eyebrow_dist > 1.5 and norm_mouth_ratio > 0.7:
                expression = "surprised"
                confidence = 0.75
            elif norm_eyebrow_dist < 0.8 and norm_mouth_ratio < 0.4:
                expression = "sad"
                confidence = 0.65
            elif norm_eyebrow_dist < 0.7:
                expression = "angry"
                confidence = 0.7
            
            # Suavizado con historial
            self.expression_history.append(expression)
            stable_expression = self._get_stable_expression()
            
            self.current_expression = stable_expression
            self.expression_confidence = confidence
            
            return stable_expression, confidence
            
        except Exception as e:
            return "neutral", 0.0
    
    def _analyze_emotional_fatigue(self, face_landmarks, current_time):
        """😴 Analiza fatiga emocional basada en patrones oculares"""
        try:
            # Calcular EAR (Eye Aspect Ratio)
            left_ear = self._calculate_ear(face_landmarks['left_eye'])
            right_ear = self._calculate_ear(face_landmarks['right_eye'])
            ear = (left_ear + right_ear) / 2.0
            
            self.ear_history.append(ear)
            
            # Detectar parpadeos
            is_eye_closed = ear < self.config['fatigue_ear_threshold']
            
            if is_eye_closed and self.last_blink_time < current_time - 0.2:
                self.blink_counter += 1
                self.blink_history.append(current_time)
                self.last_blink_time = current_time
            
            # Limpiar historial antiguo
            time_window = self.config['fatigue_time_window']
            self.blink_history = [t for t in self.blink_history if t > current_time - time_window]
            
            # Calcular métricas de fatiga
            blink_rate = len(self.blink_history) / time_window * 60
            avg_ear = sum(self.ear_history) / len(self.ear_history) if self.ear_history else 1.0
            
            # Calcular nivel de fatiga
            base_fatigue = 0
            
            if blink_rate > 20:
                base_fatigue += min(40, (blink_rate - 20) * 2)
            
            if avg_ear < 0.3:
                base_fatigue += min(30, (0.3 - avg_ear) * 100)
            
            if len(self.ear_history) > 5:
                ear_std = np.std(list(self.ear_history))
                if ear_std < 0.02:
                    base_fatigue += 15
            
            fatigue_level = max(0, min(100, int(base_fatigue)))
            self.fatigue_percentage = fatigue_level
            
            return fatigue_level
            
        except Exception as e:
            return 0
    
    def _analyze_stress_indicators(self, face_landmarks):
        """😰 Analiza indicadores de estrés facial"""
        try:
            # Tensión facial (distancia entre cejas)
            eyebrow_distance = self._distance_between_points(
                self._midpoint(face_landmarks['left_eyebrow'][0], face_landmarks['left_eyebrow'][1]),
                self._midpoint(face_landmarks['right_eyebrow'][4], face_landmarks['right_eyebrow'][3])
            )
            
            face_width = self._distance_between_points(
                face_landmarks['chin'][0], face_landmarks['chin'][16]
            )
            
            normalized_tension = eyebrow_distance / face_width
            
            # Micro-movimientos
            micro_movement = 0
            if self.last_landmarks:
                micro_movement = self._calculate_facial_micro_movements(face_landmarks, face_width)
            
            self.last_landmarks = face_landmarks.copy()
            self.facial_movement_history.append(micro_movement)
            
            # Calcular nivel de estrés
            tension_component = max(0, (0.5 - normalized_tension) * 100) if normalized_tension < 0.5 else 0
            
            movement_avg = sum(self.facial_movement_history) / len(self.facial_movement_history) if self.facial_movement_history else 0
            movement_component = min(50, movement_avg * 5)
            
            stress_level = int(tension_component * 0.6 + movement_component * 0.4)
            stress_level = max(0, min(100, stress_level))
            
            self.stress_percentage = stress_level
            return stress_level
            
        except Exception as e:
            return 0
    
    def _analyze_anxiety_indicators(self, face_landmarks):
        """😟 NUEVO: Analiza indicadores de ansiedad"""
        try:
            # Ansiedad basada en:
            # 1. Tensión en músculos faciales
            # 2. Asimetría facial
            # 3. Frecuencia de micro-expresiones
            
            # Calcular asimetría facial
            left_features = self._extract_left_face_features(face_landmarks)
            right_features = self._extract_right_face_features(face_landmarks)
            asymmetry_score = self._calculate_facial_asymmetry(left_features, right_features)
            
            # Tensión en zona de los ojos
            eye_tension = self._calculate_eye_area_tension(face_landmarks)
            
            # Combinar métricas
            anxiety_base = (asymmetry_score * 0.4 + eye_tension * 0.6) * 100
            anxiety_level = max(0, min(100, int(anxiety_base)))
            
            self.anxiety_level = anxiety_level
            return anxiety_level
            
        except Exception as e:
            return 0
    
    def _analyze_concentration_level(self, face_landmarks):
        """🎯 NUEVO: Analiza nivel de concentración"""
        try:
            # Concentración basada en:
            # 1. Estabilidad de la mirada
            # 2. Posición de las cejas
            # 3. Apertura de los ojos
            
            # Estabilidad ocular
            eye_stability = self._calculate_eye_stability(face_landmarks)
            
            # Posición de cejas (concentración = cejas ligeramente contraídas)
            eyebrow_position = self._calculate_concentration_eyebrow_position(face_landmarks)
            
            # Apertura ocular (concentración = ojos bien abiertos pero no tensos)
            eye_openness = self._calculate_optimal_eye_openness(face_landmarks)
            
            # Score de concentración (100 = máxima concentración)
            concentration_base = (eye_stability * 0.4 + eyebrow_position * 0.3 + eye_openness * 0.3)
            concentration_score = max(0, min(100, int(concentration_base * 100)))
            
            self.concentration_score = concentration_score
            return concentration_score
            
        except Exception as e:
            return 50  # Valor neutro
    
    def _track_mood_changes(self, emotional_state):
        """📊 NUEVO: Tracking de cambios de estado de ánimo"""
        try:
            # Crear snapshot del estado actual
            mood_snapshot = {
                'timestamp': time.time(),
                'expression': emotional_state.get('expression', 'neutral'),
                'stress': emotional_state.get('stress_percentage', 0),
                'fatigue': emotional_state.get('fatigue_percentage', 0),
                'anxiety': emotional_state.get('anxiety_level', 0),
            }
            
            self.mood_history.append(mood_snapshot)
            
            # Analizar tendencias
            if len(self.mood_history) >= 5:
                recent_moods = list(self.mood_history)[-5:]
                mood_trend = self._analyze_mood_trend(recent_moods)
                return mood_trend
            
            return "stable"
            
        except Exception as e:
            return "unknown"
    
    def _calculate_wellness_score(self, emotional_state):
        """💚 NUEVO: Calcula score de bienestar general"""
        try:
            # Factores que afectan el bienestar:
            stress_factor = max(0, 100 - emotional_state.get('stress_percentage', 0))
            fatigue_factor = max(0, 100 - emotional_state.get('fatigue_percentage', 0))
            anxiety_factor = max(0, 100 - emotional_state.get('anxiety_level', 0))
            concentration_factor = emotional_state.get('concentration_score', 50)
            
            # Bonus por expresiones positivas
            expression_bonus = 10 if emotional_state.get('expression') == 'happy' else 0
            expression_penalty = -10 if emotional_state.get('expression') in ['sad', 'angry'] else 0
            
            # Calcular wellness score
            wellness_base = (
                stress_factor * 0.3 +
                fatigue_factor * 0.3 +
                anxiety_factor * 0.2 +
                concentration_factor * 0.2
            )
            
            wellness_score = max(0, min(100, int(wellness_base + expression_bonus + expression_penalty)))
            
            self.wellness_score = wellness_score
            return wellness_score
            
        except Exception as e:
            return 50  # Valor neutro
    
    def _update_emotional_timeline(self, emotional_state, current_time):
        """📈 Actualiza timeline emocional para análisis temporal"""
        timeline_entry = {
            'timestamp': current_time,
            'emotional_state': emotional_state.copy()
        }
        
        self.emotion_timeline.append(timeline_entry)
    
    def draw_emotional_analysis(self, frame, emotional_state):
        """🎨 Dibuja análisis emocional en el frame"""
        if not self.show_gui:
            return frame
        
        h, w = frame.shape[:2]
        
        # Panel de información emocional
        panel_x = w - 300
        panel_y = 50
        
        # Fondo del panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x - 10, panel_y - 10), 
                     (w - 10, panel_y + 300), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Título
        cv2.putText(frame, "ANALISIS EMOCIONAL", (panel_x, panel_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        y_offset = panel_y + 50
        
        # Expresión actual
        expression = emotional_state.get('expression', 'neutral')
        confidence = emotional_state.get('expression_confidence', 0)
        exp_color = self.colors.get(expression, (255, 255, 255))
        cv2.putText(frame, f"Expresion: {expression.title()} ({confidence:.1%})",
                   (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, exp_color, 1)
        y_offset += 25
        
        # Métricas de estrés
        stress = emotional_state.get('stress_percentage', 0)
        stress_color = self._get_stress_color(stress)
        cv2.putText(frame, f"Estres: {stress}%",
                   (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, stress_color, 1)
        y_offset += 25
        
        # Fatiga emocional
        fatigue = emotional_state.get('fatigue_percentage', 0)
        fatigue_color = self._get_fatigue_color(fatigue)
        cv2.putText(frame, f"Fatiga: {fatigue}%",
                   (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, fatigue_color, 1)
        y_offset += 25
        
        # Ansiedad
        if 'anxiety_level' in emotional_state:
            anxiety = emotional_state['anxiety_level']
            anxiety_color = self._get_anxiety_color(anxiety)
            cv2.putText(frame, f"Ansiedad: {anxiety}%",
                       (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, anxiety_color, 1)
            y_offset += 25
        
        # Concentración
        if 'concentration_score' in emotional_state:
            concentration = emotional_state['concentration_score']
            conc_color = self._get_concentration_color(concentration)
            cv2.putText(frame, f"Concentracion: {concentration}%",
                       (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, conc_color, 1)
            y_offset += 25
        
        # Score de bienestar
        if 'wellness_score' in emotional_state:
            wellness = emotional_state['wellness_score']
            wellness_color = self._get_wellness_color(wellness)
            cv2.putText(frame, f"Bienestar: {wellness}%",
                       (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, wellness_color, 1)
            y_offset += 25
        
        # Estado de ánimo
        if 'mood_state' in emotional_state:
            mood = emotional_state['mood_state']
            cv2.putText(frame, f"Estado: {mood.title()}",
                       (panel_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    # =============== MÉTODOS AUXILIARES ===============
    
    def _get_default_emotional_state(self):
        """Retorna estado emocional por defecto cuando no hay landmarks"""
        return {
            'expression': 'neutral',
            'expression_confidence': 0.0,
            'stress_percentage': 0,
            'fatigue_percentage': 0,
            'anxiety_level': 0,
            'concentration_score': 50,
            'wellness_score': 50,
            'mood_state': 'unknown'
        }
    
    def _distance_between_points(self, p1, p2):
        """Calcula distancia euclidiana entre dos puntos"""
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def _midpoint(self, p1, p2):
        """Calcula punto medio entre dos puntos"""
        return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    
    def _calculate_ear(self, eye_points):
        """Calcula Eye Aspect Ratio"""
        A = self._distance_between_points(eye_points[1], eye_points[5])
        B = self._distance_between_points(eye_points[2], eye_points[4])
        C = self._distance_between_points(eye_points[0], eye_points[3])
        return (A + B) / (2.0 * C) if C > 0 else 1.0
    
    def _average_distance_between_curves(self, curve1, curve2):
        """Calcula distancia promedio entre dos curvas"""
        total_dist = 0
        count = 0
        for i in range(min(len(curve1), len(curve2))):
            dist = self._distance_between_points(curve1[i], curve2[i])
            total_dist += dist
            count += 1
        return total_dist / count if count > 0 else 0
    
    def _get_stable_expression(self):
        """Obtiene expresión estable basada en historial"""
        if not self.expression_history:
            return "neutral"
        
        counts = {}
        for expr in self.expression_history:
            counts[expr] = counts.get(expr, 0) + 1
        
        most_common = max(counts.items(), key=lambda x: x[1])
        
        if most_common[1] / len(self.expression_history) >= 0.4:
            return most_common[0]
        else:
            return "neutral"
    
    # Métodos auxiliares para nuevas funcionalidades (implementar según necesidad)
    def _calculate_eyebrow_eye_distance(self, face_landmarks):
        """Calcula distancia promedio entre cejas y ojos"""
        left_dist = self._distance_between_points(
            self._midpoint(face_landmarks['left_eyebrow'][2], face_landmarks['left_eyebrow'][3]),
            self._midpoint(face_landmarks['left_eye'][1], face_landmarks['left_eye'][2])
        )
        right_dist = self._distance_between_points(
            self._midpoint(face_landmarks['right_eyebrow'][2], face_landmarks['right_eyebrow'][3]),
            self._midpoint(face_landmarks['right_eye'][1], face_landmarks['right_eye'][2])
        )
        return (left_dist + right_dist) / 2
    
    def _calculate_facial_micro_movements(self, current_landmarks, face_width):
        """Calcula micro-movimientos faciales"""
        if not self.last_landmarks:
            return 0
        
        movement_sum = 0
        point_count = 0
        
        for feature in current_landmarks:
            if feature in self.last_landmarks:
                for i, point in enumerate(current_landmarks[feature]):
                    if i < len(self.last_landmarks[feature]):
                        movement = self._distance_between_points(
                            point, self.last_landmarks[feature][i]
                        )
                        movement_sum += movement
                        point_count += 1
        
        return (movement_sum / point_count / face_width * 100) if point_count > 0 else 0
    
    # Métodos de colorización para visualización
    def _get_stress_color(self, stress_level):
        """Retorna color basado en nivel de estrés"""
        if stress_level < 30:
            return self.colors['stress_low']
        elif stress_level < 70:
            return self.colors['stress_medium']
        else:
            return self.colors['stress_high']
    
    def _get_fatigue_color(self, fatigue_level):
        """Retorna color basado en nivel de fatiga"""
        if fatigue_level < 30:
            return (0, 255, 0)  # Verde
        elif fatigue_level < 70:
            return (0, 165, 255)  # Naranja
        else:
            return (0, 0, 255)  # Rojo
    
    def _get_anxiety_color(self, anxiety_level):
        """Retorna color basado en nivel de ansiedad"""
        if anxiety_level < 30:
            return (0, 255, 0)
        elif anxiety_level < 60:
            return (0, 255, 255)
        else:
            return (0, 0, 255)
    
    def _get_concentration_color(self, concentration_score):
        """Retorna color basado en score de concentración"""
        if concentration_score > 70:
            return (0, 255, 0)  # Verde - Buena concentración
        elif concentration_score > 40:
            return (0, 165, 255)  # Naranja - Concentración media
        else:
            return (0, 0, 255)  # Rojo - Poca concentración
    
    def _get_wellness_color(self, wellness_score):
        """Retorna color basado en score de bienestar"""
        if wellness_score > 70:
            return (0, 255, 0)
        elif wellness_score > 40:
            return (0, 165, 255)
        else:
            return (0, 0, 255)
    
    # Placeholder methods para nuevas funcionalidades - IMPLEMENTAR SEGÚN NECESIDAD
    def _extract_left_face_features(self, face_landmarks):
        """Extrae características del lado izquierdo de la cara"""
        # TODO: Implementar extracción de características izquierdas
        return {}
    
    def _extract_right_face_features(self, face_landmarks):
        """Extrae características del lado derecho de la cara"""
        # TODO: Implementar extracción de características derechas
        return {}
    
    def _calculate_facial_asymmetry(self, left_features, right_features):
        """Calcula asimetría facial"""
        # TODO: Implementar cálculo de asimetría
        return 0
    
    def _calculate_eye_area_tension(self, face_landmarks):
        """Calcula tensión en el área de los ojos"""
        # TODO: Implementar cálculo de tensión ocular
        return 0
    
    def _calculate_eye_stability(self, face_landmarks):
        """Calcula estabilidad de la mirada"""
        # TODO: Implementar cálculo de estabilidad ocular
        return 0.5
    
    def _calculate_concentration_eyebrow_position(self, face_landmarks):
        """Calcula posición de cejas para concentración"""
        # TODO: Implementar análisis de posición de cejas
        return 0.5
    
    def _calculate_optimal_eye_openness(self, face_landmarks):
        """Calcula apertura ocular óptima"""
        # TODO: Implementar cálculo de apertura ocular
        return 0.5
    
    def _analyze_mood_trend(self, recent_moods):
        """Analiza tendencia del estado de ánimo"""
        # TODO: Implementar análisis de tendencias
        return "stable"
    
    def get_emotional_summary(self):
        """Retorna resumen del estado emocional actual"""
        return {
            'current_expression': self.current_expression,
            'expression_confidence': self.expression_confidence,
            'stress_percentage': self.stress_percentage,
            'fatigue_percentage': self.fatigue_percentage,
            'anxiety_level': self.anxiety_level,
            'concentration_score': self.concentration_score,
            'wellness_score': self.wellness_score
        }
    
    def update_config(self, new_config):
        """Actualiza configuración desde panel web"""
        self.config.update(new_config)
        print("Configuración de EmotionStressDetector actualizada")
    
    def get_config(self):
        """Retorna configuración actual"""
        return self.config.copy()