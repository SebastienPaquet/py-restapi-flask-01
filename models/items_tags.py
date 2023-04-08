from db import sqlAlch


class ItemsTagsModel(sqlAlch.Model):
    __tablename__ = "items_tags"

    id = sqlAlch.Column(sqlAlch.Integer, primary_key=True)
    item_id = sqlAlch.Column(sqlAlch.Integer, sqlAlch.ForeignKey("items.id"))
    tag_id = sqlAlch.Column(sqlAlch.Integer, sqlAlch.ForeignKey("tags.id"))
