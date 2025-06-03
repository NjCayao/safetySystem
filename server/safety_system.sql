-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-05-2025 a las 02:14:25
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `safety_system`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alerts`
--

CREATE TABLE `alerts` (
  `id` int(11) NOT NULL,
  `operator_id` varchar(50) DEFAULT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `alert_type` enum('fatigue','phone','smoking','unauthorized','other','yawn','distraction','behavior') NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `image_path` varchar(255) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `acknowledged` tinyint(1) DEFAULT 0,
  `acknowledged_by` varchar(50) DEFAULT NULL,
  `acknowledgement_time` datetime DEFAULT NULL,
  `actions_taken` text DEFAULT NULL,
  `ack_comments` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alerts`
--

INSERT INTO `alerts` (`id`, `operator_id`, `machine_id`, `alert_type`, `timestamp`, `image_path`, `details`, `acknowledged`, `acknowledged_by`, `acknowledgement_time`, `actions_taken`, `ack_comments`) VALUES
(1, 'OP001', 'MAQ001', 'fatigue', '2025-05-01 11:36:16', NULL, 'Detección de fatiga en operador', 1, 'admin', '2025-05-06 02:50:41', NULL, NULL),
(2, 'OP002', 'MAQ003', 'phone', '2025-05-01 12:36:16', NULL, 'Uso de teléfono detectado', 1, NULL, NULL, NULL, NULL),
(3, 'OP001', 'MAQ001', 'yawn', '2025-05-01 13:06:16', NULL, 'Bostezo detectado', 1, 'admin', '2025-05-06 02:50:53', NULL, NULL),
(4, 'OP003', 'MAQ004', 'distraction', '2025-05-01 13:21:16', NULL, 'Distracción detectada', 1, 'admin', '2025-05-03 04:15:10', '', ''),
(5, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 01:10:32', 'uploads/alerts/2025-05/47469940_fatigue_20250506_011032.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_011032\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 01:56:19', NULL, NULL),
(6, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 01:10:50', 'uploads/alerts/2025-05/47469940_fatigue_20250506_011050.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_011050\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 2\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 01:57:00', '', ''),
(7, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 01:11:10', 'uploads/alerts/2025-05/47469940_fatigue_20250506_011110.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_011110\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:00:53', NULL, NULL),
(8, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 01:36:46', 'uploads/alerts/2025-05/47469940_fatigue_20250506_013646.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_013646\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:19:01', '', ''),
(9, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 01:37:27', 'uploads/alerts/2025-05/47469940_fatigue_20250506_013727.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_013727\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 2\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:18:28', '', ''),
(10, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 01:58:01', 'uploads/alerts/2025-05/47469940_fatigue_20250506_015801.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_015801\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:24:22', NULL, NULL),
(11, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:12:45', 'uploads/alerts/2025-05/47469940_fatigue_20250506_021245.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_021245\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:39:04', NULL, NULL),
(12, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:13:17', 'uploads/alerts/2025-05/47469940_fatigue_20250506_021317.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_021317\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 2\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:41:11', NULL, NULL),
(13, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:14:05', 'uploads/alerts/2025-05/47469940_fatigue_20250506_021405.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_021405\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'admin', '2025-05-06 02:41:31', '', ''),
(14, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:42:07', 'uploads/alerts/2025-05/47469940_fatigue_20250506_024207.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_024207\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 0, NULL, NULL, NULL, NULL),
(15, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:47:34', 'uploads/alerts/2025-05/47469940_fatigue_20250506_024734.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_024734\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 0, NULL, NULL, NULL, NULL),
(16, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:57:05', 'uploads/alerts/2025-05/47469940_fatigue_20250506_025705.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_025705\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 0, NULL, NULL, NULL, NULL),
(17, 'OP459', 'MAQ136', 'fatigue', '2025-05-06 02:58:07', 'uploads/alerts/2025-05/47469940_fatigue_20250506_025807.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250506_025807\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 2\r\n\r\nAcci?n recomendada: El operador debe tomar un descanso inmediato de al menos 15 minutos.\r\n', 1, 'super', '2025-05-06 15:05:41', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alert_settings`
--

CREATE TABLE `alert_settings` (
  `id` int(11) NOT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `alert_type` enum('fatigue','phone','smoking','break','all','yawn','distraction','behavior') NOT NULL,
  `enabled` tinyint(1) DEFAULT 1,
  `interval_seconds` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `last_modified` datetime DEFAULT current_timestamp(),
  `modified_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alert_settings`
--

INSERT INTO `alert_settings` (`id`, `machine_id`, `alert_type`, `enabled`, `interval_seconds`, `message`, `last_modified`, `modified_by`) VALUES
(1, NULL, 'break', 1, 10800, 'Es hora de tomar una pausa activa de 10 minutos', '2025-05-01 13:36:16', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `device_id` varchar(50) NOT NULL,
  `api_key` varchar(255) NOT NULL,
  `device_type` varchar(30) NOT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `status` enum('online','offline','syncing','error') DEFAULT 'offline',
  `last_sync` datetime DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `events`
--

CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `device_id` varchar(50) NOT NULL,
  `event_type` enum('fatigue','cellphone','smoking','unrecognized_operator','other') NOT NULL,
  `operator_id` varchar(50) DEFAULT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `event_data` text DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `event_time` datetime NOT NULL,
  `server_time` datetime NOT NULL DEFAULT current_timestamp(),
  `sync_batch_id` varchar(50) DEFAULT NULL,
  `is_synced` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `machines`
--

CREATE TABLE `machines` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(50) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `status` enum('active','maintenance','inactive') DEFAULT 'active',
  `last_maintenance` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `machines`
--

INSERT INTO `machines` (`id`, `name`, `type`, `location`, `status`, `last_maintenance`, `notes`) VALUES
('MAQ001', 'Excavadora Cat 320', 'Excavadora', 'Zona Norte', 'active', NULL, NULL),
('MAQ002', 'Cargadora Frontal 950H', 'Cargadora', 'Zona Sur', 'active', NULL, NULL),
('MAQ003', 'Grúa Torre Liebherr', 'Grúa', 'Zona Central', 'maintenance', NULL, NULL),
('MAQ004', 'Bulldozer D8T', 'Bulldozer', 'Zona Este', 'active', NULL, NULL),
('MAQ136', 'Tractor D8T TRA01', 'Bulldozer', 'Diques', 'active', NULL, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modules`
--

CREATE TABLE `modules` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `order` int(11) DEFAULT 0,
  `status` enum('active','inactive') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modules`
--

INSERT INTO `modules` (`id`, `name`, `description`, `url`, `icon`, `parent_id`, `order`, `status`) VALUES
(1, 'Dashboard', 'Panel principal del sistema', '/index.php', 'fas fa-tachometer-alt', NULL, 1, 'active'),
(2, 'Operadores', 'Gestión de operadores', '/pages/operators/index.php', 'fas fa-users', NULL, 2, 'active'),
(3, 'Máquinas', 'Gestión de maquinaria', '/pages/machines/index.php', 'fas fa-truck', NULL, 3, 'active'),
(4, 'Alertas', 'Sistema de alertas', '/pages/alerts/index.php', 'fas fa-bell', NULL, 4, 'active'),
(5, 'Estadísticas', 'Reportes estadísticos', '/pages/dashboard/index.php', 'fas fa-chart-bar', NULL, 5, 'active'),
(6, 'Reportes', 'Generación de reportes', '/pages/reports/daily.php', 'fas fa-file-alt', NULL, 6, 'active'),
(7, 'Usuarios', 'Administración de usuarios', '/pages/users/index.php', 'fas fa-user-shield', NULL, 7, 'active'),
(8, 'Configuración', 'Configuración del sistema', '/pages/settings.php', 'fas fa-cog', NULL, 8, 'active');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `operators`
--

CREATE TABLE `operators` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `position` varchar(100) DEFAULT NULL,
  `registration_date` datetime DEFAULT current_timestamp(),
  `last_login` datetime DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `notes` text DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `dni_number` varchar(20) DEFAULT NULL,
  `license_number` varchar(50) DEFAULT NULL,
  `license_expiry` date DEFAULT NULL,
  `license_status` enum('active','expired') DEFAULT NULL,
  `face_photo1` varchar(255) DEFAULT NULL,
  `face_photo2` varchar(255) DEFAULT NULL,
  `face_photo3` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `operators`
--

INSERT INTO `operators` (`id`, `name`, `position`, `registration_date`, `last_login`, `status`, `notes`, `photo_path`, `dni_number`, `license_number`, `license_expiry`, `license_status`, `face_photo1`, `face_photo2`, `face_photo3`) VALUES
('OP001', 'Juan Pérez', 'Operador de Maquinaria Pesada', '2025-05-01 13:36:16', NULL, 'active', 'Operador experimentado', NULL, '47465580', NULL, NULL, NULL, NULL, NULL, NULL),
('OP002', 'María López', 'Operadora de Grúa', '2025-05-01 13:36:16', NULL, 'active', 'Certificada en operación de grúas de alto tonelaje', NULL, '47465541', NULL, NULL, NULL, NULL, NULL, NULL),
('OP003', 'Carlos Rodríguez', 'Operador de Excavadora', '2025-05-01 13:36:16', NULL, 'active', 'Especializado en terrenos difíciles', NULL, '47458810', NULL, NULL, NULL, NULL, NULL, NULL),
('OP004', 'Ana Martínez', 'Operadora de Cargadora', '2025-05-01 13:36:16', NULL, 'inactive', 'En proceso de recertificación', NULL, '47458820', NULL, NULL, NULL, NULL, NULL, NULL),
('OP459', 'Nilson Cayao', 'Op. Tractor Oruga D8T', '2025-05-03 11:47:41', NULL, 'active', '', '/safety_system/server/operator-photo/47469940/profile_20250503_114741.jpg', '47469940', 'AIIB', '2025-08-20', 'active', '/safety_system/server/operator-photo/47469940/face1_20250503_114741.jpg', '/safety_system/server/operator-photo/47469940/face2_20250503_114741.jpg', '/safety_system/server/operator-photo/47469940/face3_20250503_114741.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `operator_machine`
--

CREATE TABLE `operator_machine` (
  `id` int(11) NOT NULL,
  `operator_id` varchar(50) NOT NULL,
  `machine_id` varchar(50) NOT NULL,
  `assigned_date` datetime DEFAULT current_timestamp(),
  `is_current` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `operator_machine`
--

INSERT INTO `operator_machine` (`id`, `operator_id`, `machine_id`, `assigned_date`, `is_current`) VALUES
(1, 'OP001', 'MAQ001', '2025-05-01 13:36:16', 1),
(2, 'OP002', 'MAQ003', '2025-05-01 13:36:16', 1),
(3, 'OP003', 'MAQ004', '2025-05-01 13:36:16', 1),
(4, 'OP004', 'MAQ002', '2025-05-01 13:36:16', 0),
(5, 'OP459', 'MAQ136', '2025-05-03 11:54:16', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `module_id` int(11) NOT NULL,
  `can_view` tinyint(1) DEFAULT 0,
  `can_create` tinyint(1) DEFAULT 0,
  `can_edit` tinyint(1) DEFAULT 0,
  `can_delete` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permissions`
--

INSERT INTO `permissions` (`id`, `user_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `created_at`, `updated_at`) VALUES
(21, 2, 1, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(22, 2, 2, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(23, 2, 3, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(24, 2, 4, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(25, 2, 5, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(26, 2, 6, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(27, 2, 7, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL),
(28, 2, 8, 1, 1, 1, 1, '2025-05-06 15:20:10', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sync_batches`
--

CREATE TABLE `sync_batches` (
  `id` varchar(50) NOT NULL,
  `device_id` varchar(50) NOT NULL,
  `batch_size` int(11) NOT NULL,
  `status` enum('processing','completed','failed') NOT NULL DEFAULT 'processing',
  `started_at` datetime NOT NULL DEFAULT current_timestamp(),
  `completed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `system_logs`
--

CREATE TABLE `system_logs` (
  `id` int(11) NOT NULL,
  `log_type` enum('info','warning','error','critical') NOT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `message` text NOT NULL,
  `details` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `system_logs`
--

INSERT INTO `system_logs` (`id`, `log_type`, `machine_id`, `timestamp`, `message`, `details`) VALUES
(1, 'info', NULL, '2025-05-02 09:11:09', 'Usuario admin ha iniciado sesión', 'IP: ::1'),
(2, 'info', NULL, '2025-05-03 08:41:32', 'Usuario admin ha iniciado sesión', 'IP: ::1'),
(3, 'info', NULL, '2025-05-06 01:26:31', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(4, 'info', 'MAQ136', '2025-05-06 01:26:31', 'Alerta creada para Nilson Cayao (ID: 5)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_011032.jpg'),
(5, 'info', 'MAQ136', '2025-05-06 01:26:31', 'Alerta creada para Nilson Cayao (ID: 6)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_011050.jpg'),
(6, 'info', 'MAQ136', '2025-05-06 01:26:31', 'Alerta creada para Nilson Cayao (ID: 7)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_011110.jpg'),
(7, 'info', NULL, '2025-05-06 01:26:31', 'Monitoreo de reportes finalizado. Procesados: 3. Fallidos: 0', 'Script: monitor_reports.php'),
(8, 'info', NULL, '2025-05-06 01:27:14', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(9, 'info', NULL, '2025-05-06 01:27:14', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(10, 'info', NULL, '2025-05-06 01:27:23', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(11, 'info', NULL, '2025-05-06 01:27:23', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(12, 'info', NULL, '2025-05-06 01:27:23', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(13, 'info', NULL, '2025-05-06 01:27:23', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(14, 'info', NULL, '2025-05-06 01:33:05', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(15, 'info', NULL, '2025-05-06 01:33:05', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(16, 'info', NULL, '2025-05-06 01:33:05', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(17, 'info', NULL, '2025-05-06 01:33:05', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(18, 'info', NULL, '2025-05-06 01:34:05', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(19, 'info', NULL, '2025-05-06 01:34:05', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(20, 'info', NULL, '2025-05-06 01:55:07', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(21, 'info', 'MAQ136', '2025-05-06 01:55:07', 'Alerta creada para Nilson Cayao (ID: 8)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_013646.jpg'),
(22, 'info', 'MAQ136', '2025-05-06 01:55:07', 'Alerta creada para Nilson Cayao (ID: 9)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_013727.jpg'),
(23, 'info', NULL, '2025-05-06 01:55:07', 'Monitoreo de reportes finalizado. Procesados: 2. Fallidos: 0', 'Script: monitor_reports.php'),
(24, 'info', NULL, '2025-05-06 01:55:11', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(25, 'info', NULL, '2025-05-06 01:55:11', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(26, 'info', NULL, '2025-05-06 01:55:24', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(27, 'info', NULL, '2025-05-06 01:55:24', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(28, 'info', NULL, '2025-05-06 01:55:53', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(29, 'info', NULL, '2025-05-06 01:55:53', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(30, 'info', NULL, '2025-05-06 01:55:53', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(31, 'info', NULL, '2025-05-06 01:55:53', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(32, 'info', NULL, '2025-05-06 01:56:32', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(33, 'info', NULL, '2025-05-06 01:56:32', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(34, 'info', NULL, '2025-05-06 01:56:32', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(35, 'info', NULL, '2025-05-06 01:56:32', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(36, 'info', NULL, '2025-05-06 01:57:03', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(37, 'info', NULL, '2025-05-06 01:57:03', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(38, 'info', NULL, '2025-05-06 01:57:03', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(39, 'info', NULL, '2025-05-06 01:57:03', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(40, 'info', NULL, '2025-05-06 01:58:03', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(41, 'info', 'MAQ136', '2025-05-06 01:58:03', 'Alerta creada para Nilson Cayao (ID: 10)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_015801.jpg'),
(42, 'info', NULL, '2025-05-06 01:58:03', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(43, 'info', NULL, '2025-05-06 01:58:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(44, 'info', NULL, '2025-05-06 01:58:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(45, 'info', NULL, '2025-05-06 01:58:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(46, 'info', NULL, '2025-05-06 01:58:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(47, 'info', NULL, '2025-05-06 01:59:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(48, 'info', NULL, '2025-05-06 01:59:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(49, 'info', NULL, '2025-05-06 02:00:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(50, 'info', NULL, '2025-05-06 02:00:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(51, 'info', NULL, '2025-05-06 02:02:24', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(52, 'info', NULL, '2025-05-06 02:02:24', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(53, 'info', NULL, '2025-05-06 02:03:24', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(54, 'info', NULL, '2025-05-06 02:03:24', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(55, 'info', NULL, '2025-05-06 02:04:24', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(56, 'info', NULL, '2025-05-06 02:04:24', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(57, 'info', NULL, '2025-05-06 02:04:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(58, 'info', NULL, '2025-05-06 02:04:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(59, 'info', NULL, '2025-05-06 02:04:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(60, 'info', NULL, '2025-05-06 02:04:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(61, 'info', NULL, '2025-05-06 02:05:38', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(62, 'info', NULL, '2025-05-06 02:05:38', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(63, 'info', NULL, '2025-05-06 02:06:38', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(64, 'info', NULL, '2025-05-06 02:06:38', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(65, 'info', NULL, '2025-05-06 02:07:38', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(66, 'info', NULL, '2025-05-06 02:07:38', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(67, 'info', NULL, '2025-05-06 02:08:38', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(68, 'info', NULL, '2025-05-06 02:08:38', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(69, 'info', NULL, '2025-05-06 02:09:38', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(70, 'info', NULL, '2025-05-06 02:09:38', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(71, 'info', NULL, '2025-05-06 02:10:38', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(72, 'info', NULL, '2025-05-06 02:10:38', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(73, 'info', NULL, '2025-05-06 02:10:54', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(74, 'info', NULL, '2025-05-06 02:10:54', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(75, 'info', NULL, '2025-05-06 02:10:54', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(76, 'info', NULL, '2025-05-06 02:10:54', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(77, 'info', NULL, '2025-05-06 02:11:54', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(78, 'info', NULL, '2025-05-06 02:11:54', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(79, 'info', NULL, '2025-05-06 02:12:54', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(80, 'info', 'MAQ136', '2025-05-06 02:12:54', 'Alerta creada para Nilson Cayao (ID: 11)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_021245.jpg'),
(81, 'info', NULL, '2025-05-06 02:12:54', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(82, 'info', NULL, '2025-05-06 02:13:54', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(83, 'info', 'MAQ136', '2025-05-06 02:13:54', 'Alerta creada para Nilson Cayao (ID: 12)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_021317.jpg'),
(84, 'info', NULL, '2025-05-06 02:13:54', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(85, 'info', NULL, '2025-05-06 02:14:55', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(86, 'info', 'MAQ136', '2025-05-06 02:14:55', 'Alerta creada para Nilson Cayao (ID: 13)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_021405.jpg'),
(87, 'info', NULL, '2025-05-06 02:14:55', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(88, 'info', NULL, '2025-05-06 02:15:55', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(89, 'info', NULL, '2025-05-06 02:15:55', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(90, 'info', NULL, '2025-05-06 02:16:55', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(91, 'info', NULL, '2025-05-06 02:16:55', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(92, 'info', NULL, '2025-05-06 02:17:05', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(93, 'info', NULL, '2025-05-06 02:17:05', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(94, 'info', NULL, '2025-05-06 02:18:53', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(95, 'info', NULL, '2025-05-06 02:18:53', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(96, 'info', NULL, '2025-05-06 02:18:53', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(97, 'info', NULL, '2025-05-06 02:18:53', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(98, 'info', NULL, '2025-05-06 02:19:16', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(99, 'info', NULL, '2025-05-06 02:19:16', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(100, 'info', NULL, '2025-05-06 02:19:16', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(101, 'info', NULL, '2025-05-06 02:19:16', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(102, 'info', NULL, '2025-05-06 02:20:16', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(103, 'info', NULL, '2025-05-06 02:20:16', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(104, 'info', NULL, '2025-05-06 02:21:16', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(105, 'info', NULL, '2025-05-06 02:21:16', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(106, 'info', NULL, '2025-05-06 02:22:21', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(107, 'info', NULL, '2025-05-06 02:22:21', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(108, 'info', NULL, '2025-05-06 02:22:21', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(109, 'info', NULL, '2025-05-06 02:22:21', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(110, 'info', NULL, '2025-05-06 02:23:05', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(111, 'info', NULL, '2025-05-06 02:23:05', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(112, 'info', NULL, '2025-05-06 02:23:05', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(113, 'info', NULL, '2025-05-06 02:23:05', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(114, 'info', NULL, '2025-05-06 02:23:32', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(115, 'info', NULL, '2025-05-06 02:23:32', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(116, 'info', NULL, '2025-05-06 02:23:32', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(117, 'info', NULL, '2025-05-06 02:23:32', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(118, 'info', NULL, '2025-05-06 02:24:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(119, 'info', NULL, '2025-05-06 02:24:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(120, 'info', NULL, '2025-05-06 02:24:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(121, 'info', NULL, '2025-05-06 02:24:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(122, 'info', NULL, '2025-05-06 02:26:04', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(123, 'info', NULL, '2025-05-06 02:26:04', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(124, 'info', NULL, '2025-05-06 02:27:04', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(125, 'info', NULL, '2025-05-06 02:27:04', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(126, 'info', NULL, '2025-05-06 02:28:04', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(127, 'info', NULL, '2025-05-06 02:28:04', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(128, 'info', NULL, '2025-05-06 02:29:04', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(129, 'info', NULL, '2025-05-06 02:29:04', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(130, 'info', NULL, '2025-05-06 02:29:40', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(131, 'info', NULL, '2025-05-06 02:29:40', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(132, 'info', NULL, '2025-05-06 02:29:40', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(133, 'info', NULL, '2025-05-06 02:29:40', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(134, 'info', NULL, '2025-05-06 02:30:40', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(135, 'info', NULL, '2025-05-06 02:30:40', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(136, 'info', NULL, '2025-05-06 02:31:25', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(137, 'info', NULL, '2025-05-06 02:31:25', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(138, 'info', NULL, '2025-05-06 02:31:25', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(139, 'info', NULL, '2025-05-06 02:31:25', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(140, 'info', NULL, '2025-05-06 02:32:26', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(141, 'info', NULL, '2025-05-06 02:32:26', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(142, 'info', NULL, '2025-05-06 02:33:26', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(143, 'info', NULL, '2025-05-06 02:33:26', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(144, 'info', NULL, '2025-05-06 02:34:26', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(145, 'info', NULL, '2025-05-06 02:34:26', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(146, 'info', NULL, '2025-05-06 02:34:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(147, 'info', NULL, '2025-05-06 02:34:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(148, 'info', NULL, '2025-05-06 02:34:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(149, 'info', NULL, '2025-05-06 02:34:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(150, 'info', NULL, '2025-05-06 02:34:56', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(151, 'info', NULL, '2025-05-06 02:34:56', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(152, 'info', NULL, '2025-05-06 02:34:56', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(153, 'info', NULL, '2025-05-06 02:34:56', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(154, 'info', NULL, '2025-05-06 02:35:23', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(155, 'info', NULL, '2025-05-06 02:35:23', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(156, 'info', NULL, '2025-05-06 02:35:23', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(157, 'info', NULL, '2025-05-06 02:35:23', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(158, 'info', NULL, '2025-05-06 02:36:18', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(159, 'info', NULL, '2025-05-06 02:36:18', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(160, 'info', NULL, '2025-05-06 02:36:18', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(161, 'info', NULL, '2025-05-06 02:36:18', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(162, 'info', NULL, '2025-05-06 02:37:19', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(163, 'info', NULL, '2025-05-06 02:37:19', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(164, 'info', NULL, '2025-05-06 02:38:02', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(165, 'info', NULL, '2025-05-06 02:38:02', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(166, 'info', NULL, '2025-05-06 02:38:02', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(167, 'info', NULL, '2025-05-06 02:38:02', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(168, 'info', NULL, '2025-05-06 02:39:02', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(169, 'info', NULL, '2025-05-06 02:39:02', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(170, 'info', NULL, '2025-05-06 02:40:50', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(171, 'info', NULL, '2025-05-06 02:40:50', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(172, 'info', NULL, '2025-05-06 02:41:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(173, 'info', NULL, '2025-05-06 02:41:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(174, 'info', NULL, '2025-05-06 02:41:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(175, 'info', NULL, '2025-05-06 02:41:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(176, 'info', 'MAQ136', '2025-05-06 02:41:11', 'Alerta #12 marcada como atendida por admin', 'Tipo: fatigue, Operador: OP459'),
(177, 'info', NULL, '2025-05-06 02:41:23', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(178, 'info', NULL, '2025-05-06 02:41:23', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(179, 'info', NULL, '2025-05-06 02:41:23', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(180, 'info', NULL, '2025-05-06 02:41:23', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(181, 'info', NULL, '2025-05-06 02:41:34', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(182, 'info', NULL, '2025-05-06 02:41:34', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(183, 'info', NULL, '2025-05-06 02:41:34', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(184, 'info', NULL, '2025-05-06 02:41:34', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(185, 'info', NULL, '2025-05-06 02:42:34', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(186, 'info', 'MAQ136', '2025-05-06 02:42:34', 'Alerta creada para Nilson Cayao (ID: 14)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_024207.jpg'),
(187, 'info', NULL, '2025-05-06 02:42:34', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(188, 'info', NULL, '2025-05-06 02:43:35', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(189, 'info', NULL, '2025-05-06 02:43:35', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(190, 'info', NULL, '2025-05-06 02:44:35', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(191, 'info', NULL, '2025-05-06 02:44:35', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(192, 'info', NULL, '2025-05-06 02:45:35', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(193, 'info', NULL, '2025-05-06 02:45:35', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(194, 'info', NULL, '2025-05-06 02:46:35', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(195, 'info', NULL, '2025-05-06 02:46:35', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(196, 'info', NULL, '2025-05-06 02:46:59', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(197, 'info', NULL, '2025-05-06 02:46:59', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(198, 'info', NULL, '2025-05-06 02:46:59', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(199, 'info', NULL, '2025-05-06 02:46:59', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(200, 'info', NULL, '2025-05-06 02:47:59', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(201, 'info', 'MAQ136', '2025-05-06 02:47:59', 'Alerta creada para Nilson Cayao (ID: 15)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_024734.jpg'),
(202, 'info', NULL, '2025-05-06 02:47:59', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(203, 'info', NULL, '2025-05-06 02:49:00', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(204, 'info', NULL, '2025-05-06 02:49:00', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(205, 'info', NULL, '2025-05-06 02:50:00', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(206, 'info', NULL, '2025-05-06 02:50:00', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(207, 'info', NULL, '2025-05-06 02:50:33', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(208, 'info', NULL, '2025-05-06 02:50:33', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(209, 'info', NULL, '2025-05-06 02:50:33', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(210, 'info', NULL, '2025-05-06 02:50:33', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(211, 'info', 'MAQ001', '2025-05-06 02:50:41', 'Alerta #1 marcada como atendida por admin', 'Tipo: fatigue, Operador: OP001'),
(212, 'info', NULL, '2025-05-06 02:50:44', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(213, 'info', NULL, '2025-05-06 02:50:44', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(214, 'info', NULL, '2025-05-06 02:50:44', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(215, 'info', NULL, '2025-05-06 02:50:44', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(216, 'info', NULL, '2025-05-06 02:50:51', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(217, 'info', NULL, '2025-05-06 02:50:51', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(218, 'info', NULL, '2025-05-06 02:50:51', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(219, 'info', NULL, '2025-05-06 02:50:51', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(220, 'info', 'MAQ001', '2025-05-06 02:50:53', 'Alerta #3 marcada como atendida por admin', 'Tipo: yawn, Operador: OP001'),
(221, 'info', NULL, '2025-05-06 02:50:55', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(222, 'info', NULL, '2025-05-06 02:50:55', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(223, 'info', NULL, '2025-05-06 02:50:55', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(224, 'info', NULL, '2025-05-06 02:50:55', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(225, 'info', NULL, '2025-05-06 02:51:56', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(226, 'info', NULL, '2025-05-06 02:51:56', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(227, 'info', NULL, '2025-05-06 02:52:56', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(228, 'info', NULL, '2025-05-06 02:52:56', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(229, 'info', NULL, '2025-05-06 02:53:56', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(230, 'info', NULL, '2025-05-06 02:53:56', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(231, 'info', NULL, '2025-05-06 02:54:56', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(232, 'info', NULL, '2025-05-06 02:54:56', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(233, 'info', NULL, '2025-05-06 02:55:02', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(234, 'info', NULL, '2025-05-06 02:55:02', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(235, 'info', NULL, '2025-05-06 02:55:53', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(236, 'info', NULL, '2025-05-06 02:55:53', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(237, 'info', NULL, '2025-05-06 02:57:43', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(238, 'info', 'MAQ136', '2025-05-06 02:57:43', 'Alerta creada para Nilson Cayao (ID: 16)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_025705.jpg'),
(239, 'info', NULL, '2025-05-06 02:57:43', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(240, 'info', NULL, '2025-05-06 02:58:18', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(241, 'info', 'MAQ136', '2025-05-06 02:58:18', 'Alerta creada para Nilson Cayao (ID: 17)', 'Tipo: fatigue, Archivo: 47469940_fatigue_20250506_025807.jpg'),
(242, 'info', NULL, '2025-05-06 02:58:18', 'Monitoreo de reportes finalizado. Procesados: 1. Fallidos: 0', 'Script: monitor_reports.php'),
(243, 'info', NULL, '2025-05-06 02:59:48', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(244, 'info', NULL, '2025-05-06 02:59:48', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(245, 'info', NULL, '2025-05-06 02:59:48', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(246, 'info', NULL, '2025-05-06 02:59:48', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(247, 'info', NULL, '2025-05-06 03:00:00', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(248, 'info', NULL, '2025-05-06 03:00:00', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(249, 'info', NULL, '2025-05-06 03:00:00', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(250, 'info', NULL, '2025-05-06 03:00:00', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(251, 'info', NULL, '2025-05-06 03:01:00', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(252, 'info', NULL, '2025-05-06 03:01:00', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(253, 'info', NULL, '2025-05-06 03:02:00', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(254, 'info', NULL, '2025-05-06 03:02:00', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(255, 'info', NULL, '2025-05-06 03:02:42', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(256, 'info', NULL, '2025-05-06 03:02:42', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(257, 'info', NULL, '2025-05-06 03:02:42', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(258, 'info', NULL, '2025-05-06 03:02:42', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(259, 'info', NULL, '2025-05-06 04:29:13', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(260, 'info', NULL, '2025-05-06 04:29:13', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(261, 'info', NULL, '2025-05-06 04:29:13', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(262, 'info', NULL, '2025-05-06 04:29:13', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(263, 'info', NULL, '2025-05-06 04:29:29', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(264, 'info', NULL, '2025-05-06 04:29:29', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(265, 'info', NULL, '2025-05-06 04:29:29', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(266, 'info', NULL, '2025-05-06 04:29:29', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(267, 'info', NULL, '2025-05-06 04:29:51', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(268, 'info', NULL, '2025-05-06 04:29:51', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(269, 'info', NULL, '2025-05-06 04:29:51', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(270, 'info', NULL, '2025-05-06 04:29:51', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(271, 'info', NULL, '2025-05-06 04:30:52', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(272, 'info', NULL, '2025-05-06 04:30:52', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(273, 'info', NULL, '2025-05-06 04:31:52', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(274, 'info', NULL, '2025-05-06 04:31:52', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(275, 'info', NULL, '2025-05-06 04:32:52', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(276, 'info', NULL, '2025-05-06 04:32:52', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(277, 'info', NULL, '2025-05-06 04:33:52', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(278, 'info', NULL, '2025-05-06 04:33:52', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(279, 'info', NULL, '2025-05-06 04:34:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(280, 'info', NULL, '2025-05-06 04:34:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(281, 'info', NULL, '2025-05-06 04:34:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(282, 'info', NULL, '2025-05-06 04:34:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(283, 'info', NULL, '2025-05-06 04:35:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(284, 'info', NULL, '2025-05-06 04:35:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(285, 'info', NULL, '2025-05-06 04:36:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(286, 'info', NULL, '2025-05-06 04:36:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(287, 'info', NULL, '2025-05-06 04:37:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(288, 'info', NULL, '2025-05-06 04:37:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(289, 'info', NULL, '2025-05-06 04:38:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(290, 'info', NULL, '2025-05-06 04:38:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(291, 'info', NULL, '2025-05-06 04:39:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(292, 'info', NULL, '2025-05-06 04:39:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(293, 'info', NULL, '2025-05-06 04:40:17', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(294, 'info', NULL, '2025-05-06 04:40:17', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(295, 'info', NULL, '2025-05-06 04:42:11', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(296, 'info', NULL, '2025-05-06 04:42:11', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(297, 'info', NULL, '2025-05-06 04:43:11', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(298, 'info', NULL, '2025-05-06 04:43:11', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(299, 'info', NULL, '2025-05-06 04:44:11', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(300, 'info', NULL, '2025-05-06 04:44:11', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(301, 'info', NULL, '2025-05-06 04:45:11', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(302, 'info', NULL, '2025-05-06 04:45:11', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(303, 'info', NULL, '2025-05-06 04:45:54', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(304, 'info', NULL, '2025-05-06 04:45:54', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(305, 'info', NULL, '2025-05-06 04:49:46', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(306, 'info', NULL, '2025-05-06 04:49:46', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(307, 'info', NULL, '2025-05-06 04:49:46', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(308, 'info', NULL, '2025-05-06 04:49:46', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(309, 'info', NULL, '2025-05-06 13:39:36', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(310, 'info', NULL, '2025-05-06 13:39:36', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(311, 'info', NULL, '2025-05-06 13:39:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(312, 'info', NULL, '2025-05-06 13:39:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(313, 'info', NULL, '2025-05-06 13:40:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(314, 'info', NULL, '2025-05-06 13:40:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(315, 'info', NULL, '2025-05-06 13:41:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(316, 'info', NULL, '2025-05-06 13:41:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(317, 'info', NULL, '2025-05-06 13:42:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(318, 'info', NULL, '2025-05-06 13:42:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(319, 'info', NULL, '2025-05-06 13:43:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(320, 'info', NULL, '2025-05-06 13:43:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(321, 'info', NULL, '2025-05-06 13:44:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(322, 'info', NULL, '2025-05-06 13:44:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(323, 'info', NULL, '2025-05-06 13:45:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(324, 'info', NULL, '2025-05-06 13:45:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(325, 'info', NULL, '2025-05-06 13:46:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(326, 'info', NULL, '2025-05-06 13:46:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(327, 'info', NULL, '2025-05-06 13:48:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(328, 'info', NULL, '2025-05-06 13:48:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(329, 'info', NULL, '2025-05-06 13:49:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(330, 'info', NULL, '2025-05-06 13:49:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(331, 'info', NULL, '2025-05-06 13:50:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(332, 'info', NULL, '2025-05-06 13:50:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(333, 'info', NULL, '2025-05-06 13:51:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(334, 'info', NULL, '2025-05-06 13:51:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(335, 'info', NULL, '2025-05-06 13:51:47', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(336, 'info', NULL, '2025-05-06 13:51:47', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(337, 'info', NULL, '2025-05-06 13:52:36', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(338, 'info', NULL, '2025-05-06 13:52:36', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(339, 'info', NULL, '2025-05-06 13:53:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(340, 'info', NULL, '2025-05-06 13:53:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(341, 'info', NULL, '2025-05-06 13:54:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(342, 'info', NULL, '2025-05-06 13:54:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(343, 'info', NULL, '2025-05-06 13:56:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(344, 'info', NULL, '2025-05-06 13:56:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(345, 'info', NULL, '2025-05-06 13:57:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(346, 'info', NULL, '2025-05-06 13:57:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(347, 'info', NULL, '2025-05-06 13:58:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(348, 'info', NULL, '2025-05-06 13:58:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(349, 'info', NULL, '2025-05-06 13:59:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(350, 'info', NULL, '2025-05-06 13:59:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(351, 'info', NULL, '2025-05-06 14:00:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(352, 'info', NULL, '2025-05-06 14:00:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(353, 'info', NULL, '2025-05-06 14:01:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(354, 'info', NULL, '2025-05-06 14:01:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(355, 'info', NULL, '2025-05-06 14:01:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(356, 'info', NULL, '2025-05-06 14:01:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(357, 'info', NULL, '2025-05-06 14:02:37', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(358, 'info', NULL, '2025-05-06 14:02:37', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(359, 'info', NULL, '2025-05-06 14:04:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(360, 'info', NULL, '2025-05-06 14:04:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(361, 'info', NULL, '2025-05-06 14:05:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(362, 'info', NULL, '2025-05-06 14:05:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(363, 'info', NULL, '2025-05-06 14:06:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(364, 'info', NULL, '2025-05-06 14:06:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(365, 'info', NULL, '2025-05-06 14:07:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(366, 'info', NULL, '2025-05-06 14:07:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(367, 'info', NULL, '2025-05-06 14:08:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(368, 'info', NULL, '2025-05-06 14:08:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(369, 'info', NULL, '2025-05-06 14:09:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(370, 'info', NULL, '2025-05-06 14:09:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(371, 'info', NULL, '2025-05-06 14:10:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(372, 'info', NULL, '2025-05-06 14:10:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(373, 'info', NULL, '2025-05-06 14:11:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(374, 'info', NULL, '2025-05-06 14:11:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(375, 'info', NULL, '2025-05-06 14:12:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(376, 'info', NULL, '2025-05-06 14:12:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(377, 'info', NULL, '2025-05-06 14:13:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(378, 'info', NULL, '2025-05-06 14:13:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(379, 'info', NULL, '2025-05-06 14:14:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(380, 'info', NULL, '2025-05-06 14:14:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(381, 'info', NULL, '2025-05-06 14:15:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(382, 'info', NULL, '2025-05-06 14:15:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(383, 'info', NULL, '2025-05-06 14:16:08', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(384, 'info', NULL, '2025-05-06 14:16:08', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(385, 'info', NULL, '2025-05-06 14:16:58', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(386, 'info', NULL, '2025-05-06 14:16:58', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(387, 'warning', NULL, '2025-05-06 21:26:54', 'Intento de inicio de sesión fallido para el usuario admin', 'IP: ::1'),
(388, 'warning', NULL, '2025-05-06 21:27:03', 'Intento de inicio de sesión fallido para el usuario admin', 'IP: ::1'),
(389, 'warning', NULL, '2025-05-06 21:34:46', 'Intento de inicio de sesión fallido para el usuario admin', 'IP: ::1'),
(390, 'warning', NULL, '2025-05-06 21:34:50', 'Intento de inicio de sesión fallido para el usuario admin', 'IP: ::1'),
(391, 'warning', NULL, '2025-05-06 21:35:00', 'Intento de inicio de sesión fallido para el usuario admin', 'IP: ::1'),
(392, 'info', NULL, '2025-05-06 21:41:17', 'Usuario admin ha iniciado sesión', 'IP: ::1'),
(393, 'info', NULL, '2025-05-06 22:03:11', 'Usuario admin ha creado el usuario super', 'ID: 2'),
(394, 'info', NULL, '2025-05-06 15:03:59', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(395, 'info', NULL, '2025-05-06 15:03:59', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(396, 'warning', NULL, '2025-05-06 22:04:34', 'Intento de inicio de sesión fallido para el usuario super@gmail.com', 'IP: ::1'),
(397, 'info', NULL, '2025-05-06 22:05:11', 'Usuario super ha iniciado sesión', 'IP: ::1'),
(398, 'info', NULL, '2025-05-06 15:05:34', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(399, 'info', NULL, '2025-05-06 15:05:34', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(400, 'info', NULL, '2025-05-06 15:05:34', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(401, 'info', NULL, '2025-05-06 15:05:34', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(402, 'info', NULL, '2025-05-06 15:05:45', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(403, 'info', NULL, '2025-05-06 15:05:45', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(404, 'info', NULL, '2025-05-06 15:05:45', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(405, 'info', NULL, '2025-05-06 15:05:45', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(406, 'info', NULL, '2025-05-06 22:06:45', 'Usuario admin ha actualizado los permisos del usuario super', 'ID: 2');
INSERT INTO `system_logs` (`id`, `log_type`, `machine_id`, `timestamp`, `message`, `details`) VALUES
(407, 'info', NULL, '2025-05-06 15:06:45', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(408, 'info', NULL, '2025-05-06 15:06:45', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(409, 'info', NULL, '2025-05-06 15:06:50', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(410, 'info', NULL, '2025-05-06 15:06:50', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(411, 'info', NULL, '2025-05-06 15:06:50', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(412, 'info', NULL, '2025-05-06 15:06:50', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(413, 'info', NULL, '2025-05-06 22:19:24', 'Usuario admin ha aplicado el perfil Supervisor al usuario super', 'ID: 2'),
(414, 'info', NULL, '2025-05-06 22:19:50', 'Usuario admin ha actualizado los permisos del usuario super', 'ID: 2'),
(415, 'info', NULL, '2025-05-06 22:20:06', 'Usuario admin ha aplicado el perfil Supervisor al usuario super', 'ID: 2'),
(416, 'info', NULL, '2025-05-06 22:20:10', 'Usuario admin ha actualizado los permisos del usuario super', 'ID: 2'),
(417, 'info', NULL, '2025-05-06 22:22:12', 'Usuario super ha cerrado sesión', 'IP: ::1'),
(418, 'info', NULL, '2025-05-06 15:48:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(419, 'info', NULL, '2025-05-06 15:48:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(420, 'info', NULL, '2025-05-06 15:48:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(421, 'info', NULL, '2025-05-06 15:48:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(422, 'info', NULL, '2025-05-06 15:49:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(423, 'info', NULL, '2025-05-06 15:49:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(424, 'info', NULL, '2025-05-06 15:50:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(425, 'info', NULL, '2025-05-06 15:50:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(426, 'info', NULL, '2025-05-06 15:51:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(427, 'info', NULL, '2025-05-06 15:51:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(428, 'info', NULL, '2025-05-06 15:52:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(429, 'info', NULL, '2025-05-06 15:52:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(430, 'info', NULL, '2025-05-06 15:53:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(431, 'info', NULL, '2025-05-06 15:53:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(432, 'info', NULL, '2025-05-06 15:54:41', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(433, 'info', NULL, '2025-05-06 15:54:41', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(434, 'info', NULL, '2025-05-06 15:56:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(435, 'info', NULL, '2025-05-06 15:56:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(436, 'info', NULL, '2025-05-06 15:57:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(437, 'info', NULL, '2025-05-06 15:57:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(438, 'info', NULL, '2025-05-06 15:58:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(439, 'info', NULL, '2025-05-06 15:58:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(440, 'info', NULL, '2025-05-06 15:59:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(441, 'info', NULL, '2025-05-06 15:59:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(442, 'info', NULL, '2025-05-06 16:00:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(443, 'info', NULL, '2025-05-06 16:00:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(444, 'info', NULL, '2025-05-06 16:01:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(445, 'info', NULL, '2025-05-06 16:01:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(446, 'info', NULL, '2025-05-06 16:02:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(447, 'info', NULL, '2025-05-06 16:02:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(448, 'info', NULL, '2025-05-06 16:03:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(449, 'info', NULL, '2025-05-06 16:03:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(450, 'info', NULL, '2025-05-06 16:04:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(451, 'info', NULL, '2025-05-06 16:04:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(452, 'info', NULL, '2025-05-06 16:05:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(453, 'info', NULL, '2025-05-06 16:05:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(454, 'info', NULL, '2025-05-06 16:06:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(455, 'info', NULL, '2025-05-06 16:06:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(456, 'info', NULL, '2025-05-06 16:07:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(457, 'info', NULL, '2025-05-06 16:07:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(458, 'info', NULL, '2025-05-06 16:08:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(459, 'info', NULL, '2025-05-06 16:08:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(460, 'info', NULL, '2025-05-06 16:09:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(461, 'info', NULL, '2025-05-06 16:09:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(462, 'info', NULL, '2025-05-06 16:10:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(463, 'info', NULL, '2025-05-06 16:10:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(464, 'info', NULL, '2025-05-06 16:11:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(465, 'info', NULL, '2025-05-06 16:11:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(466, 'info', NULL, '2025-05-06 16:12:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(467, 'info', NULL, '2025-05-06 16:12:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(468, 'info', NULL, '2025-05-06 16:13:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(469, 'info', NULL, '2025-05-06 16:13:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(470, 'info', NULL, '2025-05-06 16:14:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(471, 'info', NULL, '2025-05-06 16:14:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(472, 'info', NULL, '2025-05-06 16:15:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(473, 'info', NULL, '2025-05-06 16:15:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(474, 'info', NULL, '2025-05-06 16:16:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(475, 'info', NULL, '2025-05-06 16:16:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(476, 'info', NULL, '2025-05-06 16:17:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(477, 'info', NULL, '2025-05-06 16:17:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(478, 'info', NULL, '2025-05-06 16:18:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(479, 'info', NULL, '2025-05-06 16:18:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(480, 'info', NULL, '2025-05-06 16:19:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(481, 'info', NULL, '2025-05-06 16:19:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(482, 'info', NULL, '2025-05-06 16:20:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(483, 'info', NULL, '2025-05-06 16:20:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(484, 'info', NULL, '2025-05-06 16:21:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(485, 'info', NULL, '2025-05-06 16:21:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(486, 'info', NULL, '2025-05-06 16:22:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(487, 'info', NULL, '2025-05-06 16:22:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(488, 'info', NULL, '2025-05-06 16:23:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(489, 'info', NULL, '2025-05-06 16:23:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(490, 'info', NULL, '2025-05-06 16:24:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(491, 'info', NULL, '2025-05-06 16:24:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(492, 'info', NULL, '2025-05-06 16:25:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(493, 'info', NULL, '2025-05-06 16:25:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(494, 'info', NULL, '2025-05-06 16:26:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(495, 'info', NULL, '2025-05-06 16:26:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(496, 'info', NULL, '2025-05-06 16:27:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(497, 'info', NULL, '2025-05-06 16:27:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(498, 'info', NULL, '2025-05-06 16:28:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(499, 'info', NULL, '2025-05-06 16:28:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(500, 'info', NULL, '2025-05-06 16:29:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(501, 'info', NULL, '2025-05-06 16:29:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(502, 'info', NULL, '2025-05-06 16:30:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(503, 'info', NULL, '2025-05-06 16:30:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php'),
(504, 'info', NULL, '2025-05-06 16:31:09', 'Iniciando monitoreo de reportes', 'Script: monitor_reports.php'),
(505, 'info', NULL, '2025-05-06 16:31:09', 'Monitoreo de reportes finalizado. Procesados: 0. Fallidos: 0', 'Script: monitor_reports.php');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `role` enum('admin','supervisor','staff') NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `name`, `role`, `email`, `last_login`, `status`, `created_at`) VALUES
(1, 'admin', '$2y$10$8mnOFRGdw.yHkQwHg3NRhuWN.mcGcDRZUiJqnK8MzwzEZlsXOuLOe', 'Administrador', 'admin', 'admin@example.com', '2025-05-06 21:41:17', 'active', '2025-05-01 13:36:16'),
(2, 'super', '$2y$10$gj9DJhbnzXkX.ur2vEKXE.6oAU0hcX95Rn66VZ7vvd.FocnRGOcGW', 'Nilson Cayao', 'supervisor', 'super@gmail.com', '2025-05-06 22:05:11', 'active', '2025-05-06 15:03:11');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alerts`
--
ALTER TABLE `alerts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `operator_id` (`operator_id`),
  ADD KEY `machine_id` (`machine_id`);

--
-- Indices de la tabla `alert_settings`
--
ALTER TABLE `alert_settings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `machine_id` (`machine_id`),
  ADD KEY `modified_by` (`modified_by`);

--
-- Indices de la tabla `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `device_id` (`device_id`),
  ADD KEY `machine_id` (`machine_id`);

--
-- Indices de la tabla `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `operator_id` (`operator_id`),
  ADD KEY `machine_id` (`machine_id`),
  ADD KEY `device_id` (`device_id`);

--
-- Indices de la tabla `machines`
--
ALTER TABLE `machines`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `modules`
--
ALTER TABLE `modules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Indices de la tabla `operators`
--
ALTER TABLE `operators`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `operator_machine`
--
ALTER TABLE `operator_machine`
  ADD PRIMARY KEY (`id`),
  ADD KEY `operator_id` (`operator_id`),
  ADD KEY `machine_id` (`machine_id`);

--
-- Indices de la tabla `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_module` (`user_id`,`module_id`),
  ADD KEY `module_id` (`module_id`);

--
-- Indices de la tabla `sync_batches`
--
ALTER TABLE `sync_batches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`);

--
-- Indices de la tabla `system_logs`
--
ALTER TABLE `system_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `machine_id` (`machine_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alerts`
--
ALTER TABLE `alerts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `alert_settings`
--
ALTER TABLE `alert_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `modules`
--
ALTER TABLE `modules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `operator_machine`
--
ALTER TABLE `operator_machine`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `system_logs`
--
ALTER TABLE `system_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=506;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alerts`
--
ALTER TABLE `alerts`
  ADD CONSTRAINT `alerts_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `operators` (`id`),
  ADD CONSTRAINT `alerts_ibfk_2` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`);

--
-- Filtros para la tabla `alert_settings`
--
ALTER TABLE `alert_settings`
  ADD CONSTRAINT `alert_settings_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`),
  ADD CONSTRAINT `alert_settings_ibfk_2` FOREIGN KEY (`modified_by`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `operators` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `events_ibfk_2` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `modules`
--
ALTER TABLE `modules`
  ADD CONSTRAINT `modules_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `modules` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `operator_machine`
--
ALTER TABLE `operator_machine`
  ADD CONSTRAINT `operator_machine_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `operators` (`id`),
  ADD CONSTRAINT `operator_machine_ibfk_2` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`);

--
-- Filtros para la tabla `permissions`
--
ALTER TABLE `permissions`
  ADD CONSTRAINT `permissions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `permissions_ibfk_2` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `system_logs`
--
ALTER TABLE `system_logs`
  ADD CONSTRAINT `system_logs_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
