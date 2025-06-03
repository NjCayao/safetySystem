import cv2
import logging

class CameraModule:
    def __init__(self, camera_index=0, width=640, height=480, fps=30):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.camera = None
        self.logger = logging.getLogger('CameraModule')
        
    def initialize(self):
        """Inicializa la cámara con los parámetros especificados"""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            
            # Configurar parámetros
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reducir buffer para menor latencia
            
            if not self.camera.isOpened():
                self.logger.error(f"No se pudo abrir la cámara con índice {self.camera_index}")
                return False
            
            self.logger.info(f"Cámara inicializada: {self.width}x{self.height} @ {self.fps}fps")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al inicializar cámara: {str(e)}")
            return False
    
    def get_frame(self):
        """Captura y devuelve un frame de la cámara"""
        if self.camera is None or not self.camera.isOpened():
            if not self.initialize():
                return None
        
        ret, frame = self.camera.read()
        if not ret:
            self.logger.warning("Error al capturar frame")
            return None
        
        return frame
    
    def release(self):
        """Libera los recursos de la cámara"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            self.logger.info("Cámara liberada")