from jose import jwt, JWTError
from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from schemas.authSchema import (
    Register, RegisteredUser, SignInData, SignInResponse
    )
from models.register import UserRegister
from database.config import config

router=APIRouter(prefix="/auth")

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/sign-in/"
)


SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)


@router.post("/register/", response_model=RegisteredUser)
async def signUp(data: Register):
    """Registers a new user in DB"""

    data.password = ctx.hash(data.password)
    new_user = await UserRegister.create(
        **data.dict()
    )
    return new_user


@router.post("/sign-in/", response_model=SignInResponse)
async def signIn(data: SignInData):
    """Logs in a user using valid credentials"""

    # Fetch user from DB using email
    user = await UserRegister.get_or_none(email=data.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist!"
        )

    # Checks if provided password is valid
    valid_password = ctx.verify(data.password, user.password)
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="access denied, invalid credentials"
        )

    # jwt payload
    jwt_data = {
        "user_id": str(user.id),
        "expire": str(datetime.now(timezone.utc) + timedelta(days=14))
    }
    
    # jwt token generation
    jwt_token = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
    return SignInResponse(message="Sign in successful", token=jwt_token)


@router.get("/user/", response_model=RegisteredUser)
async def decode_jwtToken_and_fetch_user(jwt_token: str = Depends(oauth2_scheme)):
    """Decodes JWT tokeen and fetches associated user"""

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodes token
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        expire = payload.get("expire")
        if user_id is None or expire is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    
    # Check token expiration
    if str(datetime.now(timezone.utc)) > expire:
        raise HTTPException(
            status_code=401,
            detail="Token expired! Please login.",
        )

    # Fetches associated user from db
    user = await UserRegister.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or does not exist."
        )

    return user