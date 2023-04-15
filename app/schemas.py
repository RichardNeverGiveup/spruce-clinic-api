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