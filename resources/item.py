#import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError  #exc means exception, SQLAlchemyError is the base SQLAlchemy Error class that all exceptions inherits from

#from db import items
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items") #(name, import_name, description_for_API_doc )


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)  #get or abort
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented yet.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(**item_data)       #if not found creates item

        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        #return {"items": list(items.values())}
        #with flask_smorest BluePrint.response(...) it will be returning a list
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        
        try: #validation are made on the database try insert
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Un article avec ce nom existe déjà.")
        except SQLAlchemyError:
            abort(500, message="Une erreur est survenue lors de l'import de cet article.")

        # for item in items.values():
        #     if (    item_data["name"] == item["name"] 
        #             and item_data["store_id"] == item["store_id"]):
        #         abort(400, message=f"Item {item['name']} already exist in the provided store")
        #item_id = uuid.uuid4().hex
        #item = {**item_data, "id": item_id}
        #items[item_id] = item

        return item