-- Sample dataset -> Will be updated according to the user

-- AIRPORT
INSERT INTO `AIRPORT` (`airport_code`, `name`, `city`, `country`, `timezone`, `type`, `elevation_ft`, `runway_count`) VALUES
('JFK', 'John F. Kennedy International Airport', 'New York', 'United States', 'America/New_York', 'International', 13, 4),
('LAX', 'Los Angeles International Airport', 'Los Angeles', 'United States', 'America/Los_Angeles', 'International', 125, 4),
('LHR', 'London Heathrow Airport', 'London', 'United Kingdom', 'Europe/London', 'International', 83, 2),
('DXB', 'Dubai International Airport', 'Dubai', 'United Arab Emirates', 'Asia/Dubai', 'International', 62, 2),
('NRT', 'Narita International Airport', 'Tokyo', 'Japan', 'Asia/Tokyo', 'International', 141, 2),
('SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore', 'Asia/Singapore', 'International', 22, 3),
('CDG', 'Charles de Gaulle Airport', 'Paris', 'France', 'Europe/Paris', 'International', 392, 4),
('ORD', 'O''Hare International Airport', 'Chicago', 'United States', 'America/Chicago', 'International', 672, 7),
('ATL', 'Hartsfield-Jackson Atlanta International Airport', 'Atlanta', 'United States', 'America/New_York', 'International', 1026, 5),
('FRA', 'Frankfurt Airport', 'Frankfurt', 'Germany', 'Europe/Berlin', 'International', 364, 4);

-- AIRLINE
INSERT INTO `AIRLINE` (`airline_id`, `name`, `iata_code`, `icao_code`, `country`, `founded_year`, `fleet_size`, `status`) VALUES
('AA001', 'American Airlines', 'AA', 'AAL', 'United States', 1930, 956, 'Active'),
('DL001', 'Delta Air Lines', 'DL', 'DAL', 'United States', 1924, 865, 'Active'),
('UA001', 'United Airlines', 'UA', 'UAL', 'United States', 1926, 843, 'Active'),
('BA001', 'British Airways', 'BA', 'BAW', 'United Kingdom', 1974, 273, 'Active'),
('EK001', 'Emirates', 'EK', 'UAE', 'United Arab Emirates', 1985, 269, 'Active'),
('LH001', 'Lufthansa', 'LH', 'DLH', 'Germany', 1953, 279, 'Active'),
('SQ001', 'Singapore Airlines', 'SQ', 'SIA', 'Singapore', 1947, 138, 'Active'),
('QR001', 'Qatar Airways', 'QR', 'QTR', 'Qatar', 1997, 245, 'Active');

-- AIRCRAFT_TYPE
INSERT INTO `AIRCRAFT_TYPE` (`aircraft_type_id`, `manufacturer`, `model`, `capacity_economy`, `capacity_business`, `capacity_first`, `max_range_km`, `fuel_capacity_liters`) VALUES
('B737-800', 'Boeing', '737-800', 162, 16, 0, 5425, 26020),
('B777-300ER', 'Boeing', '777-300ER', 396, 42, 8, 14490, 181280),
('A320', 'Airbus', 'A320', 150, 24, 0, 6150, 24210),
('A380-800', 'Airbus', 'A380-800', 525, 76, 14, 15200, 323546),
('B787-9', 'Boeing', '787-9', 290, 28, 0, 14140, 126206),
('A350-900', 'Airbus', 'A350-900', 315, 42, 0, 15000, 138000),
('B757-200', 'Boeing', '757-200', 200, 16, 0, 7222, 43490),
('A330-300', 'Airbus', 'A330-300', 295, 36, 0, 11750, 139090);

-- AIRCRAFT 
INSERT INTO `AIRCRAFT` (`aircraft_id`, `airline_id`, `aircraft_type_id`, `registration`, `manufacture_date`, `last_maintenance`, `next_maintenance`, `status`, `total_flight_hours`) VALUES
('AA001-001', 'AA001', 'B737-800', 'N801AA', '2018-03-15', '2024-12-01', '2025-03-01', 'Active', 12450.50),
('AA001-002', 'AA001', 'B777-300ER', 'N802AA', '2019-07-22', '2024-11-15', '2025-02-15', 'Active', 8750.25),
('DL001-001', 'DL001', 'A320', 'N301DL', '2020-01-10', '2024-12-10', '2025-03-10', 'Active', 6890.75),
('DL001-002', 'DL001', 'B757-200', 'N302DL', '2017-11-05', '2024-12-15', '2025-03-15', 'Active', 15620.00),
('BA001-001', 'BA001', 'A380-800', 'G-XLAA', '2016-09-18', '2024-11-25', '2025-02-25', 'Active', 18950.30),
('EK001-001', 'EK001', 'B777-300ER', 'A6-EGO', '2019-04-12', '2024-12-05', '2025-03-05', 'Active', 9820.45),
('LH001-001', 'LH001', 'A350-900', 'D-AIXM', '2021-02-28', '2024-11-30', '2025-02-28', 'Active', 4560.15),
('SQ001-001', 'SQ001', 'A330-300', '9V-STC', '2018-08-14', '2024-12-08', '2025-03-08', 'Active', 11280.90),
('UA001-001', 'UA001', 'B787-9', 'N26952', '2020-06-15', '2024-11-28', '2025-02-28', 'Active', 7240.75),
('QR001-001', 'QR001', 'A350-900', 'A7-ALF', '2021-09-10', '2024-12-12', '2025-03-12', 'Active', 5180.50),
('BA001-002', 'BA001', 'B777-300ER', 'G-STBF', '2018-01-25', '2024-10-15', '2025-01-15', 'Active', 13670.25),
('EK001-002', 'EK001', 'A380-800', 'A6-EUZ', '2017-05-18', '2024-11-20', '2025-02-20', 'Maintenance', 17250.75);

-- GATE 
INSERT INTO `GATE` (`gate_id`, `airport_code`, `terminal`, `gate_type`, `status`, `aircraft_capacity`) VALUES
('A12', 'JFK', '4', 'Domestic', 'Available', 'Medium'),
('B8', 'LAX', '6', 'Domestic', 'Available', 'Large'),
('C15', 'ATL', '1', 'International', 'Occupied', 'Medium'),
('D22', 'LHR', '5', 'International', 'Occupied', 'Wide_Body'),
('E8', 'DXB', '3', 'International', 'Occupied', 'Wide_Body'),
('F5', 'FRA', '2', 'International', 'Available', 'Large'),
('G10', 'SIN', '2', 'International', 'Available', 'Medium'),
('H7', 'ORD', '3', 'Domestic', 'Available', 'Medium'),
('A1', 'JFK', '1', 'International', 'Maintenance', 'Wide_Body'),
('B15', 'LAX', '4', 'International', 'Available', 'Large'),
('K12', 'ORD', '5', 'International', 'Available', 'Large'),
('L18', 'DXB', '1', 'International', 'Available', 'Large'),
('M5', 'LHR', '3', 'International', 'Available', 'Wide_Body'),
('N9', 'DXB', '2', 'International', 'Available', 'Wide_Body'),
('P7', 'FRA', '1', 'International', 'Available', 'Large'),
('Q14', 'SIN', '3', 'International', 'Available', 'Medium'),
('R11', 'JFK', '1', 'International', 'Maintenance', 'Wide_Body'),
('S8', 'LAX', '7', 'Domestic', 'Available', 'Medium'),
('T3', 'ATL', '2', 'International', 'Available', 'Large'),
('U16', 'CDG', '2E', 'International', 'Available', 'Wide_Body');

-- TRAVEL_AGENT 
INSERT INTO `TRAVEL_AGENT` (`travel_agent_id`, `name`, `email`, `phone`) VALUES
('TA001', 'Global Travel Services', 'contact@globaltravel.com', '+1-555-3001'),
('TA002', 'EuroTravel', 'info@eurotravel.com', '+39-06-700-2002');

-- EMPLOYEE 
INSERT INTO `EMPLOYEE` (`employee_id`, `airport_code`, `airline_id`, `first_name`, `last_name`, `email`, `phone`, `date_of_birth`, `hire_date`, `department`, `position`, `salary`, `status`, `supervisor_id`) VALUES
('EMP001', 'JFK', NULL, 'John', 'Smith', 'john.smith@jfkairport.com', '+1-555-0101', '1985-03-15', '2015-06-01', 'Operations', 'Airport Manager', 95000.00, 'Active', NULL),
('EMP002', 'JFK', NULL, 'Sarah', 'Johnson', 'sarah.johnson@jfkairport.com', '+1-555-0102', '1988-07-22', '2018-03-15', 'Security', 'Security Supervisor', 65000.00, 'Active', 'EMP001'),
('EMP003', NULL, 'AA001', 'Michael', 'Brown', 'michael.brown@aa.com', '+1-555-0103', '1982-11-08', '2012-09-10', 'Flight Operations', 'Chief Pilot', 125000.00, 'Active', NULL),
('EMP004', NULL, 'AA001', 'Emily', 'Davis', 'emily.davis@aa.com', '+1-555-0104', '1990-04-18', '2019-02-28', 'Cabin Crew', 'Senior Flight Attendant', 58000.00, 'Active', 'EMP003'),
('EMP005', 'LAX', NULL, 'Robert', 'Wilson', 'robert.wilson@laxairport.com', '+1-555-0105', '1987-09-12', '2017-01-20', 'Ground Operations', 'Ground Crew Supervisor', 62000.00, 'Active', NULL),
('EMP006', NULL, 'DL001', 'Lisa', 'Anderson', 'lisa.anderson@delta.com', '+1-555-0106', '1989-12-03', '2020-05-15', 'Flight Operations', 'First Officer', 85000.00, 'Active', NULL),
('EMP007', 'LHR', NULL, 'James', 'Taylor', 'james.taylor@heathrow.com', '+44-20-7946-0107', '1984-06-25', '2016-08-12', 'Air Traffic Control', 'Air Traffic Controller', 72000.00, 'Active', NULL),
('EMP008', NULL, 'BA001', 'Emma', 'Martinez', 'emma.martinez@ba.com', '+44-20-7946-0108', '1991-01-14', '2021-03-08', 'Cabin Crew', 'Flight Attendant', 45000.00, 'Active', NULL),
('EMP009', 'DXB', NULL, 'Hassan', 'Abdullah', 'hassan.abdullah@dubaiairport.ae', '+971-4-2160109', '1986-05-30', '2019-04-12', 'Customer Service', 'Customer Service Manager', 68000.00, 'Active', NULL),
('EMP010', NULL, 'EK001', 'Fatima', 'Al-Zahra', 'fatima.alzahra@emirates.com', '+971-4-2160110', '1991-09-14', '2022-01-20', 'Cabin Crew', 'Flight Attendant', 52000.00, 'Active', NULL),
('EMP011', 'SIN', NULL, 'Wei', 'Lim', 'wei.lim@changiairport.com', '+65-6542-0111', '1983-12-05', '2018-07-25', 'Ground Operations', 'Ramp Supervisor', 58000.00, 'Active', NULL),
('EMP012', 'FRA', NULL, 'Klaus', 'Schmidt', 'klaus.schmidt@fraport.de', '+49-69-690-0112', '1979-03-18', '2014-11-08', 'Maintenance', 'Aircraft Technician', 72000.00, 'Active', NULL),
('EMP013', NULL, 'LH001', 'Andreas', 'Weber', 'andreas.weber@lufthansa.com', '+49-69-696-0113', '1985-07-22', '2017-02-15', 'Flight Operations', 'Captain', 135000.00, 'Active', NULL),
('EMP014', 'CDG', NULL, 'Marie', 'Leclerc', 'marie.leclerc@adp.fr', '+33-1-48-62-0114', '1990-10-08', '2021-06-12', 'Security', 'Security Officer', 45000.00, 'Active', NULL),
('EMP015', NULL, 'AA001', 'Christopher', 'Lee', 'christopher.lee@aa.com', '+1-555-0115', '1987-06-14', '2016-08-22', 'Flight Operations', 'Captain', 128000.00, 'Active', NULL),
('EMP016', NULL, 'DL001', 'Patricia', 'White', 'patricia.white@delta.com', '+1-555-0116', '1992-02-09', '2021-04-15', 'Cabin Crew', 'Flight Attendant', 46000.00, 'Active', NULL),
('EMP017', NULL, NULL, 'Jennifer', 'Chang', 'jennifer.chang@globaltravel.com', '+1-555-2001', '1988-04-12', '2020-03-15', 'Sales', 'Travel Agent', 48000.00, 'Active', NULL),
('EMP018', NULL, NULL, 'Marco', 'Rossi', 'marco.rossi@eurotravel.com', '+39-06-1234567', '1985-11-28', '2018-08-20', 'Sales', 'Senior Travel Agent', 55000.00, 'Active', NULL);


-- CREW_MEMBER
INSERT INTO `CREW_MEMBER` (`crew_id`, `employee_id`, `crew_type`, `license_number`, `license_expiry`, `medical_certificate_expiry`, `flight_hours`, `qualification_date`, `status`) VALUES
('CREW001', 'EMP003', 'Pilot', 'ATP-12345678', '2026-03-15', '2025-09-10', 8500.75, '2012-11-15', 'Active'),
('CREW002', 'EMP006', 'Co-Pilot', 'CPL-87654321', '2025-12-20', '2025-06-15', 3250.50, '2020-07-01', 'Active'),
('CREW003', 'EMP004', 'Flight_Attendant', 'FA-11223344', '2025-08-30', '2025-04-20', 2100.25, '2019-04-01', 'Active'),
('CREW004', 'EMP008', 'Flight_Attendant', 'FA-55667788', '2026-01-25', '2025-07-10', 850.00, '2021-05-15', 'Active'),
('CREW005', 'EMP015', 'Pilot', 'ATP-99887766', '2025-11-10', '2025-05-25', 12500.00, '2010-03-20', 'Active'),
('CREW006', 'EMP016', 'Flight_Attendant', 'FA-44332211', '2026-02-14', '2025-08-05', 1750.30, '2021-06-10', 'Active'),
('CREW007', 'EMP010', 'Flight_Attendant', 'FA-99887744', '2025-12-30', '2025-06-30', 1250.75, '2022-03-15', 'Active'),
('CREW008', 'EMP013', 'Pilot', 'ATP-55443322', '2026-07-22', '2025-01-22', 15750.50, '2008-09-10', 'Active');

-- PASSENGER 
INSERT INTO `PASSENGER` (`passenger_id`, `first_name`, `last_name`, `date_of_birth`, `gender`, `nationality`, `passport_number`, `passport_expiry`, `email`, `phone`, `frequent_flyer_number`) VALUES
('PAX001', 'David', 'Thompson', '1975-05-12', 'M', 'United States', 'US123456789', '2027-05-12', 'david.thompson@email.com', '+1-555-1001', 'AA12345678'),
('PAX002', 'Maria', 'Garcia', '1983-09-18', 'F', 'Spain', 'ES987654321', '2026-09-18', 'maria.garcia@email.com', '+34-666-1002', 'DL87654321'),
('PAX003', 'William', 'Chen', '1990-02-28', 'M', 'Canada', 'CA456789123', '2028-02-28', 'william.chen@email.com', '+1-416-1003', 'BA11223344'),
('PAX004', 'Sophie', 'Dubois', '1987-11-14', 'F', 'France', 'FR789123456', '2025-11-14', 'sophie.dubois@email.com', '+33-1-1004', 'EK55667788'),
('PAX005', 'Rajesh', 'Patel', '1978-07-03', 'M', 'India', 'IN321654987', '2026-07-03', 'rajesh.patel@email.com', '+91-98765-1005', 'LH99887766'),
('PAX006', 'Anna', 'Mueller', '1985-12-20', 'F', 'Germany', 'DE654987321', '2027-12-20', 'anna.mueller@email.com', '+49-30-1006', 'SQ44332211'),
('PAX007', 'James', 'Wilson', '1992-04-09', 'M', 'United Kingdom', 'GB147258369', '2029-04-09', 'james.wilson@email.com', '+44-20-1007', 'QR77889900'),
('PAX008', 'Yuki', 'Tanaka', '1980-08-25', 'F', 'Japan', 'JP963852741', '2025-08-25', 'yuki.tanaka@email.com', '+81-3-1008', 'AA22334455'),
('PAX009', 'Ahmed', 'Al-Rashid', '1975-10-15', 'M', 'United Arab Emirates', 'AE789456123', '2026-10-15', 'ahmed.alrashid@email.com', '+971-50-1009', 'EK88776655'),
('PAX010', 'Linda', 'Johnson', '1988-03-22', 'F', 'United States', 'US456123789', '2027-03-22', 'linda.johnson@email.com', '+1-555-1010', 'DL33445566'),
('PAX011', 'Carlos', 'Rodriguez', '1982-08-07', 'M', 'Mexico', 'MX159753486', '2025-08-07', 'carlos.rodriguez@email.com', '+52-55-1011', 'AA66778899'),
('PAX012', 'Priya', 'Sharma', '1993-01-11', 'F', 'India', 'IN852741963', '2028-01-11', 'priya.sharma@email.com', '+91-98765-1012', 'QR12345678');

-- PASSENGER_ADDRESS
INSERT INTO `PASSENGER_ADDRESS` (`passenger_id`, `address_type`, `street_address`, `city`, `state_province`, `postal_code`, `country`) VALUES
('PAX001', 'Home', '123 Main Street', 'New York', 'NY', '10001', 'United States'),
('PAX002', 'Home', 'Calle Gran Via 45', 'Madrid', 'Madrid', '28013', 'Spain'),
('PAX003', 'Home', '456 Maple Avenue', 'Toronto', 'ON', 'M5V 3A8', 'Canada'),
('PAX004', 'Home', '78 Rue de Rivoli', 'Paris', 'Ile-de-France', '75001', 'France'),
('PAX005', 'Home', 'MG Road 234', 'Mumbai', 'Maharashtra', '400001', 'India'),
('PAX006', 'Home', 'Unter den Linden 12', 'Berlin', 'Berlin', '10117', 'Germany'),
('PAX007', 'Home', '89 Oxford Street', 'London', 'England', 'W1C 1DX', 'United Kingdom'),
('PAX008', 'Home', 'Shibuya 2-1-1', 'Tokyo', 'Tokyo', '150-0002', 'Japan'),
('PAX009', 'Home', 'Sheikh Zayed Road 567', 'Dubai', 'Dubai', '00000', 'United Arab Emirates'),
('PAX010', 'Home', '890 Oak Street', 'Los Angeles', 'CA', '90210', 'United States'),
('PAX011', 'Home', 'Avenida Reforma 123', 'Mexico City', 'CDMX', '06600', 'Mexico'),
('PAX012', 'Home', 'Connaught Place 45', 'New Delhi', 'Delhi', '110001', 'India');

-- BOOKING 
INSERT INTO `BOOKING` (`booking_id`, `passenger_id`, `booking_date`, `total_amount`, `currency`, `payment_status`, `booking_status`, `booking_reference`, `travel_agent_id`) VALUES
('BK001', 'PAX001', '2024-11-15 14:30:00', 485.99, 'USD', 'Paid', 'Confirmed', 'AA1B2C3D', NULL),
('BK002', 'PAX002', '2024-11-18 09:45:00', 1250.00, 'EUR', 'Paid', 'Confirmed', 'DL4E5F6G', 'TA001'),
('BK003', 'PAX003', '2024-12-01 16:20:00', 890.50, 'GBP', 'Paid', 'Confirmed', 'BA7H8I9J', NULL),
('BK004', 'PAX004', '2024-12-05 11:15:00', 1560.75, 'USD', 'Paid', 'Confirmed', 'EK0K1L2M', NULL),
('BK005', 'PAX005', '2024-12-10 08:30:00', 2100.00, 'EUR', 'Paid', 'Confirmed', 'LH3N4O5P', 'TA002'),
('BK006', 'PAX006', '2024-12-12 13:45:00', 975.25, 'SGD', 'Paid', 'Confirmed', 'SQ6Q7R8S', NULL),
('BK007', 'PAX007', '2024-12-14 10:00:00', 425.00, 'USD', 'Pending', 'Confirmed', 'AA9T0U1V', NULL),
('BK008', 'PAX008', '2024-12-16 15:30:00', 680.80, 'JPY', 'Paid', 'Confirmed', 'LH2W3X4Y', NULL),
('BK009', 'PAX009', '2024-12-18 12:15:00', 1890.00, 'AED', 'Paid', 'Confirmed', 'EK5Z6A7B', NULL),
('BK010', 'PAX010', '2024-12-19 14:20:00', 650.75, 'USD', 'Paid', 'Confirmed', 'DL8C9D0E', NULL),
('BK011', 'PAX011', '2024-12-17 09:30:00', 520.50, 'USD', 'Paid', 'Confirmed', 'AA1F2G3H', NULL),
('BK012', 'PAX012', '2024-12-20 16:45:00', 1250.00, 'USD', 'Paid', 'Confirmed', 'LH4I5J6K', NULL);

-- FLIGHT 
INSERT INTO `FLIGHT` (`flight_number`, `airline_id`, `aircraft_id`, `source_airport`, `destination_airport`, `scheduled_departure`, `scheduled_arrival`, `actual_departure`, `actual_arrival`, `status`, `gate_id`, `terminal`, `delay_minutes`, `flight_date`) VALUES
('BA400', 'BA001', 'BA001-002', 'LHR', 'JFK', '2025-10-27 20:15:00', '2025-10-27 23:45:00', NULL, NULL, 'Scheduled', 'M5', '3', 0, '2025-10-27'),
('AA100', 'AA001', 'AA001-001', 'JFK', 'LAX', '2024-12-20 08:00:00', '2024-12-20 11:30:00', '2024-12-20 08:15:00', '2024-12-20 11:45:00', 'Arrived', 'A12', '4', 15, '2024-12-20'),
('AA101', 'AA001', 'AA001-002', 'LAX', 'JFK', '2024-12-20 14:00:00', '2024-12-20 22:30:00', '2024-12-20 14:00:00', '2024-12-20 22:25:00', 'Arrived', 'B8', '6', 0, '2024-12-20'),
('DL200', 'DL001', 'DL001-001', 'ATL', 'LHR', '2024-12-21 18:45:00', '2024-12-22 07:15:00', NULL, NULL, 'Scheduled', 'C15', '1', 0, '2024-12-21'),
('BA300', 'BA001', 'BA001-001', 'LHR', 'DXB', '2024-12-21 10:30:00', '2024-12-21 20:45:00', NULL, NULL, 'Delayed', 'D22', '5', 45, '2024-12-21'),
('EK400', 'EK001', 'EK001-001', 'DXB', 'SIN', '2024-12-21 23:50:00', '2024-12-22 11:25:00', NULL, NULL, 'Boarding', 'E8', '3', 0, '2024-12-21'),
('LH500', 'LH001', 'LH001-001', 'FRA', 'NRT', '2024-12-22 11:15:00', '2024-12-23 06:30:00', NULL, NULL, 'Scheduled', 'F5', '2', 0, '2024-12-22'),
('SQ600', 'SQ001', 'SQ001-001', 'SIN', 'CDG', '2024-12-22 01:20:00', '2024-12-22 08:45:00', NULL, NULL, 'Departed', 'G10', '2', 0, '2024-12-22'),
('AA102', 'AA001', 'AA001-001', 'ORD', 'LAX', '2024-12-22 16:30:00', '2024-12-22 18:45:00', NULL, NULL, 'Scheduled', 'H7', '3', 0, '2024-12-22'),
('AA150', 'AA001', NULL, 'JFK', 'ORD', '2024-12-21 15:30:00', '2024-12-21 17:45:00', NULL, NULL, 'Cancelled', NULL, '4', 0, '2024-12-21'),
('DL250', 'DL001', 'DL001-001', 'LAX', 'ATL', '2024-12-22 09:15:00', '2024-12-22 16:30:00', NULL, NULL, 'Delayed', 'S8', '2', 120, '2024-12-22'),
('UA200', 'UA001', 'UA001-001', 'ORD', 'NRT', '2024-12-23 13:45:00', '2024-12-24 17:30:00', NULL, NULL, 'Scheduled', 'K12', '5', 0, '2024-12-23'),
('QR300', 'QR001', 'QR001-001', 'DXB', 'CDG', '2024-12-23 08:25:00', '2024-12-23 13:10:00', NULL, NULL, 'Scheduled', 'L18', '1', 0, '2024-12-23'),
('BA400', 'BA001', 'BA001-002', 'LHR', 'JFK', '2024-12-23 20:15:00', '2024-12-23 23:45:00', NULL, NULL, 'Scheduled', 'M5', '3', 0, '2024-12-23'),
('EK500', 'EK001', 'EK001-001', 'DXB', 'LAX', '2024-12-24 02:30:00', '2024-12-24 06:55:00', NULL, NULL, 'Scheduled', 'N9', '2', 0, '2024-12-24'),
('LH600', 'LH001', 'LH001-001', 'FRA', 'SIN', '2024-12-24 22:40:00', '2024-12-25 16:15:00', NULL, NULL, 'Scheduled', 'P7', '1', 0, '2024-12-24'),
('SQ700', 'SQ001', 'SQ001-001', 'SIN', 'LHR', '2024-12-25 11:30:00', '2024-12-25 17:25:00', NULL, NULL, 'Scheduled', 'Q14', '3', 0, '2024-12-25');

-- FLIGHT_CREW 
INSERT INTO `FLIGHT_CREW` (`flight_number`, `flight_date`, `crew_id`, `role`, `check_in_time`, `check_out_time`) VALUES
('AA100', '2024-12-20', 'CREW001', 'Captain', '2024-12-20 06:30:00', '2024-12-20 13:00:00'),
('AA100', '2024-12-20', 'CREW002', 'First_Officer', '2024-12-20 06:30:00', '2024-12-20 13:00:00'),
('AA100', '2024-12-20', 'CREW003', 'Flight_Attendant', '2024-12-20 06:45:00', '2024-12-20 12:45:00'),
('AA101', '2024-12-20', 'CREW005', 'Captain', '2024-12-20 12:30:00', '2024-12-21 00:30:00'),
('AA101', '2024-12-20', 'CREW006', 'Flight_Attendant', '2024-12-20 12:30:00', '2024-12-21 00:30:00'),
('DL200', '2024-12-21', 'CREW001', 'Captain', '2024-12-21 16:45:00', NULL),
('BA300', '2024-12-21', 'CREW004', 'Flight_Attendant', '2024-12-21 08:30:00', NULL),
('EK400', '2024-12-21', 'CREW007', 'Flight_Attendant', '2024-12-21 21:50:00', NULL),
('LH500', '2024-12-22', 'CREW008', 'Captain', '2024-12-22 09:15:00', NULL),
('LH500', '2024-12-22', 'CREW002', 'First_Officer', '2024-12-22 09:15:00', NULL),
('SQ600', '2024-12-22', 'CREW003', 'Flight_Attendant', '2024-12-21 23:20:00', '2024-12-22 10:15:00'),
('AA102', '2024-12-22', 'CREW005', 'Captain', '2024-12-22 14:30:00', NULL),
('AA102', '2024-12-22', 'CREW006', 'Flight_Attendant', '2024-12-22 14:30:00', NULL);

-- TICKET 
INSERT INTO `TICKET` (`ticket_id`, `booking_id`, `flight_number`, `flight_date`, `passenger_id`, `seat_number`, `class`, `fare_amount`, `ticket_status`, `check_in_status`, `check_in_time`, `boarding_time`, `baggage_allowance_kg`, `special_requests`) VALUES
('TK001', 'BK001', 'AA100', '2024-12-20', 'PAX001', '12A', 'Economy', 485.99, 'Used', 'Boarded', '2024-12-20 06:00:00', '2024-12-20 07:30:00', 23, NULL),
('TK002', 'BK002', 'DL200', '2024-12-21', 'PAX002', '3D', 'Business', 1250.00, 'Active', 'Checked_In', '2024-12-21 16:00:00', NULL, 32, 'Vegetarian meal'),
('TK003', 'BK003', 'BA300', '2024-12-21', 'PAX003', '15F', 'Economy', 890.50, 'Active', 'Checked_In', '2024-12-21 08:00:00', NULL, 23, 'Aisle seat preference'),
('TK004', 'BK004', 'EK400', '2024-12-21', 'PAX004', '7A', 'Business', 1560.75, 'Active', 'Checked_In', '2024-12-21 21:30:00', NULL, 32, 'Kosher meal'),
('TK005', 'BK005', 'LH500', '2024-12-22', 'PAX005', '2C', 'First', 2100.00, 'Active', 'Not_Checked_In', NULL, NULL, 32, 'Wheelchair assistance'),
('TK006', 'BK006', 'SQ600', '2024-12-22', 'PAX006', '18B', 'Economy', 975.25, 'Active', 'Checked_In', '2024-12-21 23:00:00', '2024-12-22 00:45:00', 23, NULL),
('TK007', 'BK007', 'AA102', '2024-12-22', 'PAX007', '25C', 'Economy', 425.00, 'Active', 'Not_Checked_In', NULL, NULL, 23, 'Extra legroom'),
('TK008', 'BK008', 'AA101', '2024-12-20', 'PAX008', '8D', 'Premium_Economy', 680.80, 'Used', 'Boarded', '2024-12-20 12:00:00', '2024-12-20 13:30:00', 32, 'Japanese meal'),
('TK009', 'BK009', 'EK400', '2024-12-21', 'PAX009', '5C', 'Business', 1890.00, 'Active', 'Checked_In', '2024-12-21 21:15:00', NULL, 32, 'Halal meal'),
('TK010', 'BK010', 'DL200', '2024-12-21', 'PAX010', '22A', 'Economy', 650.75, 'Active', 'Checked_In', '2024-12-21 16:30:00', NULL, 23, 'Window seat preference'),
('TK011', 'BK011', 'AA102', '2024-12-22', 'PAX011', '14B', 'Economy', 520.50, 'Active', 'Not_Checked_In', NULL, NULL, 23, NULL),
('TK012', 'BK012', 'LH500', '2024-12-22', 'PAX012', '1A', 'First', 1250.00, 'Active', 'Not_Checked_In', NULL, NULL, 32, 'Vegan meal, Extra pillow');

-- BAGGAGE 
INSERT INTO `BAGGAGE` (`baggage_id`, `ticket_id`, `baggage_type`, `weight_kg`, `status`, `special_handling`, `current_location`) VALUES
('BG001', 'TK001', 'Checked', 18.5, 'Delivered', NULL, 'LAX Baggage Claim 4'),
('BG002', 'TK001', 'Carry_On', 7.2, 'Delivered', NULL, 'With passenger'),
('BG003', 'TK002', 'Checked', 22.8, 'In_Transit', NULL, 'ATL Transfer Hub'),
('BG004', 'TK003', 'Checked', 19.5, 'Loaded', NULL, 'LHR Aircraft Hold'),
('BG005', 'TK004', 'Checked', 25.0, 'Loaded', 'Fragile', 'DXB Aircraft Hold'),
('BG006', 'TK005', 'Checked', 15.5, 'Checked_In', NULL, 'FRA Baggage Sorting'),
('BG007', 'TK006', 'Checked', 21.2, 'In_Transit', NULL, 'SIN Transfer'),
('BG008', 'TK008', 'Checked', 16.8, 'Delivered', NULL, 'JFK Baggage Claim 7'),
('BG009', 'TK009', 'Checked', 28.5, 'Loaded', NULL, 'DXB Aircraft Hold'),
('BG010', 'TK009', 'Carry_On', 8.2, 'Loaded', NULL, 'With passenger'),
('BG011', 'TK010', 'Checked', 20.1, 'In_Transit', NULL, 'ATL Transfer Hub'),
('BG012', 'TK011', 'Checked', 17.5, 'Checked_In', NULL, 'ORD Baggage Sorting'),
('BG013', 'TK012', 'Checked', 24.8, 'Checked_In', 'Priority', 'FRA Baggage Sorting'),
('BG014', 'TK012', 'Carry_On', 6.5, 'Checked_In', NULL, 'With passenger');

-- ATC
INSERT INTO `ATC` (`atc_id`, `airport_code`, `shift_start`, `shift_end`, `controller_count`, `frequency`, `sector`, `status`) VALUES
('ATC001', 'JFK', '06:00:00', '14:00:00', 3, 119.100, 'Tower', 'Active'),
('ATC002', 'JFK', '14:00:00', '22:00:00', 2, 119.100, 'Tower', 'Active'),
('ATC003', 'LAX', '00:00:00', '08:00:00', 2, 120.950, 'Ground', 'Active'),
('ATC004', 'LHR', '08:00:00', '16:00:00', 4, 118.700, 'Approach', 'Active'),
('ATC005', 'DXB', '16:00:00', '00:00:00', 3, 119.000, 'Tower', 'Active'),
('ATC006', 'NRT', '22:00:00', '06:00:00', 2, 118.200, 'Ground', 'Maintenance'),
('ATC007', 'SIN', '12:00:00', '20:00:00', 3, 119.400, 'Approach', 'Active'),
('ATC008', 'CDG', '04:00:00', '12:00:00', 2, 118.150, 'Tower', 'Active'),
('ATC009', 'ORD', '06:00:00', '14:00:00', 4, 120.550, 'Tower', 'Active'),
('ATC010', 'ATL', '14:00:00', '22:00:00', 5, 121.900, 'Approach', 'Active'),
('ATC011', 'FRA', '22:00:00', '06:00:00', 2, 118.500, 'Ground', 'Active'),
('ATC012', 'CDG', '20:00:00', '04:00:00', 3, 119.350, 'Tower', 'Active');

-- FLIGHT_STATUS_LOG 
INSERT INTO `FLIGHT_STATUS_LOG` (`flight_number`, `flight_date`, `old_status`, `new_status`, `reason`, `changed_by`, `changed_at`) VALUES
('AA100', '2025-12-20', 'Scheduled', 'Delayed', 'Air traffic control delay', 'EMP001', '2024-12-20 07:45:00'),
('AA100', '2024-12-20', 'Delayed', 'Boarding', 'Ready for departure', 'EMP001', '2024-12-20 07:55:00'),
('AA100', '2024-12-20', 'Boarding', 'Departed', 'Flight departed', 'EMP001', '2024-12-20 08:15:00'),
('AA100', '2024-12-20', 'Departed', 'Arrived', 'Flight arrived', 'EMP005', '2024-12-20 11:45:00'),
('AA101', '2024-12-20', 'Scheduled', 'Boarding', 'On time departure', 'EMP005', '2024-12-20 13:30:00'),
('AA101', '2024-12-20', 'Boarding', 'Departed', 'Flight departed', 'EMP005', '2024-12-20 14:00:00'),
('AA101', '2024-12-20', 'Departed', 'Arrived', 'Flight arrived early', 'EMP001', '2024-12-20 22:25:00'),
('BA300', '2024-12-21', 'Scheduled', 'Delayed', 'Weather conditions', 'EMP007', '2024-12-21 09:15:00'),
('EK400', '2024-12-21', 'Scheduled', 'Boarding', 'Ready for departure', 'EMP009', '2024-12-21 23:30:00'),
('SQ600', '2024-12-22', 'Scheduled', 'Boarding', 'Ready for departure', 'EMP011', '2024-12-22 00:50:00'),
('SQ600', '2024-12-22', 'Boarding', 'Departed', 'Flight departed', 'EMP011', '2024-12-22 01:20:00'),
('DL200', '2024-12-21', NULL, 'Scheduled', 'Initial scheduling', 'SYSTEM', '2024-11-20 10:00:00'),
('AA150', '2024-12-21', NULL, 'Scheduled', 'Initial scheduling', 'SYSTEM', '2024-11-21 09:00:00'),
('AA150', '2024-12-21', 'Scheduled', 'Cancelled', 'Aircraft mechanical issue', 'EMP001', '2024-12-21 12:00:00'),
('DL250', '2024-12-22', NULL, 'Scheduled', 'Initial scheduling', 'SYSTEM', '2024-11-22 08:00:00'),
('DL250', '2024-12-22', 'Scheduled', 'Delayed', 'Crew scheduling conflict', 'EMP005', '2024-12-22 07:30:00'),
('UA200', '2024-12-23', NULL, 'Scheduled', 'Flight scheduled', 'SYSTEM', '2024-11-23 09:00:00'),
('QR300', '2024-12-23', NULL, 'Scheduled', 'Flight scheduled', 'SYSTEM', '2024-11-23 09:00:00'),
('BA400', '2024-12-23', NULL, 'Scheduled', 'Flight scheduled', 'SYSTEM', '2024-11-23 09:00:00'),
('EK500', '2024-12-24', NULL, 'Scheduled', 'Flight scheduled', 'SYSTEM', '2024-11-24 09:00:00'),
('LH600', '2024-12-24', NULL, 'Scheduled', 'Flight scheduled', 'SYSTEM', '2024-11-24 09:00:00'),
('SQ700', '2024-12-25', NULL, 'Scheduled', 'Flight scheduled', 'SYSTEM', '2024-11-25 09:00:00');