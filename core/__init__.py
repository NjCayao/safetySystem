# core/__init__.py
"""
Módulo core del Safety System.
Contiene adaptadores y componentes centrales del sistema.
"""

__version__ = "1.0.0"
__author__ = "Safety System Team"

# Importaciones principales para facilitar acceso
try:
    from .adapters.fatigue_adapter import FatigueAdapter
    from .adapters.behavior_adapter import BehaviorAdapter
    from .adapters.face_recognition_adapter import FaceRecognitionAdapter
    
    __all__ = [
        'FatigueAdapter',
        'BehaviorAdapter', 
        'FaceRecognitionAdapter'
    ]
    
except ImportError:
    # Los adaptadores serán importados cuando estén disponibles
    __all__ = []

def get_available_adapters():
    """Retorna lista de adaptadores disponibles"""
    available = []
    
    try:
        from .adapters.fatigue_adapter import FatigueAdapter
        available.append('FatigueAdapter')
    except ImportError:
        pass
    
    try:
        from .adapters.behavior_adapter import BehaviorAdapter
        available.append('BehaviorAdapter')
    except ImportError:
        pass
    
    try:
        from .adapters.face_recognition_adapter import FaceRecognitionAdapter
        available.append('FaceRecognitionAdapter')
    except ImportError:
        pass
    
    return available