# Encargado de gestionar la conexion de la base de datos 
from pymongo import MongoClient

db_client = MongoClient().local # --> Puede recibir muchos parametros

