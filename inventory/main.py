from fastapi import FastAPI
from redis_om import get_redis_connection,HashModel

from fastapi.middleware.cors import CORSMiddleware
from pydantic import  ConfigDict




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Configure your Redis connection
redis = get_redis_connection(
    host="redis-19806.c9.us-east-1-2.ec2.redns.redis-cloud.com",  # Redis server host
    port=19806,         # Redis server port
    password='LJojabkowutc2Eb3Dm4yye6bSjo1npTn',     # Redis password if required
    decode_responses=True  # Decode responses into strings
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


@app.post("/products")
async def create(product:Product):
    return product.save()


@app.get("/products/{pk}")
async def get(pk:str):
    product = Product.get(pk)
    return product

@app.delete("/products/{pk}")
async def delete_product(pk:str):
    return Product.delete(pk)

@app.put("/products/{pk}")
async def update_products(pk:str,quantity:int):
    prodcut = Product.get(pk)
    prodcut.quantity = quantity
    return prodcut.save()

