from typing import Annotated

from ..database import SessionLocal
from fastapi import Depends, HTTPException, APIRouter
from ..models import Todos
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from .auth import get_current_user
from ..models import Users

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str
    is_active: bool
    role: str
    phoneNumber: str

class UserRequest(BaseModel):
    password: str
    new_password: str

@router.get('/', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user:user_dependency , db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed!')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    return user_model

@router.post('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, user_request:UserRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed!')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    if not bcrypt_context.verify(user_request.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please enter the correct password.')

    user_model.hashed_password = bcrypt_context.encrypt(user_request.password)
    db.add(user_model)
    db.commit()

@router.put('/phoneNumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number (user:user_dependency, db:db_dependency, phone_number:str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed!')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    user_model.phoneNumber = phone_number
    db.add(user_model)
    db.commit()