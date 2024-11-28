from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

# 基础User模型
class UserBase(BaseModel):
    name: str
    gender: Optional[Gender] = None
    contact: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    type: str

    class Config:
        from_attributes = True

# Staff模型
class StaffBase(UserBase):
    responsibility: Optional[str] = None
    authority_level: Optional[int] = None

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: int
    type: str = "staff"

    class Config:
        from_attributes = True

# Guest模型
class GuestBase(UserBase):
    location: Optional[str] = None
    organization: Optional[str] = None
    email: Optional[EmailStr] = None
    passport: Optional[str] = None
    nationality: Optional[str] = None
    guest_level: Optional[int] = None

class GuestCreate(GuestBase):
    pass

class Guest(GuestBase):
    id: int
    type: str = "guest"
    events: List["Event"] = []

    class Config:
        from_attributes = True

# CommitteeMember模型
class CommitteeMemberBase(UserBase):
    role: Optional[str] = None
    permission_level: Optional[int] = None
    team_type: Optional[str] = None

class CommitteeMemberCreate(CommitteeMemberBase):
    pass

class CommitteeMember(CommitteeMemberBase):
    id: int
    type: str = "committee_member"
    events: List["Event"] = []

    class Config:
        from_attributes = True

# Event模型
class EventBase(BaseModel):
    title: str
    location: Optional[str] = None
    time: Optional[datetime] = None
    min_permission_level: Optional[int] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    guests: List[Guest] = []
    managers: List[CommitteeMember] = []

    class Config:
        from_attributes = True

# 更新循环引用 - 使用新的model_rebuild方法
Guest.model_rebuild()
CommitteeMember.model_rebuild()
