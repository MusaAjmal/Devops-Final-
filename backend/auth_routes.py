from fastapi import APIRouter, status, Depends, HTTPException
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from another_fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

# Router setup
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Create a DB session
session = Session(bind=engine)


@auth_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    """
    ## Sample Hello World route
    Requires a valid JWT access token.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    return {"message": "Hello World"}


# ---------- SIGNUP ----------
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    """
    ## Create a new user
    Requires:
    - username: str
    - email: str
    - password: str
    - is_staff: bool
    - is_active: bool
    """

    # Check for existing email
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Check for existing username
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    # Create and save new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Ensures the object has an ID and latest state

    return jsonable_encoder(new_user)


# ---------- LOGIN ----------
@auth_router.post("/login", status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    """
    ## Login a user
    Requires:
    - username: str
    - password: str
    Returns access and refresh tokens.
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {"access": access_token, "refresh": refresh_token}

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password"
    )


# ---------- REFRESH TOKEN ----------
@auth_router.get("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    """
    ## Generate a new access token
    Requires a valid refresh token.
    """
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token",
        )

    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})
