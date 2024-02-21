from fastapi import APIRouter 

router = APIRouter(prefix="/products",
                    tags=["products"],
                    responses={404:{"message":"Este no esta disponible"}}
                    )

products_list = ["product 1", "product 2", "product 3", "product4", "product 4"]

@router.get("/") #Se define el path 
async def products():
    return products_list

@router.get("/{id}") #Se define el path 
async def products(id: int): # Definir el tipo de dato en este caso entero
    return products_list[id]
        