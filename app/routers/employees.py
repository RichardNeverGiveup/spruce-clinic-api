from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas, utils, oauth2
router = APIRouter(
    prefix='/employees',
    tags=['employees']
)

ADMIN = 15 # 15 means the role_type of admin, need to use a more elegant way to do this

@router.get("/") # get all 
def get_employees(db: Session = Depends(get_db), current_employee:schemas.TokenDataEmployee=Depends(oauth2.get_current_employee)):
    if current_employee.role_id != ADMIN:  
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admin can check all the employees!")
    employees = db.query(models.Employees).all()
    return employees

@router.get("/{id}") # get one single
def get_employee(id: int, db: Session = Depends(get_db), current_employee:schemas.TokenDataEmployee=Depends(oauth2.get_current_employee)):
    if current_employee.id != id:  # make sure only employees themselves can only see their profiles
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You can only browse your only employee profile")
    
    employee = db.query(models.Employees).filter(models.Employees.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    return employee

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_employee:schemas.TokenDataEmployee=Depends(oauth2.get_current_employee)):
    if current_employee.role_id != ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admin can create a new employee profile!")
    # hash the pwd
    hashed_password = utils.hash(employee.pwd)
    employee.pwd = hashed_password

    new_employee = models.Employees(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(get_db), current_employee:schemas.TokenDataEmployee=Depends(oauth2.get_current_employee)):
    if current_employee.id != id:  # make sure only employees themselves can only delete their profile
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You can only delete your only employee profile")
    employee_query = db.query(models.Employees).filter(models.Employees.id == id)
    employee = employee_query.first()
    if employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    # employee tb is never accessible for non admin employees
    employee_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: int, new_employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_employee:schemas.TokenDataEmployee=Depends(oauth2.get_current_employee)):
    if current_employee.role_id != ADMIN or current_employee.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admin and profile owner can use this api")
    employee_query = db.query(models.Employees).filter(models.Employees.id == id)
    employee = employee_query.first()
    if employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    
    # hash the pwd
    hashed_password = utils.hash(new_employee.pwd)
    new_employee.pwd = hashed_password

    employee_query.update(new_employee.dict(), synchronize_session=False)
    db.commit()
    return employee_query.first()

@router.patch("/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: int, new_employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    """Please use this api only for debugging!!!!, no authentication added here
    this patch method is for updating some fields not all of them."""
    employee_query = db.query(models.Employees).filter(models.Employees.id == id)
    employee = employee_query.first()
    if employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {id} not found!")
    # print(employee_query)
    for k, v in new_employee.dict().items():
        if(v != None):
            if (k == "pwd"):
                # hash the pwd
                # print(k, v)
                hashed_password = utils.hash(v)
                v = hashed_password
            setattr(employee, k, v)
    db.commit()
    return employee_query.first()