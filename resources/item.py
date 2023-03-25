import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items") #(name, import_name, description_for_API_doc )


@blp.route("/item/<string:item_id>")
class Store(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= "Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        #item_data = request.get_json()

        # if not(set(("price","name")).issubset(set(item_data))):
        #     abort(404, message="Bad request. Ensure name and price are included.")
        try:
            item = items[item_id]
            item |= item_data       #in-place merge-right (update) operator, equivalent to d1.update(d2), here item.update(item_data)
            return item
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    @blp.arguments(ItemSchema)
    def post(self, item_data):
        #item_data = request.get_json()
        # if not (set(("store_id", "name", "price")).issubset(set(item_data))):
        #     abort(400, message= "Bad request. Ensure store_id, name and price are included.")
        ## if item_data["store_id"] not in stores:
        ##     abort(404, message= "Store not found.")
        for item in items.values():
            if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
                abort(400, message=f"Item {item['name']} already exist in the provided store")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item