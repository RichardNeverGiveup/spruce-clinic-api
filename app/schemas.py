from pydantic import BaseModel, EmailStr
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