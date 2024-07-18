### Users DB API ###


import email
from hmac import new
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.user import User
from db.schemas.user import user_schemas, users_schema
from db.client import db_client

router = APIRouter(prefix="/userdb",
                tags=["userdb"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []


@router.get("/", response_model=list(User)) 
async def users():
    return users_schema(db_client.local.users.find())


#----PATH
@router.get("/{id}")
async def user(id: int):
    return search_user(id)
    

#----QUERY
@router.get("/") 
async def user(id: int):
    return search_user(id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user_by_email(user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El suario ya existe")
    

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schemas(db_client.users.find_one({"_id": id}))

    return User(**new_user)
#------ PUT----- Metodo para actualizar un usuario 

@router.put("/") 
async def user(user: User):

    found = False 

    for index, save__user in enumerate(users_list): 
        if save__user.id == user.id:  
            users_list[index] = user
            found = True
    
    if not found: 
        return {"Error: El usuaro no se puede actualizar"}
    

#-------------------DELETE-------   
@router.delete("/{id}")
async def delete_user(id: int): 
    found = False      

    for index, user in enumerate(users_list): 
        if user.id == id:  
            del users_list[index] 
            found = True

    if not found:
        return {"Error: El usuario no se encontró"}



def search_user(field: str, key:str):
    try:
        user = db_client.users.find_one({"email": email})
        return User(**user_schemas(user))
    except:
        return {"Usuario duplicado"}
    

def search_user(id: int):
    return ""