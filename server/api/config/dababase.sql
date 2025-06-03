-- Tabla para gestionar dispositivos (Raspberry Pi)
CREATE TABLE IF NOT EXISTS `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `api_key` varchar(255) NOT NULL,
  `device_type` varchar(30) NOT NULL,
  `machine_id` int(11) DEFAULT NULL,
  `status` enum('online','offline','syncing','error') DEFAULT 'offline',
  `last_sync` datetime DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`),
  KEY `machine_id` (`machine_id`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla para eventos sincronizados
CREATE TABLE IF NOT EXISTS `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(50) NOT NULL,
  `event_type` enum('fatigue','cellphone','smoking','unrecognized_operator','other') NOT NULL,
  `operator_id` int(11) DEFAULT NULL,
  `machine_id` int(11) DEFAULT NULL,
  `event_data` text,
  `image_path` varchar(255) DEFAULT NULL,
  `event_time` datetime NOT NULL,
  `server_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sync_batch_id` varchar(50) DEFAULT NULL,
  `is_synced` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `operator_id` (`operator_id`),
  KEY `machine_id` (`machine_id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `operators` (`id`) ON DELETE SET NULL,
  CONSTRAINT `events_ibfk_2` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla para control de sincronización por lotes
CREATE TABLE IF NOT EXISTS `sync_batches` (
  `id` varchar(50) NOT NULL,
  `device_id` varchar(50) NOT NULL,
  `batch_size` int(11) NOT NULL,
  `status` enum('processing','completed','failed') NOT NULL DEFAULT 'processing',
  `started_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `completed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;