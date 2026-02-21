"""AI Travel Guardian+ — Authentication API (JWT-based)"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt

from config import settings
from database.database import SessionLocal, get_db
from database.models import User
from database.schemas import UserRegister, UserLogin, UserResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister, db=Depends(get_db)):
    existing = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token({"sub": str(db_user.id), "username": db_user.username})
    return UserResponse(user_id=db_user.id, username=db_user.username, access_token=token)


@router.post("/login", response_model=UserResponse)
async def login(creds: UserLogin, db=Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not pwd_context.verify(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "username": user.username})
    return UserResponse(user_id=user.id, username=user.username, access_token=token)
