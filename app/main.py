from fastapi import FastAPI, Depends, HTTPException, WebSocket, BackgroundTasks, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from . import models, schemas, auth, database, tasks
from .auth import authenticate_user, create_access_token, get_password_hash, get_user_by_email
from .database import get_db
from fastapi import WebSocket

from app.routes import task_routes 
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(task_routes.router) 

@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API!"}

#  User Registration
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User Login 
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

#  Include task routes (CRUD + background email tasks)
app.include_router(tasks.router)

#  Real-Time WebSocket for Task Updates
@app.websocket("/ws/{user_id}")
async def websocket_route(websocket: WebSocket, user_id: str):
    """WebSocket route for real-time updates."""
    await websocket_endpoint(websocket, user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
