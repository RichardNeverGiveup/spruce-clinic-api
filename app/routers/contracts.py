from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..import models, schemas
router = APIRouter(
    prefix='/contracts',
    tags=['contracts']
)

@router.get("/") # get all contracts
def get_contracts(db: Session = Depends(get_db)):
    contracts = db.query(models.Contracts).all()
    return contracts

@router.get("/{id}") # get one single contract
def get_contract(id: int, db: Session = Depends(get_db)):
    
    contract = db.query(models.Contracts).filter(models.Contracts.cid == id).first()
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract with id {id} not found!")
    return contract

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ContractResponse)
def create_contract(contract: schemas.ContractCreate, db: Session = Depends(get_db)):
    new_contract = models.Contracts(**contract.dict())
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(id: int, db: Session = Depends(get_db)):
    contract_query = db.query(models.Contracts).filter(models.Contracts.cid == id)
    contract = contract_query.first()
    if contract == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract with id {id} not found!")
    # role tb is never accessible for non admin employees
    contract_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ContractResponse)
def update_contract(id: int, new_role: schemas.ContractCreate, db: Session = Depends(get_db)):
    contract_query = db.query(models.Contracts).filter(models.Contracts.cid == id)
    contract = contract_query.first()
    if contract == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract with id {id} not found!")
    contract_query.update(new_role.dict(), synchronize_session=False)
    db.commit()
    return contract_query.first()