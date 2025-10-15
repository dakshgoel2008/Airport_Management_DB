DROP DATABASE IF EXISTS `AIRPORT_MANAGEMENT_DB`;
CREATE DATABASE `AIRPORT_MANAGEMENT_DB`;
USE `AIRPORT_MANAGEMENT_DB`;

-- 
-- Table AIRPORT
-- 
CREATE TABLE `AIRPORT`(
    `airport_code` CHAR(3) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    `country` VARCHAR(50) NOT NULL,
    `timezone` VARCHAR(50) NOT NULL,
    `type` ENUM('International', 'Domestic', 'Regional', 'Private') NOT NULL,
    `elevation_ft` INT,
    `runway_count` INT DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`airport_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table AIRLINE
-- 
CREATE TABLE `AIRLINE`(
    `airline_id` VARCHAR(10) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `iata_code` CHAR(2),
    `icao_code` CHAR(3),
    `country` VARCHAR(50) NOT NULL,
    `founded_year` YEAR,
    `fleet_size` INT DEFAULT 0,
    `status` ENUM('Active', 'Inactive', 'Suspended') DEFAULT 'Active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`airline_id`),
    UNIQUE KEY `iata_code` (`iata_code`),
    UNIQUE KEY `icao_code` (`icao_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 
-- Table AIRCRAFT_TYPE
-- 
CREATE TABLE `AIRCRAFT_TYPE`(
    `aircraft_type_id` VARCHAR(20) NOT NULL,
    `manufacturer` VARCHAR(50) NOT NULL,
    `model` VARCHAR(50) NOT NULL,
    `capacity_economy` INT NOT NULL,
    `capacity_business` INT DEFAULT 0,
    `capacity_first` INT DEFAULT 0,
    `max_range_km` INT,
    `fuel_capacity_liters` INT,
    PRIMARY KEY (`aircraft_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 
-- Table AIRCRAFT
-- 
CREATE TABLE `AIRCRAFT`(
    `aircraft_id` VARCHAR(20) NOT NULL,
    `airline_id` VARCHAR(10) NOT NULL,
    `aircraft_type_id` VARCHAR(20) NOT NULL,
    `registration` VARCHAR(10) NOT NULL,
    `manufacture_date` DATE,
    `last_maintenance` DATE,
    `next_maintenance` DATE,
    `status` ENUM('Active', 'Maintenance', 'Grounded', 'Retired') DEFAULT 'Active',
    `total_flight_hours` DECIMAL(10,2) DEFAULT 0,
    PRIMARY KEY (`aircraft_id`),
    UNIQUE KEY `registration` (`registration`),
    FOREIGN KEY (`airline_id`) REFERENCES `AIRLINE`(`airline_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`aircraft_type_id`) REFERENCES `AIRCRAFT_TYPE`(`aircraft_type_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 
-- Table FLIGHT
-- 
CREATE TABLE `FLIGHT` (
    `flight_number` VARCHAR(10) NOT NULL,
    `airline_id` VARCHAR(10) NOT NULL,
    `airctraft_id` VARCHAR(20),
    `source_airport` CHAR(3) NOT NULL,
    `destination_airport` CHAR(3) NOT NULL,
    `scheduled_departure` DATETIME NOT NULL,
    `scheduled_arrival` DATETIME NOT NULL,
    `actual_departure` DATETIME,
    `actual_arrival` DATETIME,
    `status` ENUM('Scheduled', 'Delayed', 'Boarding', 'Departed', 'Arrived', 'Cancelled') DEFAULT 'Scheduled',
    `gate` VARCHAR(10),
    `terminal` VARCHAR(5),
    `delay_minutes` INT DEFAULT 0,
    `flight_date` DATE NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`flight_number`, `flight_date`),
    FOREIGN KEY (`airline_id`) REFERENCES `AIRLINE`(`airline_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`aircraft_id`) REFERENCES `AIRCRAFT`(`aircraft_id`) ON DELETE SET NULL,
    FOREIGN KEY (`source_airport`) REFERENCES `AIRPORT`(`airport_code`) ON DELETE RESTRICT,
    FOREIGN KEY (`destination_airport`) REFERENCES `AIRPORT`(`airport_code`) ON DELETE RESTRICT,
    INDEX `idx_departure_date` (`scheduled_departure`),
    INDEX `idx_arrival_date` (`scheduled_arrival`),
    INDEX `idx_source` (`source_airport`),
    INDEX `idx_destination` (`destination_airport`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table EMPLOYEE
--
CREATE TABLE `EMPLOYEE` (
    `employee_id` VARCHAR(20) NOT NULL,
    `airport_code` CHAR(3),
    `airline_id` VARCHAR(10),
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100),
    `phone` VARCHAR(20),
    `date_of_birth` DATE NOT NULL,
    `hire_date` DATE NOT NULL,
    `department` VARCHAR(50) NOT NULL,
    `position` VARCHAR(50) NOT NULL,
    `salary` DECIMAL(10,2),
    `status` ENUM('Active', 'Inactive', 'Terminated', 'Retired') DEFAULT 'Active',
    `supervisor_id` VARCHAR(20),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`employee_id`),
    UNIQUE KEY `email` (`email`),
    FOREIGN KEY (`airport_code`) REFERENCES `AIRPORT`(`airport_code`) ON DELETE SET NULL,
    FOREIGN KEY (`airline_id`) REFERENCES `AIRLINE`(`airline_id`) ON DELETE SET NULL,
    FOREIGN KEY (`supervisor_id`) REFERENCES `EMPLOYEE`(`employee_id`) ON DELETE SET NULL,
    INDEX `idx_department` (`department`),
    INDEX `idx_position` (`position`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table CREW_MEMBER
--
CREATE TABLE `CREW_MEMBER` (
    `crew_id` VARCHAR(20) NOT NULL,
    `employee_id` VARCHAR(20) NOT NULL,
    `crew_type` ENUM('Pilot', 'Co-Pilot', 'Flight_Engineer', 'Flight_Attendant', 'Purser') NOT NULL,
    `license_number` VARCHAR(50),
    `license_expiry` DATE,
    `medical_certificate_expiry` DATE,
    `flight_hours` DECIMAL(10,2) DEFAULT 0,
    `qualification_date` DATE,
    `status` ENUM('Active', 'Training', 'Medical_Leave', 'Suspended') DEFAULT 'Active',
    PRIMARY KEY (`crew_id`),
    UNIQUE KEY `employee_id` (`employee_id`),
    FOREIGN KEY (`employee_id`) REFERENCES `EMPLOYEE`(`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table FLIGHT_CREW 
--
CREATE TABLE `FLIGHT_CREW` (
    `flight_number` VARCHAR(10) NOT NULL,
    `flight_date` DATE NOT NULL,
    `crew_id` VARCHAR(20) NOT NULL,
    `role` ENUM('Captain', 'First_Officer', 'Flight_Engineer', 'Chief_Purser', 'Flight_Attendant') NOT NULL,
    `check_in_time` DATETIME,
    `check_out_time` DATETIME,
    PRIMARY KEY (`flight_number`, `flight_date`, `crew_id`),
    FOREIGN KEY (`flight_number`, `flight_date`) REFERENCES `FLIGHT`(`flight_number`, `flight_date`) ON DELETE CASCADE,
    FOREIGN KEY (`crew_id`) REFERENCES `CREW_MEMBER`(`crew_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 
-- Table PASSENGER
-- 
CREATE TABLE `PASSENGER`(
    `passenger_id` VARCHAR(20) NOT NULL,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `gender` ENUM('M', 'F', 'Other') NOT NULL,
    `nationality` VARCHAR(50) NOT NULL,
    `passport_number` VARCHAR(20) NOT NULL,
    `passport_expiry` DATE NOT NULL,
    `email` VARCHAR(100),
    `phone` VARCHAR(20),
    `frequent_flyer_number` VARCHAR(30),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`passenger_id`),
    UNIQUE KEY `passport_number` (`passport_number`),
    UNIQUE KEY `email` (`email`),
    INDEX `idx_name` (`last_name`, `first_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table PASSENGER_ADDRESS
--
CREATE TABLE `PASSENGER_ADDRESS`(
    `passenger_id` VARCHAR(20) NOT NULL,
    `address_type` ENUM('Home', 'Work', 'Emergency') NOT NULL,
    `street_address` VARCHAR(200) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    `state_province` VARCHAR(50),
    `postal_code` VARCHAR(20),
    `country` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`passenger_id`, `address_type`),
    FOREIGN KEY (`passenger_id`) REFERENCES `PASSENGER`(`passenger_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table BOOKING
--
CREATE TABLE `BOOKING`(
    `booking_id` VARCHAR(20) NOT NULL,
    `passenger_id` VARCHAR(20) NOT NULL,
    `booking_date` DATETIME NOT NULL,
    `total_amount` DECIMAL(10,2) NOT NULL,
    `currency` CHAR(3) DEFAULT 'USD',
    `payment_status` ENUM('Pending', 'Paid', 'Cancelled', 'Refunded') DEFAULT 'Pending',
    `booking_status` ENUM('Confirmed', 'Cancelled', 'Modified') DEFAULT 'Confirmed',
    `booking_reference` VARCHAR(10) NOT NULL,
    `travel_agent_id` VARCHAR(20),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`booking_id`),
    UNIQUE KEY `booking_reference` (`booking_reference`),
    FOREIGN KEY (`passenger_id`) REFERENCES `PASSENGER`(`passenger_id`) ON DELETE RESTRICT,
    INDEX `idx_booking_date` (`booking_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table TICKET
--
CREATE TABLE `TICKET`(
    `ticket_id` VARCHAR(20) NOT NULL,
    `booking_id` VARCHAR(20) NOT NULL,
    `flight_number` VARCHAR(10) NOT NULL,
    `flight_date` DATE NOT NULL,
    `passenger_id` VARCHAR(20) NOT NULL,
    `seat_number` VARCHAR(5),
    `class` ENUM('Economy', 'Premium_Economy', 'Business', 'First') NOT NULL,
    `fare_amount` DECIMAL(10,2) NOT NULL,
    `ticket_status` ENUM('Active', 'Used', 'Cancelled', 'No_Show') DEFAULT 'Active',
    `check_in_status` ENUM('Not_Checked_In', 'Checked_In', 'Boarded') DEFAULT 'Not_Checked_In',
    `check_in_time` DATETIME,
    `boarding_time` DATETIME,
    `baggage_allowance_kg` INT DEFAULT 20,
    `special_requests` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`ticket_id`),
    UNIQUE KEY `flight_seat` (`flight_number`, `flight_date`, `seat_number`),
    FOREIGN KEY (`booking_id`) REFERENCES `BOOKING`(`booking_id`) ON DELETE CASCADE,
    FOREIGN KEY (`flight_number`, `flight_date`) REFERENCES `FLIGHT`(`flight_number`, `flight_date`) ON DELETE RESTRICT,
    FOREIGN KEY (`passenger_id`) REFERENCES `PASSENGER`(`passenger_id`) ON DELETE RESTRICT,
    INDEX `idx_flight_date` (`flight_date`),
    INDEX `idx_passenger` (`passenger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table BAGGAGE
--
CREATE TABLE `BAGGAGE`(
    `baggage_id` VARCHAR(20) NOT NULL,
    `ticket_id` VARCHAR(20) NOT NULL,
    `baggage_type` ENUM('Carry_On', 'Checked', 'Oversized', 'Special') NOT NULL,
    `weight_kg` DECIMAL(5,2) NOT NULL,
    `status` ENUM('Checked_In', 'Loaded', 'In_Transit', 'Delivered', 'Lost', 'Delayed') DEFAULT 'Checked_In',
    `special_handling` VARCHAR(100),
    `current_location` VARCHAR(100),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`baggage_id`),
    FOREIGN KEY (`ticket_id`) REFERENCES `TICKET`(`ticket_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 
-- Table ATC (Air Traffic Control)
-- 
CREATE TABLE `ATC`(
    `atc_id` VARCHAR(20) NOT NULL,
    `airport_code` CHAR(3) NOT NULL,
    `shift_start` TIME NOT NULL,
    `shift_end` TIME NOT NULL,
    `controller_count` INT NOT NULL DEFAULT 1,
    `frequency` DECIMAL(6,3),
    `sector` VARCHAR(50),
    `status` ENUM('Active', 'Inactive', 'Maintenance') DEFAULT 'Active',
    PRIMARY KEY (`atc_id`),
    FOREIGN KEY (`airport_code`) REFERENCES `AIRPORT`(`airport_code`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table GATE
--
CREATE TABLE `GATE`(
    `gate_id` VARCHAR(10) NOT NULL,
    `airport_code` CHAR(3) NOT NULL,
    `terminal` VARCHAR(5) NOT NULL,
    `gate_type` ENUM('Domestic', 'International', 'Regional') NOT NULL,
    `status` ENUM('Available', 'Occupied', 'Maintenance', 'Closed') DEFAULT 'Available',
    `aircraft_capacity` ENUM('Small', 'Medium', 'Large', 'Wide_Body') NOT NULL,
    PRIMARY KEY (`gate_id`, `airport_code`),
    FOREIGN KEY (`airport_code`) REFERENCES `AIRPORT`(`airport_code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table FLIGHT_STATUS_LOG 
--
CREATE TABLE `FLIGHT_STATUS_LOG`(
    `log_id` INT AUTO_INCREMENT,
    `flight_number` VARCHAR(10) NOT NULL,
    `flight_date` DATE NOT NULL,
    `old_status` VARCHAR(20),
    `new_status` VARCHAR(20) NOT NULL,
    `reason` VARCHAR(200),
    `changed_by` VARCHAR(20),
    `changed_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`log_id`),
    FOREIGN KEY (`flight_number`, `flight_date`) REFERENCES `FLIGHT`(`flight_number`, `flight_date`) ON DELETE CASCADE,
    INDEX `idx_flight_date_log` (`flight_number`, `flight_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;