from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    get_current_user,
    get_user_by_email,
    hash_password,
    new_user_id,
    verify_password,
)
from app.db import get_db
from app.models import User
from app.schemas import AuthLoginRequest, AuthRegisterRequest, AuthResponse, AuthUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register(body: AuthRegisterRequest, db: Session = Depends(get_db)):
    email = body.email.lower().strip()
    if get_user_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        id=new_user_id(),
        email=email,
        password_hash=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id, user.email)
    return AuthResponse(access_token=token, user=AuthUser(id=user.id, email=user.email))


@router.post("/login", response_model=AuthResponse)
def login(body: AuthLoginRequest, db: Session = Depends(get_db)):
    email = body.email.lower().strip()
    user = get_user_by_email(db, email)
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(user.id, user.email)
    return AuthResponse(access_token=token, user=AuthUser(id=user.id, email=user.email))


@router.get("/me", response_model=AuthUser)
def me(user: User = Depends(get_current_user)):
    return AuthUser(id=user.id, email=user.email)
