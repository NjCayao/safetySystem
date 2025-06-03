<?php
// Mostrar todos los errores para depuración
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Incluir necesarios
require_once '../../config/config.php';
require_once '../../config/database.php'; // Añadido para acceso a la base de datos
require_once '../../models/Alert.php';
require_once '../../models/Operator.php';
require_once '../../models/Machine.php';

// Verificar si el usuario está autenticado
session_start();
$isLoggedIn = isset($_SESSION['user_id']);

// Si no está autenticado, redirigir al login
if (!$isLoggedIn) {
    header('Location: ../../login.php');
    exit;
}

// Inicializar modelos
$alertModel = new Alert();
$operatorModel = new Operator();
$machineModel = new Machine();

// Obtener estadísticas generales
$today = date('Y-m-d');
$weekStart = date('Y-m-d', strtotime('monday this week'));
$monthStart = date('Y-m-01');
$alertsToday = $alertModel->countAlerts(['date_from' => $today]);
$alertsThisWeek = $alertModel->countAlerts(['date_from' => $weekStart]);
$alertsThisMonth = $alertModel->countAlerts(['date_from' => $monthStart]);
$alertsPending = $alertModel->countAlerts(['acknowledged' => 0]);

// Obtener últimas alertas
$recentAlerts = $alertModel->getAlerts([], 10, 0);

// Definir tipos de alerta para mostrar nombre legible
$alertTypes = [
    'fatigue' => 'Fatiga',
    'phone' => 'Uso de celular',
    'smoking' => 'Fumando',
    'unauthorized' => 'No autorizado',
    'yawn' => 'Bostezo',
    'distraction' => 'Distracción',
    'behavior' => 'Comportamiento anómalo',
    'other' => 'Otro'
];

// Obtener total de operadores y máquinas
$totalOperators = $operatorModel->countOperators();
$totalMachines = $machineModel->countMachines();

// Definir título de la página
$pageTitle = 'Estadísticas del Sistema';

// Configurar breadcrumbs
$breadcrumbs = [
    'Dashboard' => '../../index.php',
    'Estadísticas' => ''
];

// Incluir archivos de cabecera y barra lateral
require_once '../../includes/header.php';
require_once '../../includes/sidebar.php';

// Contenido específico de esta página
ob_start();
?>

<!-- Main content -->
<section class="content">
    <div class="container-fluid">
        <!-- Info boxes -->
        <div class="row">
            <div class="col-12 col-sm-6 col-md-3">
                <div class="info-box">
                    <span class="info-box-icon bg-info"><i class="fas fa-bell"></i></span>
                    <div class="info-box-content">
                        <span class="info-box-text">Alertas Hoy</span>
                        <span class="info-box-number"><?php echo $alertsToday; ?></span>
                    </div>
                </div>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
                <div class="info-box">
                    <span class="info-box-icon bg-success"><i class="fas fa-calendar-week"></i></span>
                    <div class="info-box-content">
                        <span class="info-box-text">Alertas Esta Semana</span>
                        <span class="info-box-number"><?php echo $alertsThisWeek; ?></span>
                    </div>
                </div>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
                <div class="info-box">
                    <span class="info-box-icon bg-warning"><i class="fas fa-calendar-alt"></i></span>
                    <div class="info-box-content">
                        <span class="info-box-text">Alertas Este Mes</span>
                        <span class="info-box-number"><?php echo $alertsThisMonth; ?></span>
                    </div>
                </div>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
                <div class="info-box">
                    <span class="info-box-icon bg-danger"><i class="fas fa-exclamation-circle"></i></span>
                    <div class="info-box-content">
                        <span class="info-box-text">Alertas Pendientes</span>
                        <span class="info-box-number"><?php echo $alertsPending; ?></span>
                    </div>
                </div>
            </div>
        </div>
        <!-- Gráficos principales -->
        <div class="row">
            <div class="col-md-6">
                <!-- Gráfico de Alertas por Tipo -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-chart-pie mr-1"></i>
                            Distribución de Alertas por Tipo
                        </h3>
                        <div class="card-tools">
                            <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                <i class="fas fa-minus"></i>
                            </button>
                            <button type="button" class="btn btn-tool" data-card-widget="remove">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="alertsByTypeChart" style="height: 300px;"></canvas>
                    </div>
                </div>
                <!-- Gráfico de Alertas por Operador -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-user mr-1"></i>
                            Top Operadores con Más Alertas
                        </h3>
                        <div class="card-tools">
                            <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                <i class="fas fa-minus"></i>
                            </button>
                            <button type="button" class="btn btn-tool" data-card-widget="remove">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="alertsByOperatorChart" style="height: 300px;"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <!-- Gráfico de Tendencia de Alertas -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-chart-line mr-1"></i>
                            Tendencia de Alertas
                        </h3>
                        <div class="card-tools">
                            <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                <i class="fas fa-minus"></i>
                            </button>
                            <button type="button" class="btn btn-tool" data-card-widget="remove">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="alertsTrendChart" style="height: 300px;"></canvas>
                    </div>
                </div>
                <!-- Estadísticas rápidas -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-info-circle mr-1"></i>
                            Información del Sistema
                        </h3>
                        <div class="card-tools">
                            <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                <i class="fas fa-minus"></i>
                            </button>
                            <button type="button" class="btn btn-tool" data-card-widget="remove">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="info-box bg-light">
                                    <div class="info-box-content">
                                        <span class="info-box-text text-center text-muted">Total Operadores</span>
                                        <span class="info-box-number text-center text-muted mb-0"><?php echo $totalOperators; ?></span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="info-box bg-light">
                                    <div class="info-box-content">
                                        <span class="info-box-text text-center text-muted">Total Máquinas</span>
                                        <span class="info-box-number text-center text-muted mb-0"><?php echo $totalMachines; ?></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Estado de los dispositivos -->
                        <h5 class="mt-4 mb-2">Estado de Dispositivos</h5>
                        <?php
                        // Obtener estado de dispositivos
                        $devicesQuery = "SELECT id, name, status FROM devices ORDER BY name";
                        $devices = [];
                        
                        // Verificar si existe la tabla devices
                        try {
                            $devices = db_fetch_all($devicesQuery);
                        } catch (Exception $e) {
                            // Si hay error, probablemente la tabla no existe
                            echo '<div class="alert alert-info">No hay información de dispositivos disponible.</div>';
                        }
                        
                        if (empty($devices)) {
                            echo '<div class="alert alert-info">No hay dispositivos registrados.</div>';
                        } else {
                            foreach ($devices as $device) {
                                $statusClass = isset($device['status']) && $device['status'] == 'online' ? 'success' : 'danger';
                                $statusText = isset($device['status']) && $device['status'] == 'online' ? 'En línea' : 'Desconectado';
                        ?>
                                <div class="progress-group">
                                    <?php echo $device['name']; ?>
                                    <span class="float-right">
                                        <span class="badge bg-<?php echo $statusClass; ?>">
                                            <?php echo $statusText; ?>
                                        </span>
                                    </span>
                                </div>
                        <?php
                            }
                        }
                        ?>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<?php
// Capturar el contenido y guardarlo en $pageContent
$pageContent = ob_get_clean();

// Definir contenido para la sección de acciones (botones en header)
$actions = '
<a href="export.php" class="btn btn-success">
    <i class="fas fa-file-excel"></i> Exportar Estadísticas
</a>
';

// Incluir archivo de contenido
require_once '../../includes/content.php';
?>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de alertas por tipo
        const alertTypeCtx = document.getElementById('alertsByTypeChart').getContext('2d');
        const alertTypeData = {
            labels: [],
            datasets: [{
                label: 'Cantidad de Alertas',
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(199, 199, 199, 0.6)',
                    'rgba(83, 102, 255, 0.6)'
                ],
                borderWidth: 1
            }]
        };

        const alertTypeChart = new Chart(alertTypeCtx, {
            type: 'pie',
            data: alertTypeData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribución de Alertas por Tipo'
                    }
                }
            }
        });

        // Gráfico de operadores
        const operatorCtx = document.getElementById('alertsByOperatorChart').getContext('2d');
        const operatorData = {
            labels: [],
            datasets: [{
                label: 'Cantidad de Alertas',
                data: [],
                backgroundColor: 'rgba(60, 141, 188, 0.7)',
                borderColor: 'rgba(60, 141, 188, 1)',
                borderWidth: 1
            }]
        };

        const operatorChart = new Chart(operatorCtx, {
            type: 'bar',
            data: operatorData,
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Top Operadores con Más Alertas'
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Datos para el gráfico de tendencias
        const trendCtx = document.getElementById('alertsTrendChart').getContext('2d');
        const trendData = {
            labels: [],
            datasets: [{
                label: 'Alertas por Día',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }]
        };

        const trendChart = new Chart(trendCtx, {
            type: 'line',
            data: trendData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Tendencia de Alertas en los Últimos 30 Días'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Número de Alertas'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Fecha'
                        }
                    }
                }
            }
        });

        // Cargar datos de los gráficos con AJAX
        fetch('../../includes/charts/alerts_by_type.php')
            .then(response => response.json())
            .then(data => {
                alertTypeChart.data.labels = data.map(item => item.label);
                alertTypeChart.data.datasets[0].data = data.map(item => item.count);
                alertTypeChart.update();
            })
            .catch(error => console.error('Error al cargar datos de tipos de alertas:', error));

        fetch('../../includes/charts/alerts_by_operator.php')
            .then(response => response.json())
            .then(data => {
                operatorChart.data.labels = data.map(item => item.name);
                operatorChart.data.datasets[0].data = data.map(item => item.alert_count);
                operatorChart.update();
            })
            .catch(error => console.error('Error al cargar datos de operadores:', error));

        fetch('../../includes/charts/alerts_trend.php')
            .then(response => response.json())
            .then(data => {
                trendChart.data.labels = data.map(item => item.date);
                trendChart.data.datasets[0].data = data.map(item => item.count);
                trendChart.update();
            })
            .catch(error => console.error('Error al cargar datos de tendencias:', error));
    });
</script>

<?php
// Incluir archivo de pie de página
require_once '../../includes/footer.php';
?>