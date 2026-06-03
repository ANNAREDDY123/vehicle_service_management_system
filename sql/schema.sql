CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE vehicles (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_number VARCHAR(50) UNIQUE,
    brand VARCHAR(100),
    model VARCHAR(100),
    customer_id INT,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE service_requests (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT,
    service_type VARCHAR(100),
    service_cost FLOAT,
    service_date DATE,
    status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);
