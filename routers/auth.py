from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Literal
from starlette import status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional, Dict
import re
from jose import JWTError, jwt
from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)


def validate_password(password: str) -> bool:
    """
    Validate the given password against a regular expression pattern.

    Parameters:
    password (str): The password to be validated.

    Returns:
    bool: True if the password matches the pattern, False otherwise.
    """
    reg_expn = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,20}$"
    if re.match(reg_expn, password):
        return True
    else:
        return False


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)



SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oath2_bearer = OAuth2PasswordBearer(tokenUrl='auth/access-token')


def get_current_user(token: str = Depends(oath2_bearer), db: Session = Depends(get_db)) -> Optional[dict]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.userName == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    return {"id": user.id, "username": user.userName}




class CreateUserRequest(BaseModel):
    userName: str
    fullName: Optional[str] = None
    email: str
    hashedPassword: str
    DoB: Optional[str] = None
    gender: Optional[Literal['male', 'female', 'NOT_SPECIFIED']] = Field(default='NOT_SPECIFIED')



def authenticate_user(username: str, password: str, db):
    """
    A function to authenticate a user by checking the provided username and password against the database.

    Parameters:
    - username (str): The username of the user trying to authenticate.
    - password (str): The password of the user trying to authenticate.
    - db: The database object used to query user information.

    Returns:
    - False if the user is not found or the password does not match.
    - user: The user object if authentication is successful.
    """
    user = db.query(User).filter(User.userName == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashedPassword):
        return False
    return user


def create_access_token(data: Dict[str, str]) -> str:
    """
    A function that creates an access token.

    Parameters:
    - data: A dictionary containing key-value pairs to be encoded.

    Returns:
    - str: The encoded JWT access token.
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_user(request: Request, create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    """
    A function to create a new user in the database.

    Parameters:
    - create_user_request: An instance of CreateUserRequest containing user information.
    - db: A database session to interact with the database.

    Returns:
    None
    """
    if validate_password(create_user_request.hashedPassword) is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enter valid Password. Password should contain at least 1 uppercase, 1 lowercase, 1 number, 1 special character and should be 8-20 characters long.",
        )
        
    create_user_model = User(
        userName=create_user_request.userName,
        fullName=create_user_request.fullName,
        email=create_user_request.email,
        hashedPassword=bcrypt_context.hash(create_user_request.hashedPassword),
        DoB=create_user_request.DoB,
        gender=create_user_request.gender,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/access-token")
@limiter.limit("5/minute")
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    A description of the entire function, its parameters,
    and its return types.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_dict = user.__dict__
    del user_dict["_sa_instance_state"]
    access_token = create_access_token(data={"sub": user.userName, "id": user.id})
    print(f"the user name is {user.userName}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/access-token")
@limiter.limit("5/minute")
def logout(request: Request):
    """
    A description of the entire function,
    its parameters, and its return types.
    """
    response = HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Successfully logged out",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return response

