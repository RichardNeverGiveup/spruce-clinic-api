from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    prefix='/employees',
    tags=['employees']
)

@router.get("/") # get all 
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employees).all()
    return employees

@router.get("/{id}") # get one single
def get_employee(id: int, db: Session = Depends(get_db)):
    
    employee = db.query(models.Employees).filter(models.Employees.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    return employee

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = models.Employees(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(get_db)):
    employee_query = db.query(models.Employees).filter(models.Employees.id == id)
    employee = employee_query.first()
    if employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    # employee tb is never accessible for non admin employees
    employee_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: int, new_employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee_query = db.query(models.Employees).filter(models.Employees.id == id)
    employee = employee_query.first()
    if employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    employee_query.update(new_employee.dict(), synchronize_session=False)
    db.commit()
    return employee_query.first()