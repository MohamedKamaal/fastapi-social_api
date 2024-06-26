
from sqlalchemy import Boolean,TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from .db import Base


class PostModel(Base):
    __tablename__ ='posts'
    id = Column(Integer,primary_key=True, nullable=False)
    title = Column(String)
    content = Column(String)
    created_at = Column(TIMESTAMP,nullable=False,server_default=text('now()'))
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    time = Column(TIMESTAMP(timezone = True), nullable=False,server_default=text('now()'))



class Like(Base):
    __tablename__ = "like"
    user_id = Column(Integer,  ForeignKey("users.id",ondelete="CASCADE") ,primary_key=True)
    post_id = Column(Integer,  ForeignKey("posts.id",ondelete="CASCADE") ,primary_key=True)