<?php
// pages/devices/edit.php

// Primero iniciar sesión si no está iniciada
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Cargar configuración
require_once '../../config/config.php';
require_once '../../config/database.php';
require_once '../../includes/auth.php';

// Verificar si el usuario está autenticado
if (!isset($_SESSION['user_id'])) {
    header("Location: " . BASE_URL . "/login.php");
    exit();
}

// Definir el título de la página
$pageTitle = "Editar Dispositivo";

// Incluir header y sidebar
require_once '../../includes/header.php';
require_once '../../includes/sidebar.php';

// Obtener ID del dispositivo
$device_id = $_GET['id'] ?? null;

if (!$device_id) {
    header("Location: index.php?error=ID de dispositivo no especificado");
    exit();
}

// Obtener información del dispositivo
$device = db_fetch_one("SELECT * FROM devices WHERE id = ?", [$device_id]);

if (!$device) {
    header("Location: index.php?error=Dispositivo no encontrado");
    exit();
}

// Obtener lista de máquinas para el select
$machines = db_fetch_all("SELECT id, name FROM machines WHERE status = 'active' ORDER BY name");

// Procesar formulario si se envió
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'] ?? '';
    $device_type = $_POST['device_type'] ?? '';
    $machine_id = $_POST['machine_id'] ?? null;
    $location = $_POST['location'] ?? '';
    $status = $_POST['status'] ?? 'offline';
    $reset_api_key = isset($_POST['reset_api_key']);
    
    // Validar datos requeridos
    if (empty($device_type)) {
        $error = "El tipo de dispositivo es requerido";
    } else {
        // Preparar datos para actualizar
        $updateData = [
            'name' => $name,
            'device_type' => $device_type,
            'machine_id' => $machine_id,
            'location' => $location,
            'status' => $status
        ];
        
        // Si se solicita resetear la API key
        if ($reset_api_key) {
            $new_api_key = bin2hex(random_bytes(32));
            $updateData['api_key'] = password_hash($new_api_key, PASSWORD_DEFAULT);
        }
        
        // Actualizar dispositivo
        $result = db_update('devices', $updateData, 'id = ?', [$device_id]);
        
        if ($result !== false) {
            if ($reset_api_key) {
                // Guardar la nueva API key para mostrarla
                $_SESSION['new_device_api_key'] = $new_api_key;
                $_SESSION['new_device_id'] = $device['device_id'];
                header("Location: view.php?id=$device_id&new=1");
            } else {
                header("Location: index.php?msg=Dispositivo actualizado exitosamente");
            }
            exit();
        } else {
            $error = "Error al actualizar el dispositivo";
        }
    }
}
?>

<!-- Content Wrapper -->
<div class="content-wrapper">
    <!-- Content Header -->
    <section class="content-header">
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-sm-6">
                    <h1>Editar Dispositivo</h1>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-right">
                        <li class="breadcrumb-item"><a href="<?php echo BASE_URL; ?>/index.php">Inicio</a></li>
                        <li class="breadcrumb-item"><a href="index.php">Dispositivos</a></li>
                        <li class="breadcrumb-item active">Editar</li>
                    </ol>
                </div>
            </div>
        </div>
    </section>

    <!-- Main content -->
    <section class="content">
        <div class="container-fluid">
            <?php if (isset($error)): ?>
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <?php echo htmlspecialchars($error); ?>
                    <button type="button" class="close" data-dismiss="alert">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            <?php endif; ?>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Información del Dispositivo</h3>
                </div>
                
                <form method="POST" action="">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>ID del Dispositivo</label>
                                    <input type="text" class="form-control" readonly 
                                           value="<?php echo htmlspecialchars($device['device_id']); ?>">
                                    <small class="form-text text-muted">El ID no puede ser modificado</small>
                                </div>
                            </div>
                            
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="name">Nombre del Dispositivo</label>
                                    <input type="text" class="form-control" id="name" name="name" 
                                           placeholder="Ej: Raspberry Pi Zona Norte"
                                           value="<?php echo htmlspecialchars($_POST['name'] ?? $device['name'] ?? ''); ?>">
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="device_type">Tipo de Dispositivo *</label>
                                    <select class="form-control" id="device_type" name="device_type" required>
                                        <option value="">Seleccione un tipo</option>
                                        <option value="Raspberry Pi" <?php echo ($device['device_type'] === 'Raspberry Pi') ? 'selected' : ''; ?>>
                                            Raspberry Pi
                                        </option>
                                        <option value="Edge Computer" <?php echo ($device['device_type'] === 'Edge Computer') ? 'selected' : ''; ?>>
                                            Edge Computer
                                        </option>
                                        <option value="Industrial PC" <?php echo ($device['device_type'] === 'Industrial PC') ? 'selected' : ''; ?>>
                                            Industrial PC
                                        </option>
                                        <option value="Other" <?php echo ($device['device_type'] === 'Other') ? 'selected' : ''; ?>>
                                            Otro
                                        </option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="machine_id">Máquina Asignada</label>
                                    <select class="form-control" id="machine_id" name="machine_id">
                                        <option value="">Sin asignar</option>
                                        <?php foreach ($machines as $machine): ?>
                                            <option value="<?php echo $machine['id']; ?>" 
                                                    <?php echo ($device['machine_id'] === $machine['id']) ? 'selected' : ''; ?>>
                                                <?php echo htmlspecialchars($machine['name']); ?>
                                            </option>
                                        <?php endforeach; ?>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="location">Ubicación</label>
                                    <input type="text" class="form-control" id="location" name="location" 
                                           placeholder="Ej: Zona Norte, Área de Excavación"
                                           value="<?php echo htmlspecialchars($_POST['location'] ?? $device['location'] ?? ''); ?>">
                                </div>
                            </div>
                            
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="status">Estado</label>
                                    <select class="form-control" id="status" name="status">
                                        <option value="online" <?php echo ($device['status'] === 'online') ? 'selected' : ''; ?>>
                                            En línea
                                        </option>
                                        <option value="offline" <?php echo ($device['status'] === 'offline') ? 'selected' : ''; ?>>
                                            Fuera de línea
                                        </option>
                                        <option value="syncing" <?php echo ($device['status'] === 'syncing') ? 'selected' : ''; ?>>
                                            Sincronizando
                                        </option>
                                        <option value="error" <?php echo ($device['status'] === 'error') ? 'selected' : ''; ?>>
                                            Error
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-12">
                                <div class="form-group">
                                    <div class="custom-control custom-checkbox">
                                        <input type="checkbox" class="custom-control-input" id="reset_api_key" name="reset_api_key">
                                        <label class="custom-control-label" for="reset_api_key">
                                            Generar nueva API Key (esto invalidará la clave actual)
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Información de conexión:
                            <ul class="mb-0">
                                <li>Último acceso: <?php echo $device['last_access'] ? date('d/m/Y H:i:s', strtotime($device['last_access'])) : 'Nunca'; ?></li>
                                <li>Última sincronización: <?php echo $device['last_sync'] ? date('d/m/Y H:i:s', strtotime($device['last_sync'])) : 'Nunca'; ?></li>
                                <li>IP: <?php echo htmlspecialchars($device['ip_address'] ?? 'No disponible'); ?></li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="card-footer">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Guardar Cambios
                        </button>
                        <a href="index.php" class="btn btn-secondary">
                            <i class="fas fa-times"></i> Cancelar
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </section>
</div>

<?php include '../../includes/footer.php'; ?>

<script>
$(document).ready(function() {
    // Confirmación para reset de API key
    $('#reset_api_key').change(function() {
        if ($(this).is(':checked')) {
            if (!confirm('¿Está seguro de generar una nueva API Key? Esto invalidará la clave actual y el dispositivo deberá ser reconfigurado.')) {
                $(this).prop('checked', false);
            }
        }
    });
    
    // Validación del formulario
    $('form').submit(function(e) {
        const deviceType = $('#device_type').val();
        
        if (!deviceType) {
            e.preventDefault();
            alert('Por favor seleccione el tipo de dispositivo');
            return false;
        }
    });
});
</script>