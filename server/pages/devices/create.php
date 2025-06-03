<?php
// pages/devices/create.php

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
$pageTitle = "Registrar Dispositivo";

// Incluir header y sidebar
require_once '../../includes/header.php';
require_once '../../includes/sidebar.php';

// Obtener lista de máquinas para el select
$machines = db_fetch_all("SELECT id, name FROM machines WHERE status = 'active' ORDER BY name");

// Procesar formulario si se envió
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $device_id = $_POST['device_id'] ?? '';
    $name = $_POST['name'] ?? '';
    $device_type = $_POST['device_type'] ?? '';
    $machine_id = $_POST['machine_id'] ?? null;
    $location = $_POST['location'] ?? '';
    
    // Validar datos requeridos
    if (empty($device_id) || empty($device_type)) {
        $error = "El ID del dispositivo y el tipo son requeridos";
    } else {
        // Verificar si el device_id ya existe
        $existing = db_fetch_one(
            "SELECT id FROM devices WHERE device_id = ?", 
            [$device_id]
        );
        
        if ($existing) {
            $error = "Ya existe un dispositivo con ese ID";
        } else {
            // Generar API key
            $api_key = bin2hex(random_bytes(32));
            $api_key_hash = password_hash($api_key, PASSWORD_DEFAULT);
            
            // Insertar dispositivo
            $data = [
                'device_id' => $device_id,
                'api_key' => $api_key_hash,
                'name' => $name,
                'device_type' => $device_type,
                'machine_id' => $machine_id,
                'location' => $location,
                'status' => 'offline',
                'created_at' => date('Y-m-d H:i:s')
            ];
            
            $id = db_insert('devices', $data);
            
            if ($id) {
                // Guardar la API key sin hash para mostrarla al usuario
                $_SESSION['new_device_api_key'] = $api_key;
                $_SESSION['new_device_id'] = $device_id;
                header("Location: view.php?id=$id&new=1");
                exit();
            } else {
                $error = "Error al registrar el dispositivo";
            }
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
                    <h1>Registrar Dispositivo</h1>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-right">
                        <li class="breadcrumb-item"><a href="<?php echo BASE_URL; ?>/index.php">Inicio</a></li>
                        <li class="breadcrumb-item"><a href="index.php">Dispositivos</a></li>
                        <li class="breadcrumb-item active">Registrar</li>
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
                                    <label for="device_id">ID del Dispositivo *</label>
                                    <input type="text" class="form-control" id="device_id" name="device_id" 
                                           required placeholder="Ej: RPI001"
                                           value="<?php echo htmlspecialchars($_POST['device_id'] ?? ''); ?>">
                                    <small class="form-text text-muted">Identificador único del dispositivo</small>
                                </div>
                            </div>
                            
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="name">Nombre del Dispositivo</label>
                                    <input type="text" class="form-control" id="name" name="name" 
                                           placeholder="Ej: Raspberry Pi Zona Norte"
                                           value="<?php echo htmlspecialchars($_POST['name'] ?? ''); ?>">
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label for="device_type">Tipo de Dispositivo *</label>
                                    <select class="form-control" id="device_type" name="device_type" required>
                                        <option value="">Seleccione un tipo</option>
                                        <option value="Raspberry Pi" <?php echo ($_POST['device_type'] ?? '') === 'Raspberry Pi' ? 'selected' : ''; ?>>
                                            Raspberry Pi
                                        </option>
                                        <option value="Edge Computer" <?php echo ($_POST['device_type'] ?? '') === 'Edge Computer' ? 'selected' : ''; ?>>
                                            Edge Computer
                                        </option>
                                        <option value="Industrial PC" <?php echo ($_POST['device_type'] ?? '') === 'Industrial PC' ? 'selected' : ''; ?>>
                                            Industrial PC
                                        </option>
                                        <option value="Other" <?php echo ($_POST['device_type'] ?? '') === 'Other' ? 'selected' : ''; ?>>
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
                                                    <?php echo ($_POST['machine_id'] ?? '') === $machine['id'] ? 'selected' : ''; ?>>
                                                <?php echo htmlspecialchars($machine['name']); ?>
                                            </option>
                                        <?php endforeach; ?>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label for="location">Ubicación</label>
                                    <input type="text" class="form-control" id="location" name="location" 
                                           placeholder="Ej: Zona Norte, Área de Excavación"
                                           value="<?php echo htmlspecialchars($_POST['location'] ?? ''); ?>">
                                </div>
                            </div>
                        </div>
                        
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Al registrar el dispositivo se generará automáticamente una API Key que deberá 
                            configurar en el dispositivo cliente.
                        </div>
                    </div>
                    
                    <div class="card-footer">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Registrar Dispositivo
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
    // Validación del formulario
    $('form').submit(function(e) {
        const deviceId = $('#device_id').val().trim();
        const deviceType = $('#device_type').val();
        
        if (!deviceId || !deviceType) {
            e.preventDefault();
            alert('Por favor complete todos los campos requeridos');
            return false;
        }
        
        // Validar formato del device_id (solo letras, números y guiones)
        const deviceIdPattern = /^[a-zA-Z0-9-_]+$/;
        if (!deviceIdPattern.test(deviceId)) {
            e.preventDefault();
            alert('El ID del dispositivo solo puede contener letras, números, guiones y guiones bajos');
            return false;
        }
    });
});
</script>