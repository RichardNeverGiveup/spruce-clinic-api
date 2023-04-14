from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .config import settings
from .routers import employees, roles


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
    return {"data": "welcome to spruce clinic api"}

app.include_router(employees.router)
app.include_router(roles.router)