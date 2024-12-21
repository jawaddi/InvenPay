from main import redis,Order
import time

key = 'refund_order'
group = 'payment-group'

try:
    redis.xgroup_create(key,group)
except:
    print("Group already exists!")

while True:
    try:
        results = redis.xreadgroup(group,key,{key:'>'},None)
        if results != []:
            print(results)
            for result in results:
                print("here")
                obj = result[1][0][1]
                order = Order.get(obj["pk"])
                order.status = 'refunded'
                order.save()
                
    except Exception as exception:
        print(exception)
    
    time.sleep(1)
    

