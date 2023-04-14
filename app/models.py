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
    # role_id = Column(Integer, ForeignKey("role.rid", ondelete="SET DEFAULT"), default=0, nullable=False)
    # when we delete a contract, we delete this employee
    # contract_id = Column(Integer, ForeignKey("contracts.cid", ondelete="CASCADE"), nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    gender = Column(Boolean, nullable=False)  # 0 means female, 1 means male
    address = Column(String, nullable=False)
    education = Column(String, nullable=False) # bachelor, master, or phd
    experience = Column(Integer, nullable=False)  # how many years
    modified_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner = relationship("User")  # 这里会自动去获取对应FK的user表里面的信息