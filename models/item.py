from db import sqlAlch


class ItemModel(sqlAlch.Model):
    __tablename__ = "items"

    id = sqlAlch.Column(sqlAlch.Integer, primary_key=True)
    name = sqlAlch.Column(sqlAlch.String(80), unique=False, nullable=False)
    price = sqlAlch.Column(sqlAlch.Float(precision=2), unique=False, nullable=False)
    store_id = sqlAlch.Column(sqlAlch.Integer, sqlAlch.ForeignKey("stores.id"), unique=False, nullable=False)
    store = sqlAlch.relationship("StoreModel", back_populates="items")
    tags = sqlAlch.relationship("TagModel", back_populates="items", secondary="items_tags")
