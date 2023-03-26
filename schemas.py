#marshmallow schemas
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Integer(dump_only=True)     #when returning data only
    name = fields.Str(required=True)        #must be in incoming json and outgoing response
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)     #when returning data only
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()         #optional
    price = fields.Float()      #optional
    store_id = fields.Integer() #optional

class ItemSchema(PlainItemSchema):
    store_id = fields.Integer(required=True, load_only=True)    #must be in incoming json only
    store = fields.Nested(PlainStoreSchema(), dump_only=True)   #when returning data only

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)   #when returning data only
