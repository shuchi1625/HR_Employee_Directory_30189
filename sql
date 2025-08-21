-- Create the database
-- CREATE DATABASE hr_db;

-- Connect to the new database
-- \c hr_db;

-- Create the jobs table
CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) UNIQUE NOT NULL,
    min_salary DECIMAL(10, 2),
    max_salary DECIMAL(10, 2)
);

-- Create the departments table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) UNIQUE NOT NULL,
    location VARCHAR(255)
);

-- Create the employees table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    hire_date DATE,
    salary DECIMAL(10, 2),
    job_id INT,
    department_id INT,
    manager_id INT,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

-- Insert sample data into the jobs table
INSERT INTO jobs (job_title, min_salary, max_salary) VALUES
('Software Engineer', 90000.00, 120000.00),
('Data Analyst', 70000.00, 95000.00),
('HR Manager', 80000.00, 110000.00),
('Sales Representative', 60000.00, 85000.00),
('Marketing Specialist', 75000.00, 100000.00);

-- Insert sample data into the departments table
INSERT INTO departments (department_name, location) VALUES
('Engineering', 'San Francisco'),
('Sales', 'New York'),
('Human Resources', 'Chicago'),
('Marketing', 'Boston');

-- Insert sample data into the employees table (ensure job_id and department_id match your insertions)
INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, salary, job_id, department_id) VALUES
('Alice', 'Johnson', 'alice.j@company.com', '555-0101', '2020-03-15', 105000.00, 1, 1),
('Bob', 'Williams', 'bob.w@company.com', '555-0102', '2019-07-22', 78000.00, 4, 2),
('Charlie', 'Davis', 'charlie.d@company.com', '555-0103', '2021-01-10', 85000.00, 3, 3),
('Diana', 'Miller', 'diana.m@company.com', '555-0104', '2018-05-30', 92000.00, 2, 1),
('Edward', 'Brown', 'edward.b@company.com', '555-0105', '2022-09-01', 82000.00, 4, 2);
