from fastapi import Depends, APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2, OAuth2PasswordBearer , OAuth2PasswordRequestForm


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel): 
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    
users_db = {
    "cristobal": {
        "username": "cristobal",
        "full_name": "Cristobal Quilimaco",
        "email": "quilimacox1@gmail.com",
        "disabled": False,
        "password": "123456",
    },
        "cristobal2": {
        "username": "cristobal2",
        "full_name": "Cristobal Quilimaco 2",
        "email": "quilimacox2@gmail.com",
        "disabled": True,
        "password": "1234567",
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidos",
            headers={"WWW-Autenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no inactivo",
            headers={"WWW-Autenticate": "Bearer"})

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    users_db.get(form.username)
    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario o contraseña invalido")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user