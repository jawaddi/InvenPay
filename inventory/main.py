from fastapi import FastAPI
from redis_om import get_redis_connection,HashModel

from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from typing import List



ALLOW_ORIGINS = config("CORS_ALLOW_ORIGINS").split(",")
#SERVER_URL = config("SERVER_URL")
#PORT = config("PORT")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=['*'],
    allow_headers=['*']
)

# Configure your Redis connection

redis = get_redis_connection(
    host=config("REDIS_HOST"),
    port=config("REDIS_PORT"),
    password=config("REDIS_PASSWORD"),
    decode_responses=True
)

class Product(HashModel):
    name:str
    price:float
    quantity:int

    
    class Meta:
        database = redis

    

@app.get("/products")
async def all_products():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    # Retrieve the Product instance
    product = Product.get(pk)
    return {
        "id": pk,
        "name": product.name,  # Access the attributes directly
        "price": product.price,
        "quantity": product.quantity
    }


#create one product
@app.post("/products")
async def create(product:Product):
    return product.save()


#create multible products
@app.post("/multiple_products")
async def create_multiple(products: List[Product]):
    # Save all products
    saved_products = [product.save() for product in products]
    return {"message": "Products created", "products": saved_products}

# git product by the pk
@app.get("/products/{pk}")
async def get(pk:str):
    product = Product.get(pk)
    return product

#delete product by the pk
@app.delete("/products/{pk}")
async def delete_product(pk:str):
    return Product.delete(pk)

#edit product by pk
@app.put("/products/{pk}")
async def update_products(pk:str,quantity:int):
    prodcut = Product.get(pk)
    prodcut.quantity = quantity
    return prodcut.save()

