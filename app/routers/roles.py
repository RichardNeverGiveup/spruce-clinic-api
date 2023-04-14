from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    tags=['roles']
)

@router.get("/roles") # get all roles
def get_roles(db: Session = Depends(get_db)):
    role = db.query(models.Roles).all()
    return role

@router.get("/roles/{id}") # get one single role
def get_role(id: int, db: Session = Depends(get_db)):
    
    role = db.query(models.Roles).all()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found!")
    return role

@router.post("/roles", status_code=status.HTTP_201_CREATED)
def create_role(role, db: Session = Depends(get_db)):
    pass