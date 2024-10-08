
def user_schema(user) -> dict:
    return{
        "id": user["id"],
        "username": user["username"],
        "email":user["email"],
        "password":user["password"]
    }

def users_schemas(users) -> list:
    return [user_schema(user) for user in users]