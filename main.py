from fastapi import FastAPI
import models
from database import engine
from routers import uuid_router
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(uuid_router.router)
