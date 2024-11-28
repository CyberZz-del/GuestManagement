from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from typing import List, Optional

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Guest CRUD operations
def create_guest(db: Session, guest: schemas.GuestCreate):
    db_guest = models.Guest(**guest.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

def get_guest(db: Session, guest_id: int):
    return db.query(models.Guest).filter(models.Guest.id == guest_id).first()

def get_guests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Guest).offset(skip).limit(limit).all()

def get_guests_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(models.Guest).filter(models.Guest.name.like(f"%{name}%")).offset(skip).limit(limit).all()

def get_guests_by_level(db: Session, guest_level: int, skip: int = 0, limit: int = 100):
    return db.query(models.Guest).filter(models.Guest.guest_level == guest_level).offset(skip).limit(limit).all()

def update_guest(db: Session, guest_id: int, guest: schemas.GuestCreate):
    db_guest = get_guest(db, guest_id)
    if db_guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    for key, value in guest.dict(exclude_unset=True).items():
        setattr(db_guest, key, value)
    
    db.commit()
    db.refresh(db_guest)
    return db_guest

def delete_guest(db: Session, guest_id: int):
    db_guest = get_guest(db, guest_id)
    if db_guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    db.delete(db_guest)
    db.commit()
    return {"message": "Guest deleted successfully"}

# Staff CRUD operations
def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()

def update_staff(db: Session, staff_id: int, staff: schemas.StaffCreate):
    db_staff = get_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    for key, value in staff.dict(exclude_unset=True).items():
        setattr(db_staff, key, value)
    
    db.commit()
    db.refresh(db_staff)
    return db_staff

# Committee Member CRUD operations
def create_committee_member(db: Session, member: schemas.CommitteeMemberCreate):
    db_member = models.CommitteeMember(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_committee_member(db: Session, member_id: int):
    return db.query(models.CommitteeMember).filter(models.CommitteeMember.id == member_id).first()

# Event CRUD operations
def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event
