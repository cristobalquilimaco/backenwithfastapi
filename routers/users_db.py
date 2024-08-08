from fastapi import APIRouter, HTTPException, status
from typing import List
from db.models.user import User
from db.schemas.user import user_schemas, users_schema
from db.client import db_client
from helpers.helpers import search_user

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    cursor = db_client.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")

    user_dict = dict(user)
    user_dict.pop("id", None)  # Elimina la clave 'id' si existe

    columns = ', '.join(user_dict.keys())
    values = ', '.join(['%s'] * len(user_dict))
    sql = f"INSERT INTO users ({columns}) VALUES ({values})"
    cursor.execute(sql, tuple(user_dict.values()))
    db_client.commit()
    new_id = cursor.lastrowid
    cursor.close()

    new_user = search_user("id", new_id)
    return user_schemas(new_user)

@router.get("/", response_model=List[User])
async def users():
    cursor = db_client.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users_schema(users)

@router.get("/{id}", response_model=User)
async def user(id: str):
    user = search_user("id", id)
    if "error" in user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=user["error"])
    return user_schemas(user)

@router.put("/", response_model=User)
async def update_user(user: User):
    user_dict = dict(user)
    user_id = user_dict.pop("id", None)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID del usuario es requerido")

    cursor = db_client.cursor()
    set_clause = ', '.join([f"{key} = %s" for key in user_dict.keys()])
    sql = f"UPDATE users SET {set_clause} WHERE id = %s"
    cursor.execute(sql, tuple(user_dict.values()) + (user_id,))
    db_client.commit()
    cursor.close()

    updated_user = search_user("id", user_id)
    if "error" in updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=updated_user["error"])
    return user_schemas(updated_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    cursor = db_client.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db_client.commit()
    cursor.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha eliminado el usuario")
