from fastapi import FastAPI
from users import model as user_model, router as user_router

from users import *

from configs.database import engine
from auth import auth_router

app= FastAPI()

@app.on_event("startup")
def create_tables():
    print("Creating tables")
    user_model.Base.metadata.create_all(bind=engine)


app.include_router(user_router.router)
app.include_router(auth_router.router)