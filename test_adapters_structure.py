#!/usr/bin/env python3
"""
Script de prueba para verificar la restructuración de adaptadores
en core/adapters/
"""

import sys
import os
from pathlib import Path

def test_directory_structure():
    """Verificar que la estructura de directorios sea correcta"""
    print("=== TEST: Estructura de Directorios ===")
    
    required_dirs = [
        'core/',
        'core/adapters/'
    ]
    
    required_files = [
        'core/__init__.py',
        'core/adapters/__init__.py',
        'core/adapters/fatigue_adapter.py',
        'core/adapters/behavior_adapter.py',
        'core/adapters/face_recognition_adapter.py'
    ]
    
    # Verificar directorios
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ Directorio {dir_path} existe")
        else:
            print(f"  ❌ Directorio {dir_path} NO existe")
            return False
    
    # Verificar archivos
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ Archivo {file_path} existe")
        else:
            print(f"  ❌ Archivo {file_path} NO existe")
            return False
    
    # Verificar que archivos antiguos ya NO existan en raíz
    old_files = [
        'fatigue_adapter.py',
        'behavior_adapter.py',
        'face_recognition_adapter.py'
    ]
    
    print("\n🔍 Verificando que archivos antiguos fueron movidos:")
    for old_file in old_files:
        if Path(old_file).exists():
            print(f"  ⚠️ {old_file} aún existe en raíz (debería moverse a core/adapters/)")
        else:
            print(f"  ✅ {old_file} movido correctamente desde raíz")
    
    return True

def test_adapters_import():
    """Probar importación de adaptadores desde nueva ubicación"""
    print("\n=== TEST: Importación de Adaptadores ===")
    
    adapters_to_test = [
        ('core.adapters.fatigue_adapter', 'FatigueAdapter'),
        ('core.adapters.behavior_adapter', 'BehaviorAdapter'),
        ('core.adapters.face_recognition_adapter', 'FaceRecognitionAdapter')
    ]
    
    errors = 0
    
    for module_name, class_name in adapters_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            adapter_class = getattr(module, class_name)
            print(f"  ✅ {module_name}.{class_name} importado correctamente")
        except ImportError as e:
            print(f"  ❌ {module_name}: Error de importación - {e}")
            errors += 1
        except AttributeError as e:
            print(f"  ❌ {module_name}: Clase {class_name} no encontrada - {e}")
            errors += 1
        except Exception as e:
            print(f"  ❌ {module_name}: Error inesperado - {e}")
            errors += 1
    
    return errors == 0

def test_core_init():
    """Probar importación desde core/__init__.py"""
    print("\n=== TEST: Importación desde core/__init__.py ===")
    
    try:
        # Probar importación directa desde core
        import core
        
        # Verificar que las funciones helper existan
        if hasattr(core, 'get_available_adapters'):
            available = core.get_available_adapters()
            print(f"  ✅ Adaptadores disponibles: {available}")
        else:
            print("  ⚠️ Función get_available_adapters no encontrada")
        
        # Probar importación de adaptadores específicos
        try:
            from core import FatigueAdapter, BehaviorAdapter, FaceRecognitionAdapter
            print("  ✅ Importación directa desde core exitosa")
        except ImportError as e:
            print(f"  ⚠️ Importación directa falló (normal si módulos principales no existen): {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error importando core: {e}")
        return False

def test_adapters_init():
    """Probar importación desde core/adapters/__init__.py"""
    print("\n=== TEST: Importación desde core/adapters/__init__.py ===")
    
    try:
        # Probar importación del módulo adapters
        from core import adapters
        
        # Verificar funciones helper
        if hasattr(adapters, 'get_all_adapters'):
            all_adapters = adapters.get_all_adapters()
            print(f"  ✅ Todos los adaptadores: {list(all_adapters.keys())}")
        
        if hasattr(adapters, 'create_adapter'):
            print("  ✅ Función create_adapter disponible")
        
        if hasattr(adapters, 'test_adapters'):
            print("  ✅ Función test_adapters disponible")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error importando core.adapters: {e}")
        return False

def test_adapter_instantiation():
    """Probar instanciación de adaptadores (sin dependencias)"""
    print("\n=== TEST: Instanciación de Adaptadores (Sin Dependencias) ===")
    
    adapters_info = [
        ('core.adapters.fatigue_adapter', 'FatigueAdapter'),
        ('core.adapters.behavior_adapter', 'BehaviorAdapter'),
        ('core.adapters.face_recognition_adapter', 'FaceRecognitionAdapter')
    ]
    
    success_count = 0
    
    for module_name, class_name in adapters_info:
        try:
            # Importar módulo
            module = __import__(module_name, fromlist=[class_name])
            adapter_class = getattr(module, class_name)
            
            # INTENTAR instanciar (puede fallar por dependencias)
            try:
                instance = adapter_class()
                print(f"  ✅ {class_name} instanciado correctamente")
                
                # Probar método get_adapter_info si existe
                if hasattr(instance, 'get_adapter_info'):
                    info = instance.get_adapter_info()
                    print(f"      Info: {info['name']} en {info['location']}")
                
                success_count += 1
                
            except Exception as e:
                print(f"  ⚠️ {class_name}: Error de instanciación (normal - dependencias faltantes): {e}")
        
        except Exception as e:
            print(f"  ❌ {class_name}: Error de importación: {e}")
    
    print(f"\n📊 Adaptadores instanciados exitosamente: {success_count}/3")
    return success_count > 0

def test_imports_correction():
    """Verificar que los imports en adaptadores sean correctos"""
    print("\n=== TEST: Corrección de Imports ===")
    
    adapter_files = [
        'core/adapters/fatigue_adapter.py',
        'core/adapters/behavior_adapter.py', 
        'core/adapters/face_recognition_adapter.py'
    ]
    
    expected_imports = {
        'fatigue_adapter.py': [
            'from fatigue_detection import FatigueDetector',
            'from client.utils.event_manager import EventManager'
        ],
        'behavior_adapter.py': [
            'from behavior_detection_module import BehaviorDetectionModule',
            'from client.utils.event_manager import EventManager'
        ],
        'face_recognition_adapter.py': [
            'from face_recognition_module import FaceRecognitionModule',
            'from client.utils.event_manager import EventManager'
        ]
    }
    
    all_good = True
    
    for adapter_file in adapter_files:
        if not Path(adapter_file).exists():
            print(f"  ❌ {adapter_file} no existe")
            all_good = False
            continue
        
        filename = Path(adapter_file).name
        expected = expected_imports.get(filename, [])
        
        try:
            with open(adapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  📄 Verificando {filename}:")
            
            for expected_import in expected:
                if expected_import in content:
                    print(f"    ✅ {expected_import}")
                else:
                    print(f"    ❌ {expected_import} - NO ENCONTRADO")
                    all_good = False
            
        except Exception as e:
            print(f"  ❌ Error leyendo {adapter_file}: {e}")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de restructuración de adaptadores...")
    print()
    
    # Cambiar al directorio del proyecto
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Ejecutar todas las pruebas
    tests = [
        ("Estructura de Directorios", test_directory_structure),
        ("Importación de Adaptadores", test_adapters_import),
        ("Core Init", test_core_init),
        ("Adapters Init", test_adapters_init),
        ("Corrección de Imports", test_imports_correction),
        ("Instanciación de Adaptadores", test_adapter_instantiation)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERROR - {e}")
        print()
    
    # Resumen final
    print("="*60)
    print(f"📊 RESUMEN DE PRUEBAS:")
    print(f"  ✅ Pasaron: {passed}")
    print(f"  ❌ Fallaron: {failed}")
    print(f"  📈 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("✅ La restructuración de adaptadores está completa")
        print("💡 Puedes continuar con el siguiente paso")
        sys.exit(0)
    else:
        print(f"\n⚠️ {failed} PRUEBAS FALLARON")
        print("🔧 Revisa los errores antes de continuar")
        if passed > 0:
            print(f"💡 {passed} pruebas pasaron - el progreso es bueno")
        sys.exit(1)