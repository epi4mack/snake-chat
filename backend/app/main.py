from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session
from app.models import Base, Message, get_db, engine
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()


class MessageCreate(BaseModel):
    name: str
    text: str


@app.get("/")
def read_root():
    return {"message": "SnakeChat v1.0"}


@app.get("/messages/")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).all()


@app.get("/messages/{username}/")
def get_messages_by_user(username: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.name == username).all()

    html_content = ""
    for msg in messages:
        html_content += f"<b>{msg.name}:</b> {msg.text}<br>"

    return Response(content=html_content, media_type="text/html")


@app.post("/messages/")
def post_message(msg: MessageCreate, db: Session = Depends(get_db)):
    message = Message(name=msg.name, text=msg.text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
