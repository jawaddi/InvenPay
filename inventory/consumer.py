from main import redis,Product
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key,group)
except:
    print("Group already exists!")

while True:
    try:
        results = redis.xreadgroup(group,key,{key:'>'},None)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Product.get(obj["product_id"])
                #print(obj)
                product.quantity = product.quantity - int(obj['quantity'])
                print(product)
                product.save()
    except Exception as exception:
        print(exception)
    
    time.sleep(1)
    

