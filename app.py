from flask import Flask, request
from db import items, stores

app = Flask(__name__)

@app.get("/store")      #endpoint #http://127.0.0.1:5000/store
def get_stores():       #function associated to the endpoint
    return {"stores": stores}

@app.get("/store/<string:storename>")
def get_store(storename: str):
    for store in stores:
        if store["name"] == storename:
            return store                #already a dictionary so Flask will turn it in JSON
    return {"message": "Store not found"}, 404

@app.get("/store/<string:storename>/item")
def get_store_items(storename: str):
    for store in stores:
        if store["name"] == storename:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404

@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201

@app.post("/store/<string:storename>/item")
def create_item(storename: str):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == storename:
            new_item = {
                            "name": request_data["name"],
                            "price": request_data["price"]
                            # "name": request_data["items"]["name"], 
                            # "price": request_data["items"]["price"]
                        }
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404
            