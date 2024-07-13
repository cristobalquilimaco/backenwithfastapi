### Users DB API ###


from hmac import new
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.user import User
from db.client import db_client

router = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND:{"messaje":"NO existe"}}
                    )


users_list = []


@router.get("/") 
async def users():
    return users_list


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
    """if type(search_user(user.id)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El suario ya existe")"""
    
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = db_client.local.users.find_one({"_id":id})

    return user
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



def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}
    

    