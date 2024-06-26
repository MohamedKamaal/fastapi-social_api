from fastapi.security import OAuthPasswordBearer

oauth_scheme = OAuthPasswordBearer(tokenUrl='/login')
