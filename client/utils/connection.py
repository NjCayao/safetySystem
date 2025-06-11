import requests
import time
import logging
import threading

# 🆕 CAMBIO: Usar adaptador YAML en lugar de ConfigParser
from client.config.yaml_config_adapter import get_yaml_config

# Cargar configuración desde YAML
config = get_yaml_config()

logger = logging.getLogger('connection')

class ConnectionManager:
    def __init__(self, db, api_client):
        self.db = db
        self.api_client = api_client
        self.check_interval = config.getint('CONNECTION', 'check_interval')
        self.is_running = False
        self.thread = None
        
        # Log de configuración cargada
        logger.info(f"ConnectionManager inicializado:")
        logger.info(f"  Check interval: {self.check_interval}s")
        logger.info(f"  Retry attempts: {config.getint('CONNECTION', 'retry_attempts')}")
        logger.info(f"  Retry delay: {config.getint('CONNECTION', 'retry_delay')}s")
    
    def start_monitoring(self):
        """Iniciar monitoreo de conexión en un hilo separado"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Monitoreo de conexión iniciado")
    
    def stop_monitoring(self):
        """Detener monitoreo de conexión"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
            logger.info("Monitoreo de conexión detenido")
    
    def _monitor_loop(self):
        """Bucle principal de monitoreo"""
        while self.is_running:
            is_online = self.check_connection()
            self.db.update_connection_status(is_online)
            
            # Si estamos en línea, intentar autenticar
            if is_online and not self.api_client.is_token_valid():
                auth_result = self.api_client.authenticate()
                if auth_result:
                    logger.info("Autenticación exitosa durante monitoreo")
                else:
                    logger.warning("Fallo de autenticación durante monitoreo")
            
            time.sleep(self.check_interval)
    
    def check_connection(self):
        """Verificar si hay conexión a internet"""
        try:
            # Intentar conectar a un servicio confiable
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def check_server_connection(self):
        """Verificar conexión específicamente con nuestro servidor"""
        try:
            # Obtener URL del servidor desde configuración
            server_url = config.get('SERVER', 'api_url')
            if not server_url:
                logger.error("URL del servidor no configurada")
                return False
            
            # Hacer una petición simple al servidor
            response = requests.get(f"{server_url}/health", timeout=10)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.debug(f"Error conectando al servidor: {str(e)}")
            return False
    
    def get_status(self):
        """Obtener estado actual de conexión"""
        return self.db.get_connection_status()
    
    def is_online(self):
        """Verificar si actualmente estamos en línea"""
        return self.check_connection()
    
    def wait_for_connection(self, timeout=None):
        """Esperar hasta que haya conexión o se alcance el tiempo de espera"""
        start_time = time.time()
        while not self.check_connection():
            if timeout and (time.time() - start_time > timeout):
                logger.warning(f"Timeout esperando conexión después de {timeout}s")
                return False
            logger.info("Esperando conexión...")
            time.sleep(5)
        logger.info("Conexión establecida")
        return True
    
    def test_full_connectivity(self):
        """Prueba completa de conectividad (internet + servidor + autenticación)"""
        results = {
            'internet': False,
            'server': False,
            'authentication': False,
            'details': {}
        }
        
        # Probar conexión a internet
        try:
            response = requests.get("https://www.google.com", timeout=5)
            results['internet'] = response.status_code == 200
            results['details']['internet_status'] = response.status_code
        except Exception as e:
            results['details']['internet_error'] = str(e)
        
        # Probar conexión al servidor
        if results['internet']:
            results['server'] = self.check_server_connection()
            if results['server']:
                results['details']['server_status'] = 'reachable'
            else:
                results['details']['server_status'] = 'unreachable'
        
        # Probar autenticación
        if results['server']:
            try:
                results['authentication'] = self.api_client.authenticate()
                results['details']['auth_status'] = 'success' if results['authentication'] else 'failed'
            except Exception as e:
                results['details']['auth_error'] = str(e)
        
        return results