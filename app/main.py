from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from . import security
from .security import oauth2_scheme
from jose import JWTError, jwt
from typing import Optional

from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Guest Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Guest Management System"}

# 验证当前用户
async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    admin = crud.get_admin_by_email(db, email=token_data.email)
    if admin is None:
        raise credentials_exception
    return admin

# 登录路由
@app.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = crud.authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 创建管理员路由
@app.post("/admin/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_email(db, email=admin.email)
    if db_admin:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return crud.create_admin(db=db, admin=admin)

# Guest routes
@app.post("/guests/", response_model=schemas.Guest)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.create_guest(db=db, guest=guest)

@app.get("/guests/", response_model=List[schemas.Guest])
def read_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    guests = crud.get_guests(db, skip=skip, limit=limit)
    return guests

@app.get("/guests/{guest_id}", response_model=schemas.Guest)
def read_guest(guest_id: int, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    db_guest = crud.get_guest(db, guest_id=guest_id)
    if db_guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    return db_guest

@app.put("/guests/{guest_id}", response_model=schemas.Guest)
def update_guest(guest_id: int, guest: schemas.GuestCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.update_guest(db=db, guest_id=guest_id, guest=guest)

@app.delete("/guests/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.delete_guest(db=db, guest_id=guest_id)

@app.get("/guests/search/", response_model=List[schemas.Guest])
def search_guests_by_name(name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    guests = crud.get_guests_by_name(db, name=name, skip=skip, limit=limit)
    return guests

@app.get("/guests/level/{guest_level}", response_model=List[schemas.Guest])
def get_guests_by_level(guest_level: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    guests = crud.get_guests_by_level(db, guest_level=guest_level, skip=skip, limit=limit)
    return guests

# Staff routes
@app.post("/staff/", response_model=schemas.Staff)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.create_staff(db=db, staff=staff)

@app.get("/staff/{staff_id}", response_model=schemas.Staff)
def read_staff(staff_id: int, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

# Committee Member routes
@app.post("/committee/", response_model=schemas.CommitteeMember)
def create_committee_member(member: schemas.CommitteeMemberCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.create_committee_member(db=db, member=member)

# Event routes
@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.create_event(db=db, event=event)

@app.get("/events/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events

@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@app.put("/events/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.update_event(db=db, event_id=event_id, event=event)
