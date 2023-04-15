from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    prefix='/appointments',
    tags=['appointments']
)

@router.get("/") # get all 
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(models.appointments).all()
    return appointments

@router.get("/{id}") # get one single
def get_appointment(id: int, db: Session = Depends(get_db)):
    
    appointment = db.query(models.Appointments).filter(models.Appointments.aid == id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with id {id} not found!")
    return appointment

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = models.Appointments(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment