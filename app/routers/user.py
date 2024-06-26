from fastapi import APIRouter
from typing_extensions import deprecated
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from .. import models, utils, schemas
from ..db import get_db 
from sqlalchemy.orm import Session

router = APIRouter(prefix ="/users",tags=["USERS"])

@router.post('', response_model=schemas.UserResponse, status_code = status.HTTP_201_CREATED )
def create_user(user : schemas.User, db:Session=Depends(get_db)): 
    user.password= utils.hashed(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete('/{id}')
def delete_user(id:int, db:Session=Depends(get_db)):
    router=db.query(models.User).filter(models.User.id==id)
    router.delete()
    db.commit()
    return {'deleted successfully'}


@router.get('/{id}', response_model = schemas.UserInfo)
def get_user(id:int,db:Session=Depends(get_db)):
    router = db.query(models.User).filter(models.User.id==id).first()
   
    if router is not None :    
        return router 
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="no router found")
        