from fastapi import FastAPI
from redis_om import get_redis_connection,HashModel
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests,time
from decouple import config


ALLOW_ORIGINS = config("CORS_ALLOW_ORIGINS").split(",")
# to communicate with the inventory
SERVER_URL = config("SERVER_URL")
PORT = config("PORT")
print("server = ",SERVER_URL)
print("PORT = ",PORT)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=['*'],
    allow_headers=['*']
)


# the payment database
redis = get_redis_connection(
    host=config("REDIS_HOST"),
    port=config("REDIS_PORT"),
    password=config("REDIS_PASSWORD"),
    decode_responses=True
)

class Order(HashModel):
    product_id:str
    price: float
    fee:float
    total:float
    quantity:int
    status:str #pending completed refunded

    class Meta:
        database=redis


# get order by the pk
@app.get("/order/{pk}")
async def get_order(pk:str):
    return Order.get(pk)


# make an order
@app.post("/orders")

async def create_order(request:Request,background_tasks:BackgroundTasks):#id,quantity
   
    body = await request.json()
    
    
    url = f"{SERVER_URL}:{PORT}/products/%s" % body['id']

    req = requests.get(url)
    product = req.json()
    order = Order(
        product_id=product['pk'],
        price=product['price'],
        fee=round(product['price'] * 0.20,2),
        total= round(product['price']+product['price']*0.20,2),
        quantity=body['quantity'],
        status="pending"
    )
    order.save()
    background_tasks.add_task(order_completed,order)
    
    return order



def order_completed(order:Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    # producer
    redis.xadd("order_completed",order.dict(),"*")