from db import sqlAlch


class UserModel(sqlAlch.Model):
    __tablename__ = "users"

    id = sqlAlch.Column(sqlAlch.Integer, primary_key=True)
    username = sqlAlch.Column(sqlAlch.String(80), unique=True, nullable=False)
    password = sqlAlch.Column(sqlAlch.String(80), nullable=False)
