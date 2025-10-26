# ✈️ Airport Management System

A comprehensive, CLI-based Airport Management System built with Python and MySQL for managing flights, passengers, bookings, and more.

## Overview

This project is a robust database management application that simulates the core operations of an airport. It allows users to interact with a detailed and normalized database through a user-friendly command-line interface. The system is designed to handle various airport-related tasks, from viewing flight schedules and managing passenger bookings to generating operational reports and ensuring data integrity with advanced database features.

## Key Features

The application is organized into a clear, menu-driven interface, allowing users to perform a wide range of operations.

### Core Operations

#### View & Search

-   View all upcoming flights with their status, route, and airline.
-   See detailed passenger lists (manifests) for a specific flight.
-   View the assigned crew members for a flight, ordered by role.
-   Search for employees and their complete details by ID.
-   Find the cheapest flights available on a specific route and date.

#### Insert

-   Add new flight schedules to the database.
-   Add new passenger records.
-   Create new bookings and tickets, linking passengers to flights.
-   Add new employees to the system, assigning them to an airline or airport.

#### Update

-   Update the real-time status of flights (e.g., Scheduled, Delayed, Boarding, Cancelled).
-   Update employee salaries in bulk based on their position.

#### Delete / Cancel

-   Cancel a passenger's ticket (updates status to 'Cancelled').
-   Cancel a scheduled flight (updates status to 'Cancelled').
-   Terminate an employee's record (updates status to 'Terminated').

### Reporting & Advanced Database Features

#### Operational Reports

-   Calculate and display the exact duration of any flight.
-   Generate an "Occupancy vs. Price" report for a flight, showing passenger counts and average fare per class.
-   Calculate the average ticket price for any given route.

#### Advanced SQL Features

-   **Stored Procedure:** A stored procedure (`GenerateFlightRevenueReport`) is used to calculate and report the total revenue for any given flight.
-   **Trigger:** An automatic trigger logs every change to a flight's status in the `FLIGHT_STATUS_LOG` table, ensuring a complete audit trail for operations.
-   **Complex Joins:** Most features use multi-table joins to retrieve comprehensive, real-world data.

## Database Schema

The system is built on a relational database with 18 interconnected tables to ensure data integrity and minimize redundancy (3NF). The core tables include:

-   **AIRPORT:** Stores details of all airports (e.g., JFK, LAX).
-   **AIRLINE:** Contains information about different airlines.
-   **FLIGHT:** The central table for all flight schedules.
-   **PASSENGER:** Manages passenger information.
-   **BOOKING & TICKET:** Handle the booking and ticketing process.
-   **EMPLOYEE & CREW_MEMBER:** Store data for all staff and flight crews.
-   **FLIGHT_STATUS_LOG:** An audit table automatically populated by a trigger.

The full schema with all tables, columns, and relationships can be found in the `sql/airport_management_schema.sql` file.

## Technologies Used

-   **Backend:** Python
-   **Database:** MySQL
-   **Connector:** pymysql library

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

-   Python 3.x installed.
-   MySQL Server installed and running. For Debian/Ubuntu, you can follow these steps:

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

### 2. Clone the Repository

```bash
git clone https://github.com/dakshgoel2008/Airport_Management_DB.git
cd airport_management_db
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Configuration

1. Create a `.env` file in the root directory. You can copy or rename the `env.sample` file.
2. Add your MySQL credentials to this `.env` file:

```env
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
```

### 5. Run the Application

Execute the main script from your terminal:

```bash
python myWorld.py
```

On the first run, the application will ask: `Import schema and data? (y/n):`.

-   You must type `y` and press Enter.
-   This will automatically create the `AIRPORT_MANAGEMENT_DB` database, build the schema, and populate it with sample data.

## How to Use

Once the application is running, you will be greeted with the main menu. Simply enter the number corresponding to the action you wish to perform and follow the on-screen prompts.

```
##################################################
AIRPORT MANAGEMENT SYSTEM
##################################################
Choose operation type:
1. View
2. Insert
3. Update
4. Delete / Cancel
5. Search
6. Reports
1000. Exit
Enter your choice:
```
