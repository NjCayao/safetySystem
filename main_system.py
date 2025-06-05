import cv2
import os
import time
import logging
import traceback
import dlib
from datetime import datetime

# 🆕 NUEVO: Importar sistema de configuración
try:
    from config.config_manager import get_config, has_gui, is_development
    CONFIG_AVAILABLE = True
    print("✅ Sistema de configuración cargado")
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️ Sistema de configuración no disponible, usando valores por defecto")

# Importar módulos individuales
from camera_module import CameraModule
from face_recognition_module import FaceRecognitionModule
from fatigue_detection import FatigueDetector
from bostezo_detection import BostezosDetector
from distraction_detection import DistractionDetector
from alarm_module import AlarmModule
from behavior_detection_module import BehaviorDetectionModule

# Configuración de directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPERATORS_DIR = os.path.join(BASE_DIR, "operators")
MODEL_DIR = os.path.join(BASE_DIR, "models")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Asegurar que existan los directorios
for directory in [OPERATORS_DIR, MODEL_DIR, AUDIO_DIR, REPORTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# 🆕 NUEVO: Configuración de logging con configuración externa
if CONFIG_AVAILABLE:
    log_level = get_config('logging.level', 'INFO')
    log_format = get_config('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    log_level = 'INFO'
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=getattr(logging, log_level.upper()),
    format=log_format,
    filename=os.path.join(LOGS_DIR, f'safety_system_{datetime.now().strftime("%Y%m%d")}.log'),
    filemode='a'
)
logger = logging.getLogger('MainSystem')

class SafetySystem:
    def __init__(self):
        """Inicializa el sistema de seguridad modular"""
        self.logger = logging.getLogger('SafetySystem')
        self.logger.info("Iniciando sistema de seguridad modular")

        # 🆕 NUEVO: Cargar configuración
        if CONFIG_AVAILABLE:
            self.show_gui = has_gui()
            self.is_dev_mode = is_development()
            self.alert_cooldown = get_config('alerts.cooldown_time', 5)
            
            print(f"🔧 Configuración cargada:")
            print(f"   - Modo: {'DESARROLLO' if self.is_dev_mode else 'PRODUCCIÓN'}")
            print(f"   - GUI: {'HABILITADA' if self.show_gui else 'DESHABILITADA (headless)'}")
            print(f"   - Cooldown alertas: {self.alert_cooldown}s")
        else:
            # ✅ FALLBACK: Valores por defecto
            self.show_gui = True
            self.is_dev_mode = True
            self.alert_cooldown = 5
            print("⚠️ Usando configuración por defecto")

        # Definir el directorio de reportes
        self.reports_dir = REPORTS_DIR
        
        # Estado del sistema
        self.is_running = False
        self.current_operator = None
        
        # Tiempos para alertas
        self.last_alert_times = {
            "fatigue": 0,
            "cell_phone": 0,
            "cigarette": 0,
            "unauthorized": 0,
            "multiple_fatigue": 0,
            "yawn": 0,
            "multiple_yawns": 0,
            "distraction": 0,
            "distraction_level1": 0,  # Para alertas nivel 1
            "distraction_level2": 0,  # Para alertas nivel 2
            "multiple_distractions": 0,
            "phone_3s": 0,
            "phone_7s": 0,
            "smoking_pattern": 0,
            "smoking_7s": 0
        }
        
        # Estado de comportamientos (para manejar audio)
        self.behavior_audio_played = {
            "cell_phone": False,
            "cigarette": False
        }
        self.behavior_detection_start = {}
        
        # Variable para controlar si se reproducen sonidos del sistema principal
        self.play_system_audio = True  # Solo para alertas del sistema, no de comportamientos
        
        # Inicializar módulos
        self.camera = CameraModule()
        self.face_recognizer = FaceRecognitionModule(OPERATORS_DIR)
        
        # Ruta al detector de landmarks faciales
        landmark_path = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
        
        # Inicializar detectores individuales
        self.face_detector = None
        self.landmark_predictor = None
        self.fatigue_detector = FatigueDetector(landmark_path)
        self.bostezo_detector = BostezosDetector()
        self.distraction_detector = DistractionDetector()

        # Añadir detector de comportamientos (con directorio de audio)
        self.behavior_detector = BehaviorDetectionModule(MODEL_DIR, AUDIO_DIR)
        
        self.alarm = AlarmModule(AUDIO_DIR)
        
        # 🆕 NUEVO: Configurar ventana solo si GUI está habilitada
        if self.show_gui:
            cv2.namedWindow("Sistema de Seguridad", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Sistema de Seguridad", 800, 600)
            print("🖥️ Ventana gráfica configurada")
        else:
            print("🖥️ Modo headless - Sin interfaz gráfica")
    
    def initialize(self):
        """Inicializa todos los módulos del sistema"""
        logger.info("Inicializando módulos del sistema")
        print("Inicializando sistema de seguridad...")
        
        # Inicializar cámara
        if not self.camera.initialize():
            logger.error("Error al inicializar cámara")
            print("ERROR: No se pudo inicializar la cámara")
            return False
        
        # Cargar operadores
        if not self.face_recognizer.load_operators():
            logger.warning("No se pudieron cargar operadores")
            print("ADVERTENCIA: No se pudieron cargar operadores")
        
        # Inicializar detector facial y predictor de landmarks
        try:
            landmark_path = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
            self.face_detector = dlib.get_frontal_face_detector()
            self.landmark_predictor = dlib.shape_predictor(landmark_path)
            print("Detector facial y predictor de landmarks inicializados correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar detector facial: {str(e)}")
            print(f"ERROR: No se pudo inicializar el detector facial: {str(e)}")
            return False
        
        # Inicializar módulo de alarma
        if not self.alarm.initialize():
            logger.warning("Error al inicializar módulo de alarma")
            print("ADVERTENCIA: No se pudo inicializar el módulo de alarma")
        
        print("Sistema inicializado correctamente")
        return True
    
    def generate_report(self, frame, alert_type, operator_info=None, details=None):
        """Genera un reporte para una alerta detectada"""
        if self.current_operator is None and alert_type != "unauthorized":
            return
        
        try:
            # Crear nombre de archivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            operator_id = self.current_operator["id"] if self.current_operator else "unknown"
            
            # Convertir nombres de alerta a nombres compatibles con BD
            alert_type_db = alert_type
            if "phone" in alert_type:
                alert_type_db = "phone"
            elif "smoking" in alert_type:
                alert_type_db = "smoking"
            elif "multiple_distractions" in alert_type:
                alert_type_db = "distraction"  # Mapear multiple_distractions a distraction
            
            filename = f"{operator_id}_{alert_type_db}_{timestamp}.jpg"
            
            # Guardar imagen
            image_path = os.path.join(self.reports_dir, filename)
            cv2.imwrite(image_path, frame)

            # Crear un archivo de texto con detalles adicionales
            details_file = os.path.join(self.reports_dir, f"{operator_id}_{alert_type_db}_{timestamp}.txt")
            with open(details_file, 'w') as f:
                f.write(f"Reporte de Seguridad - {alert_type.upper()}\n")
                f.write(f"Fecha y hora: {timestamp}\n")
                f.write(f"Operador: {operator_info['name'] if operator_info else 'Desconocido'}\n")
                
                # Detalles específicos según el tipo de alerta
                if details:
                    if 'duration' in details:
                        f.write(f"Duración del comportamiento: {details['duration']:.1f} segundos\n")
                    if 'count' in details:
                        f.write(f"Número de detecciones: {details['count']}\n")
                    if 'behavior' in details:
                        f.write(f"Comportamiento detectado: {details['behavior']}\n")
                    if 'direction' in details:
                        f.write(f"Dirección de la mirada: {details['direction']}\n")
                    if 'level' in details:
                        f.write(f"Nivel de alerta alcanzado: {details['level']}\n")
                    if 'time_window' in details:
                        f.write(f"Tiempo de evaluación: {details['time_window']}\n")
                
                # Detalles específicos por tipo de alerta
                if 'fatigue' in alert_type:
                    f.write(f"Episodios de fatiga detectados: {self.fatigue_detector.get_microsleep_count()}\n")
                
                if 'yawn' in alert_type:
                    f.write(f"Bostezos detectados: {self.bostezo_detector.get_yawn_count()}\n")
                
                if 'distraction' in alert_type:
                    if 'multiple' in alert_type:
                        f.write("Patrón detectado: Múltiples distracciones en período corto\n")
                        f.write("ALERTA: Falta de atención recurrente\n")
                    else:
                        f.write("Distracción detectada: Mirada fuera del camino\n")
                        if details and details.get('level', 0) == 2:
                            f.write("ALERTA CRÍTICA: Distracción prolongada\n")
                
                if 'phone' in alert_type:
                    if '3s' in alert_type:
                        f.write("Uso de celular detectado por más de 3 segundos\n")
                    elif '7s' in alert_type:
                        f.write("Uso prolongado de celular detectado (más de 7 segundos)\n")
                        f.write("ALERTA CRÍTICA: Comportamiento peligroso sostenido\n")
                
                if 'smoking' in alert_type:
                    if 'pattern' in alert_type:
                        f.write("Patrón de fumar detectado (múltiples detecciones)\n")
                    elif '7s' in alert_type:
                        f.write("Comportamiento anormal: Cigarro detectado por más de 7 segundos continuos\n")
                
                f.write("\nAcción recomendada: El operador debe cesar el comportamiento peligroso inmediatamente.\n")
            
            self.logger.info(f"Reporte generado: {image_path} y {details_file}")
            
            # Aquí implementar el envío del reporte al servidor
            # self.send_report_to_server(image_path, details_file)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error al generar reporte: {str(e)}")
            traceback.print_exc()
            return False
    
    def start(self):
        """Inicia el sistema de seguridad"""
        logger.info("Sistema de seguridad iniciado")
        
        if not self.initialize():
            logger.error("Error al inicializar el sistema")
            return
        
        self.is_running = True
        
        # Para medir FPS
        prev_time = time.time()
        frame_count = 0
        
        # 🆕 NUEVO: Mostrar información de inicio
        print(f"\n🚀 SISTEMA INICIADO EN MODO {'DESARROLLO' if self.is_dev_mode else 'PRODUCCIÓN'}")
        print(f"   GUI: {'HABILITADA' if self.show_gui else 'DESHABILITADA'}")
        if self.show_gui:
            print("   Presiona 'q' para salir")
        else:
            print("   Presiona Ctrl+C para salir")
        print("-" * 50)
        
        try:
            while self.is_running:
                try:
                    # Capturar frame
                    frame = self.camera.get_frame()
                    
                    if frame is None:
                        logger.error("Error al capturar frame")
                        time.sleep(0.1)
                        continue
                    
                    # Calcular FPS
                    frame_count += 1
                    current_time = time.time()
                    if current_time - prev_time >= 1.0:
                        fps = frame_count / (current_time - prev_time)
                        frame_count = 0
                        prev_time = current_time
                    else:
                        fps = 0
                    
                    # 🆕 NUEVO: Mostrar FPS solo si GUI está habilitada
                    if self.show_gui:
                        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    else:
                        # En modo headless, log FPS cada 30 segundos
                        if frame_count % 300 == 0:  # Asumiendo ~10 FPS en Pi
                            print(f"📊 FPS: {fps:.2f} | Frames procesados: {frame_count}")
                    
                    # Reconocimiento facial
                    if self.current_operator is None:
                        operator = self.face_recognizer.identify_operator(frame)
                        if operator:
                            logger.info(f"Operador reconocido: {operator['name']} (ID: {operator['id']})")
                            self.current_operator = operator
                            print(f"👤 Operador reconocido: {operator['name']}")
                            
                            # Saludar al operador (solo si está habilitado el audio del sistema)
                            if self.play_system_audio:
                                self.alarm.play_alarm_threaded("greeting")
                    else:
                        # Verificar periódicamente que sigue siendo el mismo operador
                        if current_time % 5 < 0.1:  # Cada 5 segundos aproximadamente
                            operator = self.face_recognizer.identify_operator(frame)
                            if operator and operator['id'] != self.current_operator['id']:
                                logger.warning(f"Cambio de operador detectado: {operator['name']}")
                                self.current_operator = operator
                                print(f"🔄 Cambio de operador: {operator['name']}")
                                
                                # Saludar al nuevo operador (solo si está habilitado el audio del sistema)
                                if self.play_system_audio:
                                    self.alarm.play_alarm_threaded("greeting")
                    
                    # Mostrar información del operador
                    self.face_recognizer.draw_operator_info(frame, self.current_operator)
                    
                    # Detección facial y landmarks (una sola vez para todos los detectores)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.face_detector(gray, 0)
                    
                    # Solo procesar si se detecta un rostro
                    if self.current_operator and faces:
                        # Obtener landmarks para el primer rostro detectado
                        landmarks = self.landmark_predictor(gray, faces[0])
                        
                        # Detección de fatiga (microsueños)
                        fatigue_detected, multiple_fatigue, frame = self.fatigue_detector.detect(frame)
                        
                        # Detección de bostezos
                        is_yawning, multiple_yawns = self.bostezo_detector.detect(landmarks, frame)
                        
                        # Detección de distracciones
                        distraction, multiple_distractions = self.distraction_detector.detect(landmarks, frame)
                        
                        current_time = time.time()
                        
                        # Manejar fatiga detectada
                        if fatigue_detected:
                            # Verificar cooldown
                            if current_time - self.last_alert_times.get("fatigue", 0) > self.alert_cooldown:
                                logger.warning(f"Fatiga detectada para operador {self.current_operator['name']}")
                                print(f"⚠️ FATIGA DETECTADA - {self.current_operator['name']}")
                                
                                # Reproducir alarma (solo si está habilitado el audio del sistema)
                                if self.play_system_audio:
                                    self.alarm.play_alarm_threaded("fatigue")
                                
                                # Generar reporte
                                self.generate_report(frame, "fatigue", self.current_operator)
                                
                                # Actualizar tiempo de última alerta
                                self.last_alert_times["fatigue"] = current_time
                        
                        # Manejar múltiples episodios de fatiga
                        if multiple_fatigue:
                            # Verificar cooldown
                            if current_time - self.last_alert_times.get("multiple_fatigue", 0) > self.alert_cooldown:
                                logger.warning(f"Múltiples episodios de fatiga para operador {self.current_operator['name']}")
                                print(f"🚨 MÚLTIPLE FATIGA - {self.current_operator['name']}")
                                
                                # Reproducir alarma (solo si está habilitado el audio del sistema)
                                if self.play_system_audio:
                                    self.alarm.play_alarm_threaded("recomendacion")
                                
                                # Generar reporte
                                self.generate_report(frame, "multiple_fatigue", self.current_operator)
                                
                                # Actualizar tiempo de última alerta
                                self.last_alert_times["multiple_fatigue"] = current_time
                        
                        # Manejar bostezos individuales también
                        if is_yawning:
                            # Verificar cooldown
                            if current_time - self.last_alert_times.get("yawn", 0) > self.alert_cooldown:
                                logger.warning(f"Bostezo detectado para operador {self.current_operator['name']}")
                                print(f"🥱 BOSTEZO - {self.current_operator['name']}")
                                
                                # Generar reporte
                                self.generate_report(frame, "yawn", self.current_operator)
                                
                                # Actualizar tiempo de última alerta
                                self.last_alert_times["yawn"] = current_time
                        
                        # Manejar múltiples bostezos
                        if multiple_yawns:
                            # Verificar cooldown
                            if current_time - self.last_alert_times.get("multiple_yawns", 0) > self.alert_cooldown:
                                logger.warning(f"Múltiples bostezos detectados para operador {self.current_operator['name']}")
                                print(f"🥱🥱 MÚLTIPLES BOSTEZOS - {self.current_operator['name']}")
                                
                                # Generar reporte
                                self.generate_report(frame, "yawn", self.current_operator)
                                
                                # Actualizar tiempo de última alerta
                                self.last_alert_times["multiple_yawns"] = current_time
                        
                        # Manejar distracciones con niveles
                        if distraction:
                            # Obtener el estado actual del detector de distracciones
                            distraction_status = self.distraction_detector.get_status()
                            current_level = distraction_status['current_alert_level']
                            
                            # Generar reporte cuando se alcanza nivel 1 (2.5 segundos)
                            if current_level == 1 and current_time != self.last_alert_times.get("distraction_level1", 0):
                                if current_time - self.last_alert_times.get("distraction", 0) > self.alert_cooldown:
                                    logger.warning(f"Distracción nivel 1 detectada para operador {self.current_operator['name']}")
                                    print(f"👀 DISTRACCIÓN NIVEL 1 - {self.current_operator['name']}")
                                    
                                    details = {
                                        'direction': distraction_status['direction'],
                                        'duration': self.distraction_detector.config['level1_time'],
                                        'level': 1
                                    }
                                    
                                    self.generate_report(frame, "distraction", self.current_operator, details)
                                    self.last_alert_times["distraction_level1"] = current_time
                                    self.last_alert_times["distraction"] = current_time
                            
                            # Generar reporte cuando se alcanza nivel 2 (4.5 segundos)
                            elif current_level == 2 and current_time != self.last_alert_times.get("distraction_level2", 0):
                                if current_time - self.last_alert_times.get("distraction", 0) > self.alert_cooldown:
                                    logger.warning(f"Distracción nivel 2 detectada para operador {self.current_operator['name']}")
                                    print(f"👀👀 DISTRACCIÓN NIVEL 2 - {self.current_operator['name']}")
                                    
                                    details = {
                                        'direction': distraction_status['direction'],
                                        'duration': self.distraction_detector.config['level2_time'],
                                        'level': 2
                                    }
                                    
                                    self.generate_report(frame, "distraction", self.current_operator, details)
                                    self.last_alert_times["distraction_level2"] = current_time
                                    self.last_alert_times["distraction"] = current_time
                        
                        # Manejar múltiples distracciones
                        if multiple_distractions:
                            # Verificar cooldown
                            if current_time - self.last_alert_times.get("multiple_distractions", 0) > self.alert_cooldown:
                                logger.warning(f"Múltiples distracciones detectadas para operador {self.current_operator['name']}")
                                print(f"👀🔄 MÚLTIPLES DISTRACCIONES - {self.current_operator['name']}")
                                
                                # Obtener información adicional
                                distraction_status = self.distraction_detector.get_status()
                                
                                # Preparar detalles para el reporte
                                details = {
                                    'count': distraction_status['total_distractions'],
                                    'time_window': '10 minutos'
                                }
                                
                                # Generar reporte
                                self.generate_report(frame, "multiple_distractions", self.current_operator, details)
                                
                                # Actualizar tiempo de última alerta
                                self.last_alert_times["multiple_distractions"] = current_time
                        
                        # Detección de comportamientos peligrosos
                        face_locations = [(faces[0].top(), faces[0].right(), faces[0].bottom(), faces[0].left())]
                        behaviors, frame, behavior_alerts = self.behavior_detector.detect_behaviors(frame, face_locations)
                        
                        # Procesar alertas de comportamiento del módulo
                        for alert_type, behavior, value in behavior_alerts:
                            # Verificar cooldown
                            if current_time - self.last_alert_times.get(alert_type, 0) > self.alert_cooldown:
                                logger.warning(f"Alerta de comportamiento: {alert_type} - {behavior}")
                                print(f"📱 COMPORTAMIENTO PELIGROSO: {behavior.upper()} - {self.current_operator['name']}")
                                
                                # Preparar detalles para el reporte
                                details = {
                                    'behavior': behavior,
                                }
                                
                                if isinstance(value, float):
                                    details['duration'] = value
                                elif isinstance(value, int):
                                    details['count'] = value
                                
                                # NOTA: El audio es manejado por behavior_detection_module, no aquí
                                
                                # Generar reporte
                                self.generate_report(frame, alert_type, self.current_operator, details)
                                
                                # Actualizar tiempo de última alerta
                                self.last_alert_times[alert_type] = current_time
                                
                                # Mostrar alerta visual crítica
                                if '7s' in alert_type:
                                    frame = self.behavior_detector.draw_behavior_alert(frame, behavior, 1.0)
                    
                    # 🆕 NUEVO: Mostrar frame solo si GUI está habilitada
                    if self.show_gui:
                        cv2.imshow("Sistema de Seguridad", frame)
                        
                        # Salir si se presiona 'q'
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            print("👋 Saliendo del sistema...")
                            break
                    else:
                        # En modo headless, pequeña pausa para no saturar CPU
                        time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error en bucle principal: {str(e)}")
                    traceback.print_exc()
                    time.sleep(0.1)
            
        except KeyboardInterrupt:
            logger.info("Sistema detenido por el usuario")
            print("\n👋 Sistema detenido por el usuario")
        finally:
            self.stop()
    
    def stop(self):
        """Detiene el sistema y libera recursos"""
        logger.info("Deteniendo sistema")
        print("🛑 Deteniendo sistema...")
        self.is_running = False
        self.camera.release()
        
        # 🆕 NUEVO: Solo destruir ventanas si GUI estaba habilitada
        if self.show_gui:
            cv2.destroyAllWindows()
        
        print("✅ Sistema detenido correctamente")

if __name__ == "__main__":
    try:
        system = SafetySystem()
        system.start()
    except Exception as e:
        logger.critical(f"Error crítico en el sistema: {str(e)}")
        traceback.print_exc()
        
        # Mantener la ventana abierta para ver el error
        input("\nPresiona Enter para salir...")