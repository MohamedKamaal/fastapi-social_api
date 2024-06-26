from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed(password:str):
    return pwd_context.hash(password)

def verify(password,hashed):
    return pwd_context.verify(password,hashed)