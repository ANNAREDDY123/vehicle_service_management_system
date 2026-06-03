# Vehicle Service Management System

## Objective

Backend system to manage Customers, Vehicles, and Service Requests.

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / MySQL
- JWT Authentication

## Features

### Customer Management
- Add Customer
- View Customers
- Update Customer
- Soft Delete Customer

### Vehicle Management
- Add Vehicle
- View Vehicles
- Update Vehicle
- Soft Delete Vehicle
- Customer → Vehicle Relationship

### Service Management
- Create Service Request
- Update Service Status
- View Service History
- Get Service Details

### Business Rules
- Customer must exist before adding vehicle
- Vehicle must exist before service request
- Service cost > 0
- Completed services cannot be modified

### Bonus Features
- JWT Authentication
- Pagination
- Search by Vehicle Number
- Soft Delete
- Swagger Documentation

## Project Structure

vehicle_service_management_system/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── requirements.txt
├── README.md
├── sql/
│ ├── schema.sql
│ └── report_queries.sql
└── postman_collection.json

## Run Project

pip install -r requirements.txt
uvicorn main:app 


Explanation

I created four tables: Users, Customers, Vehicles, and Service Requests.

A customer can own multiple vehicles. Service requests are linked to vehicles.

JWT authentication is implemented using Register and Login APIs.

Soft delete is implemented for customers and vehicles using the is_deleted flag.

Business rules validate customer existence, vehicle existence, positive service costs, and prevent editing completed services.

SQL reports provide revenue analysis, vehicle service counts, customer rankings, and pending service requests.

Submission Files

Source Code
SQL Script
SQL Report Queries
Postman Collection
README





