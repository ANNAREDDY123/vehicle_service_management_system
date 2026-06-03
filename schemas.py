from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class VehicleCreate(BaseModel):
    vehicle_number: str
    brand: str
    model: str
    customer_id: int

class VehicleUpdate(BaseModel):
    vehicle_number: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None

class ServiceCreate(BaseModel):
    vehicle_id: int
    service_type: str
    service_cost: float
    service_date: date

class ServiceUpdate(BaseModel):
    status: str
