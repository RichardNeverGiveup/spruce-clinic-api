from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class RoleCreate(BaseModel):
    role_type: str

class RoleResponse(BaseModel):
    rid: int
    # role_type: str # we can tailor the response and remain the fields we want
    role_type: str

    class Config:
        orm_mode = True

class ContractCreate(BaseModel):
    # although date is optional, but front-end should make this field required!!!!
    joining_date: Optional[datetime] = Field(timezone_aware=True)
    contract_duration: int
    salary: int

class ContractResponse(BaseModel):
    cid: int
    joining_date: datetime = Field(timezone_aware=True)
    contract_duration: int
    salary: int

    class Config:
        orm_mode = True

class EmployeeCreate(BaseModel):
    role_id: int
    contract_id: int
    full_name: str
    email: EmailStr
    pwd: str
    tel: str
    gender: bool
    address: str
    education: str
    experience: int

class EmployeeResponse(EmployeeCreate):
    id: int
    modified_at: datetime = Field(timezone_aware=True)
    
    class Config:
        orm_mode = True

class EmployeeUpdate(BaseModel):
    role_id: Optional[int]
    contract_id: Optional[int]
    full_name: Optional[str]
    email: Optional[EmailStr]
    pwd: Optional[str]
    tel: Optional[str]
    gender: Optional[str]
    address: Optional[str]
    education: Optional[str]
    experience: Optional[str]

class PatientCreate(BaseModel):
    full_name: str
    email: EmailStr
    pwd: str
    tel: str
    gender: bool
    address: str
    insurance_number: str
    surgery_history: str
    allergy: str
    drug_history: str

class PatientResponse(PatientCreate):
    pid: int
    modified_at: datetime = Field(timezone_aware=True)
    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    notes: str
    start_time: datetime = Field(timezone_aware=True)
    end_time: datetime = Field(timezone_aware=True)

class AppointmentResponse(AppointmentCreate):
    aid: int
    modified_at: datetime = Field(timezone_aware=True)
    class Config:
        orm_mode = True