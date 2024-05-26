from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta


ALGORITH = "HS256"
ACCESS_TOKEN_DURATION = 1

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

    return {"access_token": access_token, "token_type": "bearer" }

