from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta


from app.db.base import SessionLocal
from app.db.users import User
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from app.api.schemas.auth_schemas import Token
from app.api.schemas.user_schemas import UserCreate, UserCreateResponse



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password, user.password_salt):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # set last login time
    user.last_login = datetime.now(timezone.utc)

    db.commit()

    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=UserCreateResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Add user existence check
    if db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first():
        raise HTTPException(status_code=400, detail="Username/Email already registered")
    # Hash password before storage
    user = User(
        username=user_data.username, 
        hashed_password=user_data.password,  # Plain password, will be hashed in User.__init__
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserCreateResponse(username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name)