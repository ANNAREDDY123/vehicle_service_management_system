from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    password = Column(String(255))

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String(50), unique=True)
    brand = Column(String(100))
    model = Column(String(100))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    is_deleted = Column(Boolean, default=False)

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    service_id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"))
    service_type = Column(String(100))
    service_cost = Column(Float)
    service_date = Column(Date)
    status = Column(String(30), default="Pending")
