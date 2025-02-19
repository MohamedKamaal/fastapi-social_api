from fastapi import Depends, status, HTTPException
from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas,db,models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings
   

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try : 
        payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
        id:int = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(db.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail='couldnt validate credentials',headers= {"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    user =db.query(models.User).filter(models.User.id==token.id).first()
    return user