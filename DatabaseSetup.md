# Student Management System

## Database Setup

### Create the Database and Table

Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin, or command-line interface).

Run the following SQL script to create the `student_management` database and `students` table:

```sql
-- Create Database
CREATE DATABASE IF NOT EXISTS student_management;

-- Use the Database
USE student_management;

-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile VARCHAR(15) NOT NULL,
    alt_mobile VARCHAR(15),
    branch VARCHAR(50) NOT NULL,
    course VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    dob DATE NOT NULL,
    address TEXT
);
