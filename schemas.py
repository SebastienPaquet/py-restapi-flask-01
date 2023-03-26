#marshmallow schemas
from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True)     #when returning data only
    name = fields.Str(required=True)    #must be in incoming json and outgoing response
    price = fields.Float(required=True)
    store_id = fields.Str(required=True) 


class ItemUpdateSchema(Schema):
    name = fields.Str()         #optional
    price = fields.Float()      #optional


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
