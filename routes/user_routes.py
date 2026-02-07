from db import get_db
from fastapi import APIRouter
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepo
from fastapi import Depends
from schemas.user_schema import UserSchema


router = APIRouter()

@router.post("/signup")
def signup(db: Session = Depends(get_db)):
    user_repo=UserRepo(db)
    user_repo.add_user()
    return {"message": "user signed up successfully"}

@router.post("/login")
def login():
    return {"message": "user logged in successfully"}
