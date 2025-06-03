<?php
// api/v1/devices/heartbeat.php

// Permitir solicitudes desde cualquier origen (CORS)
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// Incluir archivos necesarios
include_once '../../../config/database.php';
include_once '../../utils/JwtHandler.php';
include_once '../../utils/Response.php';
include_once '../../models/Device.php';

// Solo permitir método POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo Response::error('Método no permitido', 405);
    exit();
}

// Verificar token JWT
$headers = apache_request_headers();
$authHeader = isset($headers['Authorization']) ? $headers['Authorization'] : '';

if (empty($authHeader)) {
    echo Response::error('Token no proporcionado', 401);
    exit();
}

// Extraer token del header
$token = '';
if (preg_match('/Bearer\s(\S+)/', $authHeader, $matches)) {
    $token = $matches[1];
}

// Verificar token
$jwt = new JwtHandler();
$decoded = $jwt->verifyToken($token);

if (!$decoded) {
    echo Response::error('Token inválido o expirado', 401);
    exit();
}

// Obtener datos enviados
$data = json_decode(file_get_contents("php://input"));

// Obtener IP del cliente
$client_ip = $_SERVER['REMOTE_ADDR'];
if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $client_ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
}

// Actualizar estado del dispositivo
$result = db_query(
    "UPDATE devices 
     SET last_access = NOW(), 
         status = ?, 
         ip_address = ?
     WHERE device_id = ?",
    [
        $data->status ?? 'online',
        $client_ip,
        $decoded->device_id
    ]
);

if ($result) {
    // Registrar heartbeat en los logs
    db_insert('system_logs', [
        'log_type' => 'info',
        'machine_id' => $decoded->machine_id,
        'message' => "Heartbeat recibido del dispositivo {$decoded->device_id}",
        'details' => json_encode([
            'ip' => $client_ip,
            'status' => $data->status ?? 'online',
            'additional_info' => $data->info ?? null
        ]),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    
    echo Response::success([
        'device_id' => $decoded->device_id,
        'timestamp' => date('Y-m-d H:i:s'),
        'status' => 'acknowledged'
    ], 'Heartbeat recibido');
} else {
    echo Response::error('Error al actualizar estado del dispositivo', 500);
}
?>