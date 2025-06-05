-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-06-2025 a las 09:19:49
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
  `device_id` varchar(50) DEFAULT NULL,
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

INSERT INTO `alerts` (`id`, `device_id`, `operator_id`, `machine_id`, `alert_type`, `timestamp`, `image_path`, `details`, `acknowledged`, `acknowledged_by`, `acknowledgement_time`, `actions_taken`, `ack_comments`) VALUES
(77, NULL, 'OP459', 'MAQ136', 'fatigue', '2025-06-04 00:17:06', 'uploads/alerts/2025-06/47469940_fatigue_20250604_001706.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250604_001706\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe cesar el comportamiento peligroso inmediatamente.\r\n', 0, NULL, NULL, NULL, NULL),
(78, NULL, 'OP459', 'MAQ136', 'fatigue', '2025-06-04 00:17:43', 'uploads/alerts/2025-06/47469940_fatigue_20250604_001743.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250604_001743\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 2\r\n\r\nAcci?n recomendada: El operador debe cesar el comportamiento peligroso inmediatamente.\r\n', 0, NULL, NULL, NULL, NULL),
(79, NULL, 'OP459', 'MAQ136', 'fatigue', '2025-06-04 00:18:14', 'uploads/alerts/2025-06/47469940_fatigue_20250604_001814.jpg', 'Reporte de Seguridad - FATIGUE\r\nFecha y hora: 20250604_001814\r\nOperador: Operador: Nilson Cayao\r\nEpisodios de fatiga detectados: 1\r\n\r\nAcci?n recomendada: El operador debe cesar el comportamiento peligroso inmediatamente.\r\n', 0, NULL, NULL, NULL, NULL);

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
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `machine_id` varchar(50) DEFAULT NULL,
  `status` enum('online','offline','syncing','error') DEFAULT 'offline',
  `last_sync` datetime DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `config_json` text DEFAULT NULL COMMENT 'Configuración personalizada en formato JSON',
  `config_version` int(11) DEFAULT 1 COMMENT 'Versión de la configuración actual',
  `config_applied` datetime DEFAULT NULL COMMENT 'Cuándo se aplicó la última configuración',
  `config_pending` tinyint(1) DEFAULT 0 COMMENT 'Si hay cambios pendientes de aplicar',
  `last_config_check` datetime DEFAULT NULL COMMENT 'Última vez que la Pi consultó por configuración'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Disparadores `devices`
--
DELIMITER $$
CREATE TRIGGER `devices_config_version_update` BEFORE UPDATE ON `devices` FOR EACH ROW BEGIN
  -- Si la configuración JSON cambió, incrementar versión y marcar como pendiente
  IF OLD.config_json != NEW.config_json THEN
    SET NEW.config_version = OLD.config_version + 1;
    SET NEW.config_pending = TRUE;
  END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `device_config_history`
--

CREATE TABLE `device_config_history` (
  `id` int(11) NOT NULL,
  `device_id` varchar(50) NOT NULL,
  `changed_by` int(11) NOT NULL,
  `change_type` enum('manual','profile','rollback') NOT NULL DEFAULT 'manual',
  `config_before` text DEFAULT NULL,
  `config_after` text NOT NULL,
  `changes_summary` text DEFAULT NULL COMMENT 'Resumen legible de los cambios',
  `applied_successfully` tinyint(1) DEFAULT NULL COMMENT 'NULL=pendiente, TRUE=aplicado, FALSE=error',
  `error_message` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `applied_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `device_config_profiles`
--

CREATE TABLE `device_config_profiles` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `device_type` varchar(50) DEFAULT NULL COMMENT 'Tipo de dispositivo compatible',
  `config_json` text NOT NULL,
  `is_default` tinyint(1) DEFAULT 0,
  `created_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `device_config_profiles`
--

INSERT INTO `device_config_profiles` (`id`, `name`, `description`, `device_type`, `config_json`, `is_default`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 'Configuración Estándar', 'Configuración balanceada para uso general', 'Raspberry Pi', '{\r\n  \"camera\": {\r\n    \"fps\": 15,\r\n    \"width\": 640,\r\n    \"height\": 480,\r\n    \"brightness\": 0,\r\n    \"contrast\": 0\r\n  },\r\n  \"fatigue\": {\r\n    \"eye_closed_threshold\": 1.5,\r\n    \"ear_threshold\": 0.25,\r\n    \"frames_to_confirm\": 2\r\n  },\r\n  \"yawn\": {\r\n    \"mouth_threshold\": 0.7,\r\n    \"duration_threshold\": 2.5,\r\n    \"max_yawns_before_alert\": 3\r\n  },\r\n  \"behavior\": {\r\n    \"confidence_threshold\": 0.4,\r\n    \"phone_alert_threshold_1\": 3,\r\n    \"cigarette_continuous_threshold\": 7\r\n  },\r\n  \"system\": {\r\n    \"enable_gui\": false,\r\n    \"log_level\": \"INFO\",\r\n    \"auto_sync_interval\": 300\r\n  }\r\n}', 1, 1, '2025-06-05 02:01:59', NULL),
(2, 'Configuración Sensible', 'Mayor sensibilidad para detección temprana', 'Raspberry Pi', '{\r\n  \"camera\": {\r\n    \"fps\": 20,\r\n    \"width\": 640,\r\n    \"height\": 480,\r\n    \"brightness\": 10,\r\n    \"contrast\": 5\r\n  },\r\n  \"fatigue\": {\r\n    \"eye_closed_threshold\": 1.0,\r\n    \"ear_threshold\": 0.3,\r\n    \"frames_to_confirm\": 1\r\n  },\r\n  \"yawn\": {\r\n    \"mouth_threshold\": 0.6,\r\n    \"duration_threshold\": 2.0,\r\n    \"max_yawns_before_alert\": 2\r\n  },\r\n  \"behavior\": {\r\n    \"confidence_threshold\": 0.3,\r\n    \"phone_alert_threshold_1\": 2,\r\n    \"cigarette_continuous_threshold\": 5\r\n  },\r\n  \"system\": {\r\n    \"enable_gui\": false,\r\n    \"log_level\": \"DEBUG\",\r\n    \"auto_sync_interval\": 180\r\n  }\r\n}', 0, 1, '2025-06-05 02:01:59', NULL),
(3, 'Configuración Conservadora', 'Menor sensibilidad para evitar falsas alarmas', 'Raspberry Pi', '{\r\n  \"camera\": {\r\n    \"fps\": 10,\r\n    \"width\": 480,\r\n    \"height\": 360,\r\n    \"brightness\": 0,\r\n    \"contrast\": 0\r\n  },\r\n  \"fatigue\": {\r\n    \"eye_closed_threshold\": 2.0,\r\n    \"ear_threshold\": 0.2,\r\n    \"frames_to_confirm\": 3\r\n  },\r\n  \"yawn\": {\r\n    \"mouth_threshold\": 0.8,\r\n    \"duration_threshold\": 3.0,\r\n    \"max_yawns_before_alert\": 5\r\n  },\r\n  \"behavior\": {\r\n    \"confidence_threshold\": 0.5,\r\n    \"phone_alert_threshold_1\": 5,\r\n    \"cigarette_continuous_threshold\": 10\r\n  },\r\n  \"system\": {\r\n    \"enable_gui\": false,\r\n    \"log_level\": \"WARNING\",\r\n    \"auto_sync_interval\": 600\r\n  }\r\n}', 0, 1, '2025-06-05 02:01:59', NULL);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `device_config_status`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `device_config_status` (
`device_id` varchar(50)
,`device_name` varchar(100)
,`device_type` varchar(30)
,`device_status` enum('online','offline','syncing','error')
,`config_version` int(11)
,`config_pending` tinyint(1)
,`config_applied` datetime
,`last_config_check` datetime
,`last_access` datetime
,`config_status` varchar(16)
,`last_change_summary` text
,`last_changed_by` varchar(50)
,`last_change_date` datetime
);

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
(3, 'Máquinas', 'Gestión de maquinaria', '/pages/machines/index.php', 'fas fa-truck', NULL, 4, 'active'),
(4, 'Alertas', 'Sistema de alertas', '/pages/alerts/index.php', 'fas fa-bell', NULL, 5, 'active'),
(5, 'Estadísticas', 'Reportes estadísticos', '/pages/dashboard/index.php', 'fas fa-chart-bar', NULL, 6, 'active'),
(6, 'Reportes', 'Generación de reportes', '/pages/reports/daily.php', 'fas fa-file-alt', NULL, 7, 'active'),
(7, 'Usuarios', 'Administración de usuarios', '/pages/users/index.php', 'fas fa-user-shield', NULL, 8, 'active'),
(8, 'Configuración', 'Configuración del sistema', '/pages/settings.php', 'fas fa-cog', NULL, 9, 'active'),
(17, 'Dispositivos', 'Gestión de dispositivos', '/pages/devices/index.php', 'fas fa-microchip', NULL, 3, 'active');

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
(1834, 'info', NULL, '2025-06-05 08:52:23', 'Usuario admin ha iniciado sesión', 'IP: ::1');

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
(1, 'admin', '$2y$10$8mnOFRGdw.yHkQwHg3NRhuWN.mcGcDRZUiJqnK8MzwzEZlsXOuLOe', 'Administrador', 'admin', 'admin@example.com', '2025-06-05 08:52:23', 'active', '2025-05-01 13:36:16'),
(2, 'super', '$2y$10$gj9DJhbnzXkX.ur2vEKXE.6oAU0hcX95Rn66VZ7vvd.FocnRGOcGW', 'Nilson Cayao', 'supervisor', 'super@gmail.com', '2025-05-06 22:05:11', 'active', '2025-05-06 15:03:11');

-- --------------------------------------------------------

--
-- Estructura para la vista `device_config_status`
--
DROP TABLE IF EXISTS `device_config_status`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `device_config_status`  AS SELECT `d`.`device_id` AS `device_id`, `d`.`name` AS `device_name`, `d`.`device_type` AS `device_type`, `d`.`status` AS `device_status`, `d`.`config_version` AS `config_version`, `d`.`config_pending` AS `config_pending`, `d`.`config_applied` AS `config_applied`, `d`.`last_config_check` AS `last_config_check`, `d`.`last_access` AS `last_access`, CASE WHEN `d`.`status` = 'offline' THEN 'offline' WHEN `d`.`config_pending` = 1 THEN 'pending' WHEN `d`.`config_applied` is null THEN 'never_configured' WHEN `d`.`config_applied` < `d`.`last_access` - interval 5 minute THEN 'sync_error' ELSE 'synchronized' END AS `config_status`, `dch`.`changes_summary` AS `last_change_summary`, `u`.`username` AS `last_changed_by`, `dch`.`created_at` AS `last_change_date` FROM ((`devices` `d` left join `device_config_history` `dch` on(`d`.`device_id` = `dch`.`device_id` and `dch`.`id` = (select max(`device_config_history`.`id`) from `device_config_history` where `device_config_history`.`device_id` = `d`.`device_id`))) left join `users` `u` on(`dch`.`changed_by` = `u`.`id`)) ORDER BY `d`.`name` ASC ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alerts`
--
ALTER TABLE `alerts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `operator_id` (`operator_id`),
  ADD KEY `machine_id` (`machine_id`),
  ADD KEY `idx_alerts_device_id` (`device_id`);

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
  ADD KEY `machine_id` (`machine_id`),
  ADD KEY `idx_devices_config_pending` (`config_pending`),
  ADD KEY `idx_devices_last_config_check` (`last_config_check`);

--
-- Indices de la tabla `device_config_history`
--
ALTER TABLE `device_config_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`),
  ADD KEY `changed_by` (`changed_by`),
  ADD KEY `created_at` (`created_at`),
  ADD KEY `idx_config_history_device_date` (`device_id`,`created_at`);

--
-- Indices de la tabla `device_config_profiles`
--
ALTER TABLE `device_config_profiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_type` (`device_type`),
  ADD KEY `created_by` (`created_by`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

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
-- AUTO_INCREMENT de la tabla `device_config_history`
--
ALTER TABLE `device_config_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `device_config_profiles`
--
ALTER TABLE `device_config_profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `events`
--
ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `modules`
--
ALTER TABLE `modules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1835;

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
  ADD CONSTRAINT `alerts_ibfk_2` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`),
  ADD CONSTRAINT `fk_alerts_device_id` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`);

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
-- Filtros para la tabla `device_config_history`
--
ALTER TABLE `device_config_history`
  ADD CONSTRAINT `fk_config_history_device` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_config_history_user` FOREIGN KEY (`changed_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `device_config_profiles`
--
ALTER TABLE `device_config_profiles`
  ADD CONSTRAINT `fk_config_profiles_user` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `operators` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `events_ibfk_2` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_events_device_id` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`);

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
