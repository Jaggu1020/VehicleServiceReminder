CREATE DATABASE vehicle_service_db;

USE vehicle_service_db;

CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(100) NOT NULL,
    registration_number VARCHAR(20) NOT NULL UNIQUE,
    vehicle_model VARCHAR(100) NOT NULL,
    current_km INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE service_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    last_service_date DATE NOT NULL,
    next_due_date DATE NOT NULL,
    next_due_km INT NOT NULL,
    notes VARCHAR(255),

    FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(id)
        ON DELETE CASCADE
);
