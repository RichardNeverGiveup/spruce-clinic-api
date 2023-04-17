from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=["Authentication"],
    prefix="/login"
)


@router.post('/employee', response_model=schemas.Token)
# OAuth2PasswordRequestForm accept username and password, no matter what the actual field in db means username
def login_employee(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    employee = db.query(models.Employees).filter(models.Employees.email == credentials.username).first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid username or email.")
    
    if not utils.verify(credentials.password, employee.pwd):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid password.")
    
    # create a token
    access_token = oauth2.create_access_token(data={"scope": "employee", "id": employee.id, "role_id": employee.role_id})

    return {"access_token" : access_token, "token_type": "bearer"}

@router.post('/patient', response_model=schemas.Token)
def login_patient(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    patient = db.query(models.Patients).filter(models.Patients.email == credentials.username).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid username or email.")
    if not utils.verify(credentials.password, patient.pwd):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid password.")
    
    # create a token
    access_token = oauth2.create_access_token(data={"scope": "patient", "pid": patient.pid})

    return {"access_token" : access_token, "token_type": "bearer"}