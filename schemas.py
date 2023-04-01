# marshmallow schemas
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Integer(dump_only=True)  # when returning data only
    name = fields.Str(required=True)  # must be in incoming json and outgoing response
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()  # optional
    price = fields.Float()  # optional
    store_id = fields.Integer()  # optional


class ItemSchema(PlainItemSchema):
    store_id = fields.Integer(required=True, load_only=True)  # must be in incoming json only
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Integer(load_only=True)  # removing required=True, why ?
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
