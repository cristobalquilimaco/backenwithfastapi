def user_schemas(user) -> dict:
    return{"id": user["_id"],
           "username": user["username"],
           "email": user["email"]}

    _id: str | None
    username: str
    email: str