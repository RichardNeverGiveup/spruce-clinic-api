from jose import JWSError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .config import settings

oauth2_scheme_employee = OAuth2PasswordBearer(tokenUrl='login/employee')  #依赖注入，没登录就会转到这个登录的函数
oauth2_scheme_patient = OAuth2PasswordBearer(tokenUrl='login/patient')  #依赖注入，没登录就会转到这个登录的函数

# screte key, algo, expriation time
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 
def get_current_employee(token: str = Depends(oauth2_scheme_employee)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "employee":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"This Api is Employee Only", headers={"WWW-Authenticate": "Bearer"})
        id = payload.get("id") # get id from decoded content
        role_id=payload.get("role_id") # get role_id
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials of employee", headers={"WWW-Authenticate": "Bearer"})
        token_data = schemas.TokenDataEmployee(id=id, role_id=role_id)
    except JWSError as e:
        raise e
    return token_data 

def get_current_patient(token: str = Depends(oauth2_scheme_patient)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "patient":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"This Api is Patient Only", headers={"WWW-Authenticate": "Bearer"})
        pid = payload.get("pid")
        if pid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials of patient", headers={"WWW-Authenticate": "Bearer"})
        token_data = schemas.TokenDataPatient(pid=pid)
    except JWSError as e:
        raise e
    return token_data 