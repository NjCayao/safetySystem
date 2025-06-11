# core/adapters/__init__.py
"""
Adaptadores del sistema de seguridad.
Estos adaptadores conectan los módulos de detección principales
con el sistema de sincronización y almacenamiento.
"""

__version__ = "1.0.0"

# Importar todos los adaptadores
try:
    from .fatigue_adapter import FatigueAdapter
except ImportError as e:
    print(f"Warning: No se pudo importar FatigueAdapter: {e}")
    FatigueAdapter = None

try:
    from .behavior_adapter import BehaviorAdapter
except ImportError as e:
    print(f"Warning: No se pudo importar BehaviorAdapter: {e}")
    BehaviorAdapter = None

try:
    from .face_recognition_adapter import FaceRecognitionAdapter
except ImportError as e:
    print(f"Warning: No se pudo importar FaceRecognitionAdapter: {e}")
    FaceRecognitionAdapter = None

# Lista de adaptadores disponibles
__all__ = []

if FatigueAdapter:
    __all__.append('FatigueAdapter')
if BehaviorAdapter:
    __all__.append('BehaviorAdapter')
if FaceRecognitionAdapter:
    __all__.append('FaceRecognitionAdapter')

def get_all_adapters():
    """
    Retorna diccionario con todos los adaptadores disponibles.
    
    Returns:
        dict: Diccionario con nombre -> clase de adaptador
    """
    adapters = {}
    
    if FatigueAdapter:
        adapters['fatigue'] = FatigueAdapter
    if BehaviorAdapter:
        adapters['behavior'] = BehaviorAdapter  
    if FatigueAdapter:
        adapters['face_recognition'] = FaceRecognitionAdapter
        
    return adapters

def create_adapter(adapter_type):
    """
    Factory para crear adaptadores por tipo.
    
    Args:
        adapter_type (str): Tipo de adaptador ('fatigue', 'behavior', 'face_recognition')
        
    Returns:
        Instancia del adaptador solicitado o None si no está disponible
    """
    adapters = get_all_adapters()
    
    if adapter_type in adapters:
        return adapters[adapter_type]()
    else:
        available = list(adapters.keys())
        raise ValueError(f"Adaptador '{adapter_type}' no disponible. Disponibles: {available}")

def test_adapters():
    """
    Función de prueba para verificar que todos los adaptadores se pueden instanciar.
    
    Returns:
        dict: Resultados de las pruebas
    """
    results = {}
    adapters = get_all_adapters()
    
    for name, adapter_class in adapters.items():
        try:
            instance = adapter_class()
            results[name] = {
                'status': 'success',
                'instance': instance,
                'methods': [method for method in dir(instance) 
                           if not method.startswith('_') and callable(getattr(instance, method))]
            }
        except Exception as e:
            results[name] = {
                'status': 'error',
                'error': str(e),
                'instance': None,
                'methods': []
            }
    
    return results