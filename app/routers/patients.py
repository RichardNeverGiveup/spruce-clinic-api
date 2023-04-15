from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    prefix='/patients',
    tags=['patients']
)

@router.get("/") # get all 
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patients).all()
    return patients

@router.get("/{id}") # get one single
def get_patient(id: int, db: Session = Depends(get_db)):
    
    patient = db.query(models.Patients).filter(models.Patients.pid == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id {id} not found!")
    return patient

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    # print(patient)
    new_patient = models.Patients(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db)):
    patient_query = db.query(models.Patients).filter(models.Patients.pid == id)
    patient = patient_query.first()
    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id {id} not found!")
    
    patient_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PatientResponse)
def update_patient(id: int, new_patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient_query = db.query(models.Patients).filter(models.Patients.pid == id)
    patient = patient_query.first()
    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id {id} not found!")
    patient_query.update(new_patient.dict(), synchronize_session=False)
    db.commit()
    return patient_query.first()