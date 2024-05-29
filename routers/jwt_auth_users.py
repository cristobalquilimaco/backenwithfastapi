from sys import exception
from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "ASJGDJAHSVDajsbjaS126552DHFJ6000288ksaBVSJA"

app = FastAPI() # instancia de la app

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password:str

users_db = {
    "cristobal":{
        "username": "cristobal",
        "full_name": "Cristobal Quilimaco",
        "email": "quilimacox1@gmail.com",
        "disabled": False,
        "password": "$2a$12$ld9MHyPv35sBer5gZ9XguuDIaGX14WnAqyydzQcDnjRbeyGfVERL2",
    },
    "cristobal2":{
        "username": "cristobal",
        "full_name": "Cristobal Jose Quilimaco Lopez",
        "email": "quilimacox2@gmail.com",
        "disabled": True,
        "password": "$2a$12$UBbGAWSUCEcZIViglRg5.eQM552EanprS5BrUgY8fA9bs.TkMS5WC",
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) 


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales invalidos",
                headers={"WWW-Autenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no inactivo",
            headers={"WWW-Autenticate": "Bearer"})

    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario o contraseña inválida")
    
    access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer" }

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user