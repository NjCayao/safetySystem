#!/usr/bin/env python3
"""
Script de prueba para verificar que la configuración YAML funciona correctamente
después de eliminar config.ini
"""

import sys
import os
from pathlib import Path

def test_yaml_config():
    """Probar que la configuración YAML se carga correctamente"""
    
    print("=== TEST: Configuración YAML Unificada ===")
    print()
    
    # Verificar que el archivo YAML existe
    yaml_path = Path('config/production.yaml')
    if not yaml_path.exists():
        print("❌ ERROR: config/production.yaml no existe")
        return False
    
    print("✅ config/production.yaml encontrado")
    
    # Verificar que config.ini NO existe (debe estar eliminado)
    ini_path = Path('client/config/config.ini')
    if ini_path.exists():
        print("⚠️ ADVERTENCIA: client/config/config.ini aún existe (debería eliminarse)")
    else:
        print("✅ client/config/config.ini eliminado correctamente")
    
    # Probar el adaptador YAML
    try:
        from client.config.yaml_config_adapter import get_yaml_config
        config = get_yaml_config()
        print("✅ Adaptador YAML importado correctamente")
    except ImportError as e:
        print(f"❌ ERROR: No se pudo importar adaptador YAML: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Error inicializando adaptador YAML: {e}")
        return False
    
    # Probar lectura de configuraciones específicas
    test_configs = [
        ('SERVER', 'api_url', 'URL del servidor'),
        ('DEVICE', 'device_id', 'ID del dispositivo'),
        ('DEVICE', 'api_key', 'API Key'),
        ('DEVICE', 'device_type', 'Tipo de dispositivo'),
        ('CONNECTION', 'check_interval', 'Intervalo de verificación'),
        ('CONNECTION', 'retry_attempts', 'Intentos de reintento'),
        ('STORAGE', 'db_path', 'Ruta de base de datos'),
        ('STORAGE', 'max_stored_events', 'Máximo eventos almacenados'),
        ('SYNC', 'batch_size', 'Tamaño de lote'),
        ('SYNC', 'sync_interval', 'Intervalo de sincronización'),
        ('SYNC', 'priority_types', 'Tipos de prioridad')
    ]
    
    print("\n📋 Probando configuraciones específicas:")
    errors = 0
    
    for section, key, description in test_configs:
        try:
            value = config.get(section, key)
            if value is not None:
                # Mostrar solo primeros caracteres para keys sensibles
                if 'key' in key.lower() and len(str(value)) > 10:
                    display_value = str(value)[:10] + "..."
                else:
                    display_value = value
                print(f"  ✅ {section}.{key}: {display_value}")
            else:
                print(f"  ❌ {section}.{key}: No encontrado")
                errors += 1
        except Exception as e:
            print(f"  ❌ {section}.{key}: Error - {e}")
            errors += 1
    
    # Probar métodos específicos del adaptador
    print("\n🔧 Probando métodos del adaptador:")
    
    try:
        # Probar getint
        check_interval = config.getint('CONNECTION', 'check_interval')
        print(f"  ✅ getint() - check_interval: {check_interval}")
        
        # Probar getboolean
        sync_enabled = config.getboolean('SYNC', 'enabled', fallback=True)
        print(f"  ✅ getboolean() - sync enabled: {sync_enabled}")
        
        # Probar con fallback
        nonexistent = config.get('NONEXISTENT', 'key', 'fallback_value')
        print(f"  ✅ fallback - valor no existente: {nonexistent}")
        
    except Exception as e:
        print(f"  ❌ Error probando métodos: {e}")
        errors += 1
    
    # Probar importación de módulos del cliente
    print("\n📦 Probando importación de módulos del cliente:")
    
    modules_to_test = [
        ('client.api.api_client', 'ApiClient'),
        ('client.api.sync', 'SyncManager'),
        ('client.db.local_storage', 'LocalStorage'),
        ('client.utils.connection', 'ConnectionManager'),
        ('client.utils.file_manager', 'FileManager'),
        ('client.utils.event_manager', 'EventManager')
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"  ❌ {module_name}: Error de importación - {e}")
            errors += 1
        except Exception as e:
            print(f"  ❌ {module_name}: Error - {e}")
            errors += 1
    
    # Resumen final
    print(f"\n📊 RESUMEN:")
    if errors == 0:
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("🎉 La configuración YAML está funcionando correctamente")
        print("💡 Puedes proceder con el siguiente paso")
        return True
    else:
        print(f"❌ {errors} ERRORES ENCONTRADOS")
        print("🔧 Revisa los errores antes de continuar")
        return False

def test_production_yaml_structure():
    """Verificar estructura específica del production.yaml"""
    print("\n=== TEST: Estructura de production.yaml ===")
    
    try:
        import yaml
        with open('config/production.yaml', 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        
        # Verificar secciones principales
        required_sections = ['system', 'camera', 'fatigue', 'sync', 'connection', 'storage']
        
        for section in required_sections:
            if section in yaml_data:
                print(f"  ✅ Sección '{section}' encontrada")
            else:
                print(f"  ❌ Sección '{section}' faltante")
        
        # Verificar que sync tiene la configuración unificada
        sync_section = yaml_data.get('sync', {})
        sync_required = ['server_url', 'device_id', 'api_key', 'batch_size']
        
        print("\n🔄 Verificando sección 'sync' unificada:")
        for key in sync_required:
            if key in sync_section:
                print(f"  ✅ sync.{key}")
            else:
                print(f"  ❌ sync.{key} faltante")
        
        # Verificar que NO hay sección device duplicada
        if 'device' in yaml_data:
            print("  ⚠️ ADVERTENCIA: Sección 'device' duplicada encontrada (debería estar solo en 'sync')")
        else:
            print("  ✅ No hay duplicación de sección 'device'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura YAML: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de configuración YAML...")
    print()
    
    # Cambiar al directorio del proyecto
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success1 = test_production_yaml_structure()
    success2 = test_yaml_config()
    
    print("\n" + "="*60)
    if success1 and success2:
        print("🎉 TODAS LAS PRUEBAS EXITOSAS")
        print("✅ La unificación de configuración está completa")
        print("💡 Puedes continuar con el siguiente paso")
        sys.exit(0)
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("🔧 Revisa los errores antes de continuar")
        sys.exit(1)