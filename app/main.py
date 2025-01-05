from fastapi import FastAPI
from app.api import auth
from app.db.base import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["auth"])