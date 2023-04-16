from jose import JWSError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  #依赖注入，没登录就会转到这个登录的函数

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

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #decode
        # print("*********************", payload)
        id = payload.get("id") # get id from decoded content
        role_id=payload.get("role_id") # get role_id
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, role_id=role_id)
    except JWSError:
        raise credentials_exception
    return token_data  

def get_current_employee(token: str = Depends(oauth2_scheme)):
    #return the id and role_id of current employee
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials of employee", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)

def verify_access_token_p(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        pid = payload.get("id")
        if pid is None:
            raise credentials_exception
        token_data = schemas.TokenDataPatient(pid=pid)
    except JWSError:
        raise credentials_exception
    return token_data  

def get_current_patient(token: str = Depends(oauth2_scheme)):
    #return the pid of current patient
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials of patient", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token_p(token, credentials_exception)