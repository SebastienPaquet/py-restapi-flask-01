from db import sqlAlch


class StoreModel(sqlAlch.Model):
    __tablename__ = "stores"

    id = sqlAlch.Column(sqlAlch.Integer, primary_key=True)
    name = sqlAlch.Column(sqlAlch.String(80), unique=True, nullable=False)
    items = sqlAlch.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = sqlAlch.relationship("TagModel", back_populates="store", lazy="dynamic")
    # lazy="dynamic": doesn't fetch items until we tell him too
