from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas, oauth2
router = APIRouter(
    prefix='/appointments',
    tags=['appointments']
)

@router.get("/") # get all 
def get_appointments(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_employee)):
    print(current_user.id)
    appointments = db.query(models.Appointments).all()
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appointment_query = db.query(models.Appointments).filter(models.Appointments.aid == id)
    appointment = appointment_query.first()
    if appointment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with id {id} not found!")
    # role tb is never accessible for non admin employees
    appointment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.AppointmentResponse)
def update_appointment(id: int, new_role: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appointment_query = db.query(models.Appointments).filter(models.Appointments.aid == id)
    appointment = appointment_query.first()
    if appointment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointment with id {id} not found!")
    appointment_query.update(new_role.dict(), synchronize_session=False)
    db.commit()
    return appointment_query.first()