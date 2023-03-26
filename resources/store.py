import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
#from db import stores
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores") #(name, import_name, description_for_API_doc )


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented yet.")        

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        #return {"items": list(stores.values())}
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):

        store = StoreModel(**store_data)
        
        try: #validation are made on the database try insert
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Un magasin avec ce nom existe déjà.")
        except SQLAlchemyError:
            abort(500, message="An error occured while importing the item.")

        return store
    
        # for store in stores.values():
        #     if (store_data["name"] == store["name"]):
        #         abort(400, message=f"Store {store['name']} already exist")           
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id }
        # stores[store_id] = store
