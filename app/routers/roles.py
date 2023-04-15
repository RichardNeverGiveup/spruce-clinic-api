from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    prefix='/roles',
    tags=['roles']
)

@router.get("/") # get all roles
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Roles).all()
    return roles

@router.get("/{id}") # get one single role
def get_role(id: int, db: Session = Depends(get_db)):
    
    role = db.query(models.Roles).filter(models.Roles.rid == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found!")
    return role

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RoleResponse)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    new_role = models.Roles(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(id: int, db: Session = Depends(get_db)):
    role_query = db.query(models.Roles).filter(models.Roles.rid == id)
    role = role_query.first()
    if role == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found!")
    # role tb is never accessible for non admin employees
    role_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.RoleResponse)
def update_role(id: int, new_role: schemas.RoleCreate, db: Session = Depends(get_db)):
    role_query = db.query(models.Roles).filter(models.Roles.rid == id)
    role = role_query.first()
    if role == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {id} not found!")
    role_query.update(new_role.dict(), synchronize_session=False)
    db.commit()
    return role_query.first()