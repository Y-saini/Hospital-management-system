-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hospital_management_system;

-- Switch to the created database
USE hospital_management_system;

-- Create the appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    location VARCHAR(255),
    phone VARCHAR(15)
);
