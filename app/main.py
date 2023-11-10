# Code to demonstrate Synchronous REST Api - with the data stored in JSON file
# Demonstrated for GET, GET ID, POST, PUT AND DELETE HTTP Methods
# URL to run -> http://localhost:8000/docs which opens the Swagger API documentation
# Run Uvicorn - uvicorn main:app --reload

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .services import service
import requests
import os

load_dotenv()

app = FastAPI()
ORDER_BASE_URL = os.getenv('ORDER_BASE_URL')
PRODUCT_BASE_URL = os.getenv('PRODUCT_BASE_URL')
print(ORDER_BASE_URL, PRODUCT_BASE_URL)


class User(BaseModel):
    name: str
    email: str
    address: str
    mobile: int
    
class Order(BaseModel):
    product_price: int
    quantity: int

@app.get('/')
def getAllUsers():
    res = []
    data = service.get_all_customer()
    for i in range(len(data)):
        res.append({'id':data[i][0], 'name':data[i][1], 'email':data[i][2], 'mobile':data[i][3], 'address':data[i][4]})
    return res


@app.get('/users/{id}', status_code=200)
def get_user(id: int):
    try:
        data = service.get_customer(id)
        return {'id':data[0], 'name':data[1], 'email':data[2], 'mobile':data[3], 'address':data[4]}
    except:
        return HTTPException(status_code=404, detail=f"Failed to fetch user with id {id}")



@app.post('/users', status_code=201)
def new_user(userObj: User):
    try:
        new_user = {
            "name" : userObj.name,
            "email" : userObj.email,
            "address" : userObj.address,
            "mobile" : userObj.mobile
        }
        data = service.create_customer(new_user)

        return {'id':data[0], 'name':data[1], 'email':data[2], 'mobile':data[3], 'address':data[4]}
    except:
        return HTTPException(status_code=404, detail=f"User creation failed")


@app.delete('/users/{id}',status_code=200)
def delete_user(id: int):
    try:
        data = service.delete_customer(id);
        return data
    except:
        raise HTTPException(status_code=404, detail=f"There is no User with id as {id}")

@app.put('/users/{id}', status_code=200)
def change_user(id: int, userObj: User):
    try:
        new_user = {
            "name" : userObj.name,
            "email" : userObj.email,
            "address" : userObj.address,
            "mobile" : userObj.mobile
        }
        data = service.update_customer(id, new_user)
        return {'id':data[0], 'name':data[1], 'email':data[2], 'mobile':data[3], 'address':data[4]}
    except:
        return HTTPException(status_code=404, detail=f"User with id {id} does not exist")

@app.post('/order', status_code=200)
def create_order(user_id: int, orderObj: Order ):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        order_data = {
            'user_id': user_id,
            'product_price': orderObj.product_price, 
            'quantity': orderObj.quantity
            }
        
        response = requests.post(f"{ORDER_BASE_URL}/orders",headers=headers, json=order_data)
        if response.status_code != 201:
            return HTTPException(status_code=response.status_code, detail=response.content)
        else:
            return response.json()
        
    except:
        return HTTPException(status_code=404, detail=f"Order failed for id {user_id}. Please try again")
    
@app.get('/products', status_code=200)
def get_all_products():
    try:
        response = requests.get(f"{PRODUCT_BASE_URL}/")
        print(response)
        print(response.content)
        if response.status_code != 200:
            return HTTPException(status_code=response.status_code, detail=response.content)
        else:
            return response.json()
        
    except:
        return HTTPException(status_code=404, detail=f"Product Detials not fetched")