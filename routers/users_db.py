### Users DB API ###


from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel

router = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={404:{"messaje":"NO existe"}}
                    )



class User(BaseModel): 
    id: int
    name: str
    lastname: str
    email: str
    age: int

users_list = [User(id=1, name="Cristobal", lastname="Quilimaco", email="quilimacox1@gmail.com", age=29),
                User(id=2,name="Barbara", lastname="Cordova", email="brb.cordova@gmail.com", age=31),
                User(id=3,name="Justin", lastname="Lastame", email="bieber@gmail.com", age=29)]


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


@router.post("/", status_code=201) 
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El suario ya existe")
   
    
    users_list.append(user)
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