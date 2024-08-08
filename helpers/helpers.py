from typing import Dict, Any
from db.client import db_client

def search_user(field: str, key: Any) -> Dict[str, Any]:
    cursor = db_client.cursor(dictionary=True)
    query = f"SELECT * FROM users WHERE {field} = %s"
    cursor.execute(query, (key,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return user
    return {"error": "No se ha encontrado el usuario"}
