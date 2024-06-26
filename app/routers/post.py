from multiprocessing import synchronize
from fastapi import APIRouter
from typing_extensions import deprecated
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from .. import models, utils, schemas
from typing import Optional, List, Union
from ..db import get_db 
from sqlalchemy.orm import Session
from .. import oauth2 
from sqlalchemy.exc import MultipleResultsFound, NoResultFound




router = APIRouter(prefix="/posts",tags=["POSTS"])

@router.get('/', response_model = List[schemas.PostResponse])
def get_post(db:Session=Depends(get_db),current_user:str=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:str="") :
    
    try:
         
        posts = db.query(models.PostModel).filter(models.PostModel.user_id==current_user.id)
        
        return posts
    except:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="post not found sir")


@router.get('/one', response_model = List[schemas.PostResponse])
def posts(db:Session = Depends(get_db), limit:int=10, skip:int=0, search:str=""):
    
    query = db.query(models.PostModel).filter(models.PostModel.title.contains(search)).limit(limit).offset(skip).all()
    try:

        return query
    
   
    except :
        raise HTTPException(status_code=404,detail="others")



@router.post('/', status_code =status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.Post,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    post.user_id = current_user.id
    new_post = models.PostModel(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{id}')
def put_post(id:int,putt:schemas.Post, db:Session=Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id==id)
    post.update(putt.dict())
    db.commit()

@router.delete('/delete/{id}')
def delete_post(id:int, db:Session=Depends(get_db), token:str = Depends(oauth2.oauth2_schema)):
    post = db.query(models.PostModel).filter(models.PostModel.id==id)
    post.delete(synchronize_session=False)
    db.commit()
    return {f'message no {id} deleted'}   

@router.delete('/{id}')
def delete_post(id:int,db:Session=Depends(get_db),current_user:str=Depends(oauth2.get_current_user)):
    
    post = db.query(models.PostModel).filter(models.PostModel.id==id)
    if current_user.id != post.first().user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="you are not allowed to delete others posts bro")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return {f'post no {id} was deleted successfully'}
    

