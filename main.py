from fastapi import FastAPI # EN  main.py importar fast api 
from routers import products, users, jwt_auth_users,basic_auth_users 
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers

app.include_router(products.router)
app.include_router(users.router)
##app.include_router(basic_auth_users.router)
##app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():  #Siempre que llamamos a un servidor la peticion debe ser asincrona
    return "Hola mundo prueba"

@app.get("/url")
async def url():  
    return { "url":"http://donhoster.com" }
