from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .config import settings
from .routers import employees, roles, contracts, patients, appointments, auth


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

@app.get("/hiddenroute")
def hidden():
    return {"data": "This is a test for CI/CD with github actions v0.2"}

app.include_router(employees.router)
app.include_router(roles.router)
app.include_router(contracts.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(auth.router)
