import os
from flask import Flask
from flask_smorest import Api
from db import db
import models  # noqa: F401

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True  # propagate exception to main app
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"  # API root
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # documentation tool
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    db.init_app(app)

    # @app.before_first_request #NO LONGER REQUIRED IN FLASK_ALCHEMY
    # def create_tables():      #NO LONGER REQUIRED IN FLASK_ALCHEMY
    with app.app_context():
        db.create_all()  # create tables from imported models

    api = Api(app)  # connect the flask_smorest to the app
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app


# @app.get("/store")                              #endpoint #http://127.0.0.1:5000/store
# def get_all_stores():                           #function associated to the endpoint
#     return {"stores": list(stores.values())}


# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     if (
#         "store_id" not in item_data
#         or "name" not in item_data
#         or "price" not in item_data
#     ):
#         abort(400, message= "Bad request. Ensure store_id, name and price are included.")
#     if item_data["store_id"] not in stores:
#         abort(404, message= "Store not found.")
#     for item in items.values():
#         if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
#             abort(400, message=f"Item {item['name']} already exist in the provided store")

#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#     return item, 201
