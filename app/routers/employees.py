from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    tags=['employees']
)

@router.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(employee, db: Session = Depends(get_db)):
    
    new_employee = models.Employees(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee