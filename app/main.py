from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .config import settings
from . import models
# from .routers import post, user, auth


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"data": "hello clinic"}