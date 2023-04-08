from db import sqlAlch


class TagModel(sqlAlch.Model):
    __tablename__ = "tags"

    id = sqlAlch.Column(sqlAlch.Integer, primary_key=True)
    name = sqlAlch.Column(sqlAlch.String(80), unique=True, nullable=False)

    store_id = sqlAlch.Column(sqlAlch.Integer, sqlAlch.ForeignKey("stores.id"), unique=False, nullable=False)
    store = sqlAlch.relationship("StoreModel", back_populates="tags")
    items = sqlAlch.relationship("ItemModel", back_populates="tags", secondary="items_tags")
