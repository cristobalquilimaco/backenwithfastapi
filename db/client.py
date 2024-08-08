"""# Encargado de gestionar la conexion de la base de datos 
from pymongo import MongoClient

db_client = MongoClient().local # --> Puede recibir muchos parametros

"""

import mysql.connector

db_client = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "users_db",
    port = "3306"
)

print(db_client)