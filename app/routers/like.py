
from fastapi import APIRouter, Depends ,HTTPException
from ..schemas import Vote
from ..db import get_db
from sqlalchemy.orm import Session
from ..models import PostModel, User, Like
from oauth2 import get_current_user
router = APIRouter(prefix="/like",TAGS="like")

@router.post("/",status_code=201)
def vote(vote:Vote,db:Session=Depends(get_db),current_user:str=Depends(get_current_user)):
    
    query = db.query(Like).filter(Like.post_id == vote.post_id,Like.user_id==current_user.id)
    try:
        if query.first() and vote.status==1:
            raise HTTPException(status_code=404,detail="you cant like twice")
    
        elif query.first() and vote.status==0:
             liked = query
             liked.delete(synchronize_session=False)
             db.commit()
             return (f'like no {liked.post_id} was deleted')
        
        elif not query.one() and vote.status ==1:
            new_like = Like(current_user.id,vote.post_id)
            db.add(new_like)
            db.commit()
            return new_like
    except : 
        raise HTTPException(status_code = 203)