from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import schemas
from database import Base, engine, get_db
from auth import hash_password, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Service Management System")

@app.get("/")
def home():
    return {"message": "Vehicle Service Management API Running"}


# ---------------- AUTH ----------------

@app.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": db_user.username}
    )

    return {"access_token": token}


# ---------------- CUSTOMER MANAGEMENT ----------------

@app.post("/customers")
def add_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):

    new_customer = models.Customer(**customer.dict())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "Customer added successfully",
        "customer_id": new_customer.customer_id
    }


@app.get("/customers")
def view_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.Customer).filter(
        models.Customer.is_deleted == False
    )

    total = query.count()

    customers = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "customers": customers
    }


@app.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(get_db)
):

    db_customer = db.query(models.Customer).filter(
        models.Customer.customer_id == customer_id
    ).first()

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)

    db.commit()

    return {"message": "Customer updated successfully"}


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):

    customer = db.query(models.Customer).filter(
        models.Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.is_deleted = True

    db.commit()

    return {"message": "Customer soft deleted"}


# ---------------- VEHICLE MANAGEMENT ----------------

@app.post("/vehicles")
def add_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):

    customer = db.query(models.Customer).filter(
        models.Customer.customer_id == vehicle.customer_id,
        models.Customer.is_deleted == False
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer does not exist"
        )

    new_vehicle = models.Vehicle(**vehicle.dict())

    db.add(new_vehicle)
    db.commit()

    return {"message": "Vehicle added successfully"}


@app.get("/vehicles")
def view_vehicles(
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.Vehicle).filter(
        models.Vehicle.is_deleted == False
    )

    if search:
        query = query.filter(
            models.Vehicle.vehicle_number.like(f"%{search}%")
        )

    total = query.count()

    vehicles = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "vehicles": vehicles
    }


@app.put("/vehicles/{vehicle_id}")
def update_vehicle(
    vehicle_id: int,
    vehicle: schemas.VehicleUpdate,
    db: Session = Depends(get_db)
):

    db_vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.vehicle_id == vehicle_id
    ).first()

    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    for key, value in vehicle.dict(exclude_unset=True).items():
        setattr(db_vehicle, key, value)

    db.commit()

    return {"message": "Vehicle updated successfully"}


@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.vehicle_id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle.is_deleted = True

    db.commit()

    return {"message": "Vehicle soft deleted"}


# ---------------- SERVICE REQUESTS ----------------

@app.post("/services")
def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db)
):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.vehicle_id == service.vehicle_id,
        models.Vehicle.is_deleted == False
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    if service.service_cost <= 0:
        raise HTTPException(
            status_code=400,
            detail="Service cost must be greater than 0"
        )

    new_service = models.ServiceRequest(**service.dict())

    db.add(new_service)
    db.commit()

    return {"message": "Service request created"}


@app.put("/services/{service_id}")
def update_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(get_db)
):

    db_service = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.service_id == service_id
    ).first()

    if not db_service:
        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    if db_service.status == "Completed":
        raise HTTPException(
            status_code=400,
            detail="Completed services cannot be edited"
        )

    db_service.status = service.status

    db.commit()

    return {"message": "Service updated successfully"}


@app.get("/services")
def view_service_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):

    query = db.query(models.ServiceRequest)

    total = query.count()

    services = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "services": services
    }

@app.get("/services/{service_id}")
def get_service_details(
    service_id: int,
    db: Session = Depends(get_db)
):

    service = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.service_id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )
    return service
