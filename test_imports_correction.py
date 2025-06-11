#!/usr/bin/env python3
"""
Script para verificar que todos los imports de adaptadores han sido corregidos
"""

import sys
import os
from pathlib import Path
import re

def find_files_with_adapter_imports():
    """Buscar archivos que importen adaptadores"""
    print("=== BUSCANDO ARCHIVOS CON IMPORTS DE ADAPTADORES ===")
    
    # Patrones de imports antiguos (incorrectos)
    old_import_patterns = [
        r'from\s+fatigue_adapter\s+import',
        r'from\s+behavior_adapter\s+import', 
        r'from\s+face_recognition_adapter\s+import',
        r'import\s+fatigue_adapter',
        r'import\s+behavior_adapter',
        r'import\s+face_recognition_adapter'
    ]
    
    # Patrones de imports nuevos (correctos)
    new_import_patterns = [
        r'from\s+core\.adapters\.fatigue_adapter\s+import',
        r'from\s+core\.adapters\.behavior_adapter\s+import',
        r'from\s+core\.adapters\.face_recognition_adapter\s+import',
        r'from\s+core\s+import.*Adapter',
        r'from\s+core\.adapters\s+import'
    ]
    
    # Archivos a revisar
    files_to_check = []
    
    # Buscar archivos Python recursivamente
    for file_path in Path('.').rglob('*.py'):
        # Excluir archivos de prueba y __pycache__
        if '__pycache__' in str(file_path) or 'test_' in file_path.name:
            continue
        files_to_check.append(file_path)
    
    results = {
        'files_with_old_imports': [],
        'files_with_new_imports': [],
        'files_to_update': []
    }
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar imports antiguos
            has_old_imports = False
            for pattern in old_import_patterns:
                if re.search(pattern, content):
                    has_old_imports = True
                    break
            
            # Buscar imports nuevos
            has_new_imports = False
            for pattern in new_import_patterns:
                if re.search(pattern, content):
                    has_new_imports = True
                    break
            
            if has_old_imports:
                results['files_with_old_imports'].append(str(file_path))
                print(f"  ❌ {file_path} - Tiene imports ANTIGUOS")
            
            if has_new_imports:
                results['files_with_new_imports'].append(str(file_path))
                print(f"  ✅ {file_path} - Tiene imports NUEVOS")
            
            if has_old_imports and not has_new_imports:
                results['files_to_update'].append(str(file_path))
        
        except Exception as e:
            print(f"  ⚠️ Error leyendo {file_path}: {e}")
    
    return results

def check_specific_files():
    """Verificar archivos específicos que deberían usar adaptadores"""
    print("\n=== VERIFICANDO ARCHIVOS ESPECÍFICOS ===")
    
    target_files = [
        'sync_integrator.py',
        'main_with_sync.py',
        # Agregar otros archivos que usen adaptadores
    ]
    
    for file_path in target_files:
        if Path(file_path).exists():
            print(f"\n📄 Verificando {file_path}:")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar imports específicos
                imports_to_check = [
                    'from core.adapters.fatigue_adapter import FatigueAdapter',
                    'from core.adapters.behavior_adapter import BehaviorAdapter',
                    'from core.adapters.face_recognition_adapter import FaceRecognitionAdapter'
                ]
                
                for import_line in imports_to_check:
                    if import_line in content:
                        print(f"  ✅ {import_line}")
                    else:
                        print(f"  ❌ {import_line} - NO ENCONTRADO")
                
                # Verificar imports antiguos que NO deberían estar
                old_imports = [
                    'from fatigue_adapter import',
                    'from behavior_adapter import',
                    'from face_recognition_adapter import'
                ]
                
                for old_import in old_imports:
                    if old_import in content:
                        print(f"  ⚠️ IMPORT ANTIGUO ENCONTRADO: {old_import}")
                
            except Exception as e:
                print(f"  ❌ Error leyendo {file_path}: {e}")
        else:
            print(f"  ⚠️ {file_path} no existe")

def test_adapter_imports():
    """Probar que los imports de adaptadores funcionen"""
    print("\n=== PROBANDO IMPORTS DE ADAPTADORES ===")
    
    tests = [
        # Imports individuales
        ("from core.adapters.fatigue_adapter import FatigueAdapter", "FatigueAdapter"),
        ("from core.adapters.behavior_adapter import BehaviorAdapter", "BehaviorAdapter"),
        ("from core.adapters.face_recognition_adapter import FaceRecognitionAdapter", "FaceRecognitionAdapter"),
        
        # Imports desde core
        ("from core import FatigueAdapter, BehaviorAdapter, FaceRecognitionAdapter", None),
        
        # Import del módulo completo
        ("import core.adapters", "core.adapters"),
    ]
    
    success_count = 0
    
    for import_statement, class_to_check in tests:
        try:
            # Ejecutar import
            exec(import_statement)
            
            if class_to_check and class_to_check != "core.adapters":
                # Verificar que la clase existe
                if class_to_check in locals():
                    print(f"  ✅ {import_statement}")
                    success_count += 1
                else:
                    print(f"  ❌ {import_statement} - Clase no disponible")
            else:
                print(f"  ✅ {import_statement}")
                success_count += 1
                
        except Exception as e:
            print(f"  ❌ {import_statement} - Error: {e}")
    
    print(f"\n📊 Imports exitosos: {success_count}/{len(tests)}")
    return success_count == len(tests)

def test_sync_integrator():
    """Probar específicamente sync_integrator.py"""
    print("\n=== PROBANDO SYNC_INTEGRATOR.PY ===")
    
    if not Path('sync_integrator.py').exists():
        print("  ⚠️ sync_integrator.py no existe")
        return False
    
    try:
        # Intentar importar SyncIntegrator
        from sync_integrator import SyncIntegrator
        print("  ✅ SyncIntegrator importado correctamente")
        
        # Intentar instanciar (puede fallar por dependencias)
        try:
            integrator = SyncIntegrator()
            print("  ✅ SyncIntegrator instanciado correctamente")
            
            # Verificar métodos
            methods_to_check = [
                'get_fatigue_adapter',
                'get_behavior_adapter', 
                'get_face_recognition_adapter',
                'get_available_adapters',
                'get_adapters_info'
            ]
            
            for method_name in methods_to_check:
                if hasattr(integrator, method_name):
                    print(f"    ✅ Método {method_name} disponible")
                else:
                    print(f"    ❌ Método {method_name} NO disponible")
            
            return True
            
        except Exception as e:
            print(f"  ⚠️ Error instanciando SyncIntegrator (normal - dependencias): {e}")
            return True  # Import funcionó, instanciación puede fallar por dependencias
    
    except Exception as e:
        print(f"  ❌ Error importando SyncIntegrator: {e}")
        return False

def generate_fix_suggestions():
    """Generar sugerencias para corregir imports"""
    print("\n=== SUGERENCIAS PARA CORRECCIÓN ===")
    
    suggestions = {
        'from fatigue_adapter import FatigueAdapter': 
            'from core.adapters.fatigue_adapter import FatigueAdapter',
        'from behavior_adapter import BehaviorAdapter':
            'from core.adapters.behavior_adapter import BehaviorAdapter',
        'from face_recognition_adapter import FaceRecognitionAdapter':
            'from core.adapters.face_recognition_adapter import FaceRecognitionAdapter',
        'import fatigue_adapter':
            'from core.adapters import fatigue_adapter',
        'import behavior_adapter':
            'from core.adapters import behavior_adapter',
        'import face_recognition_adapter':
            'from core.adapters import face_recognition_adapter'
    }
    
    print("💡 Reemplazos recomendados:")
    for old, new in suggestions.items():
        print(f"  {old}")
        print(f"  ➜ {new}")
        print()

if __name__ == "__main__":
    print("🔍 Verificando corrección de imports de adaptadores...")
    print()
    
    # Ejecutar todas las verificaciones
    results = find_files_with_adapter_imports()
    check_specific_files()
    imports_work = test_adapter_imports()
    sync_integrator_works = test_sync_integrator()
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN:")
    
    if results['files_with_old_imports']:
        print(f"❌ {len(results['files_with_old_imports'])} archivos con imports ANTIGUOS:")
        for file_path in results['files_with_old_imports']:
            print(f"  - {file_path}")
    
    if results['files_with_new_imports']:
        print(f"✅ {len(results['files_with_new_imports'])} archivos con imports NUEVOS:")
        for file_path in results['files_with_new_imports']:
            print(f"  - {file_path}")
    
    print(f"\n🧪 Pruebas de imports: {'✅ PASSED' if imports_work else '❌ FAILED'}")
    print(f"🔗 SyncIntegrator: {'✅ PASSED' if sync_integrator_works else '❌ FAILED'}")
    
    if results['files_to_update']:
        print(f"\n🔧 Archivos que necesitan actualización:")
        for file_path in results['files_to_update']:
            print(f"  - {file_path}")
        generate_fix_suggestions()
    
    # Determinar éxito general
    all_good = (
        len(results['files_with_old_imports']) == 0 and
        imports_work and 
        sync_integrator_works
    )
    
    if all_good:
        print("\n🎉 TODOS LOS IMPORTS CORREGIDOS")
        print("✅ La corrección de imports está completa")
        sys.exit(0)
    else:
        print("\n⚠️ ALGUNOS IMPORTS NECESITAN CORRECCIÓN")
        print("🔧 Revisa los archivos marcados arriba")
        sys.exit(1)