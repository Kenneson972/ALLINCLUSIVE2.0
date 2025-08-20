CREATE TABLE IF NOT EXISTS villas (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(255),
  location VARCHAR(255),
  price DECIMAL(10,2),
  guests INT,
  guests_detail VARCHAR(255),
  features TEXT,
  category VARCHAR(64),
  image VARCHAR(512),
  description TEXT,
  status VARCHAR(32) DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS images (
  id VARCHAR(36) PRIMARY KEY,
  villa_id VARCHAR(36),
  src VARCHAR(512),
  alt VARCHAR(255),
  position INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX IDX_images_villa (villa_id)
);
CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  phone VARCHAR(32),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX IDX_users_email (email)
);
CREATE TABLE IF NOT EXISTS reservations (
  id VARCHAR(36) PRIMARY KEY,
  villa_id VARCHAR(36),
  user_id VARCHAR(36),
  checkin_date DATE,
  checkout_date DATE,
  guests_count INT,
  total_price DECIMAL(10,2),
  status VARCHAR(32),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX IDX_reservations_villa (villa_id),
  INDEX IDX_reservations_user (user_id)
);
CREATE TABLE IF NOT EXISTS settings (
  id VARCHAR(36) PRIMARY KEY,
  `key` VARCHAR(100) UNIQUE,
  `value` TEXT,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX IDX_settings_key (`key`)
);
