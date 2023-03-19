import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if ("name" not in store_data):
        abort(400, message= "Bad request. Ensure name is included.")
    for store in stores.values():
        if (store_data["name"] == store["name"]):
            abort(400, message=f"Store {store['name']} already exist")
        
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id }
    stores[store_id] = store
    return store, 201


@app.get("/store")                              #endpoint #http://127.0.0.1:5000/store
def get_all_stores():                           #function associated to the endpoint
    return {"stores": list(stores.values())}



@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "store_id" not in item_data
        or "name" not in item_data
        or "price" not in item_data
    ):
        abort(400, message= "Bad request. Ensure store_id, name and price are included.")
    if item_data["store_id"] not in stores:
        abort(404, message= "Store not found.")
    for item in items.values():
        if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
            abort(400, message=f"Item {item['name']} already exist in the provided store")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id: str):
    try:
        return items[item_id]
    except KeyError:    
        abort(404, message= "Item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id: str):
    item_data = request.get_json()
    if not(set(("price","name")).issubset(set(item_data))):
        abort(404, message="Bad request. Ensure name and price are included.")
    try:
        item = items[item_id]
        item |= item_data       #in-place merge-right (update) operator, equivalent to d1.update(d2), here item.update(item_data)
        return item
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/item/<string:item_id>")
def delete_item(item_id: str):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found")
