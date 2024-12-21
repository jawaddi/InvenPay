from fastapi import FastAPI
from redis_om import get_redis_connection,HashModel
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests,time




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


# the payment database
redis = get_redis_connection(
    host="redis-19806.c9.us-east-1-2.ec2.redns.redis-cloud.com",  # Redis server host
    port=19806,         # Redis server port
    password='LJojabkowutc2Eb3Dm4yye6bSjo1npTn',     # Redis password if required
    decode_responses=True  # Decode responses into strings
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

@app.get("/order/{pk}")
async def get_order(pk:str):
    return Order.get(pk)



@app.post("/orders")

async def create_order(request:Request,background_tasks:BackgroundTasks):#id,quantity
   
    body = await request.json()
    
    req = requests.get("http://127.0.0.1:8000/products/%s" % body['id'])
    product = req.json()
    order = Order(
        product_id=product['pk'],
        price=product['price'],
        fee=product['price'] * 0.20,
        total= product['price']+product['price']*0.20,
        quantity=body['quantity'],
        status="pending"
    )
    order.save()
    background_tasks.add_task(order_completed,order)
    
    url = f"http://127.0.0.1:8000/products/{body['id']}"
    payload = {"quantity": product['quantity']-body['quantity']}  # Create the body for the PUT request
    response = requests.put(url, params=payload)
    print(response)
    return order

def order_completed(order:Order):
    time.sleep(10)
    order.status = 'completed'
    order.save()