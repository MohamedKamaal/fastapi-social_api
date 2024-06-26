
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth








app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home_page():
 
    

    return {'data':'welcome home'}

