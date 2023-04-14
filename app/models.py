from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, nullable=False)
    # here we assume all employees is default to be role_id 0 (means "intern" in our roles table, minimum authorization in our clinic)
    # fk should be added later, since we do not have these two tables for now
    role_id = Column(Integer, ForeignKey("roles.rid", ondelete="CASCADE"), server_default="0", nullable=False)
    # when we delete a contract, we delete this employee
    contract_id = Column(Integer, ForeignKey("contracts.cid", ondelete="CASCADE"), nullable=False)

    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    gender = Column(Boolean, nullable=False)  # 0 means female, 1 means male
    address = Column(String, nullable=False)
    education = Column(String, nullable=False) # bachelor, master, or phd
    experience = Column(Integer, nullable=False)  # how many years
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # owner = relationship("User")  # 这里会自动去获取对应FK的user表里面的信息

class Roles(Base):
    __tablename__ = 'roles'
    rid = Column(Integer, primary_key=True, nullable=False)
    role_type = Column(String, nullable=False)

class Contracts(Base):
    __tablename__ = 'contracts'
    cid = Column(Integer, primary_key=True, nullable=False)
    # sign a contract online in our system, the joining_date is auto added
    joining_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # default is one month contract
    contract_duration = Column(Integer, nullable=False, server_default="1")
    salary = Column(Integer, nullable=False)

class Patients(Base):
    __tablename__ = 'patients'
    pid = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    gender = Column(Boolean, nullable=False)  # 0 means female, 1 means male
    tel = Column(String, nullable=False)
    address = Column(String, nullable=False)
    insurance_number = Column(String, nullable=False)
    surgery_history = Column(String, nullable=False)
    allergy = Column(String, nullable=False)
    drug_history = Column(String, nullable=False)
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Appointments(Base):
    __tablename__ = 'appointments'
    aid = Column(Integer, primary_key=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.pid", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    notes = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))