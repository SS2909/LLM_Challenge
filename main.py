from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os, shutil
from . import db, models, schemas, auth, ingest, rag

app = FastAPI()
models.Base.metadata.create_all(bind=db.engine)

def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post('/register', response_model=schemas.Token)
def register(user: schemas.UserCreate, session: Session = Depends(get_db)):
    existing = session.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(400, 'User already exists')
    hashed = auth.hash_password(user.password)
    u = models.User(email=user.email, hashed_password=hashed)
    session.add(u)
    session.commit()
    session.refresh(u)
    token = auth.create_access_token({'sub': u.email, 'user_id': u.id})
    return {'access_token': token}

@app.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = session.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, 'Incorrect username or password')
    token = auth.create_access_token({'sub': user.email, 'user_id': user.id})
    return {'access_token': token}

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    os.makedirs('./uploads', exist_ok=True)
    save_path = f'./uploads/{file.filename}'
    with open(save_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    chunks = ingest.ingest_file(save_path)
    return {'status': 'ingested', 'chunks': chunks}

@app.post('/chat')
def chat(msg: schemas.MessageIn):
    answer = rag.query_rag(msg.message)
    return {'answer': answer}
