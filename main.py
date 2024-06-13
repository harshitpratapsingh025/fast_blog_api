from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users
from db.database import engine
from db.models import users_model
import sqlalchemy


users_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
