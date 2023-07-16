import sys
sys.path.append("..")
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi.responses import HTMLResponse
from uuid import uuid1
import models
from pydantic import BaseModel

router = APIRouter(
    prefix='/uuid',
    tags=['uuid'],
    responses={404: {'description': 'Not Found'}}
)

models.Base.metadata.create_all(bind=engine)


class EntryCreate(BaseModel):
    text: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/new")
async def create_new_entry(entry_create: EntryCreate, db: Session = Depends(get_db)):
    if not entry_create.text:
        raise HTTPException(
            status_code=400, detail="Поле 'text' не может быть пустым")
    model_entry = models.Entry()
    model_entry.uuid = str(uuid1())
    model_entry.text = entry_create.text
    db.add(model_entry)
    db.commit()

    return successful_response(200)


@router.get("/all")
async def get_all_entries(db: Session = Depends(get_db)):

    return db.query(models.Entry).all()


@router.get("/{uuid}")
async def get_entry_by_uuid(uuid: str, db: Session = Depends(get_db)):
    entry_model = db.query(models.Entry).filter(
        models.Entry.uuid == uuid).first()

    if not entry_model:
        raise HTTPException(status_code=404, detail='Not Found')

    return entry_model


@router.get("/count/{count}")
async def get_entry_by_count(count: int, db: Session = Depends(get_db)):
    entry_models = db.query(models.Entry).limit(count).all()
    print(entry_models)
    if not entry_models:
        raise HTTPException(status_code=404, detail="Not Found")
    return entry_models


@router.delete("/{uuid}")
async def delete_entry_by_uuid(uuid: str, db: Session = Depends(get_db)):
    entry_model = db.query(models.Entry).filter(
        models.Entry.uuid == uuid).first()
    if not entry_model:
        raise HTTPException(status_code=404, detail='Not Found')

    db.query(models.Entry).filter(models.Entry.uuid == uuid).delete()
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }
