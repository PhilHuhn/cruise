# main.py
from fastapi import FastAPI, Depends, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import Base, engine, SessionLocal, RSVP

import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class RSVPRequest(BaseModel):
    name: str
    email: EmailStr
    attending: bool
    bringing_food: bool
    bringing_drink: bool
    message: str


@app.post("/rsvp/")
def create_rsvp(
        rsvp_request: RSVPRequest,
        db: Session = Depends(get_db)
):
    rsvp_entry = RSVP(
        name=rsvp_request.name,
        email=rsvp_request.email,
        attending=rsvp_request.attending,
        bringing_food=rsvp_request.bringing_food,
        bringing_drink=rsvp_request.bringing_drink,
        message=rsvp_request.message
    )
    try:
        db.add(rsvp_entry)
        db.commit()
        db.refresh(rsvp_entry)
        return {
            "success": True,
            "message": "RSVP received! See you aboard!"
        }

    except IntegrityError:
        db.rollback()
        return {
            "success": False,
            "message": "This email is already aboard! Please use a different email or update your existing RSVP."
        }
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="127.0.0.1", port=8000)
