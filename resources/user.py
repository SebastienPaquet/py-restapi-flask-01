from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

# exc means exception, SQLAlchemyError is the base SQLAlchemy Error class that all exceptions inherits from
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import sqlAlch
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")
# (name, import_name, description_for_API_doc )


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]))

        try:
            sqlAlch.session.add(user)
            sqlAlch.session.commit()
        except IntegrityError:
            abort(500, message="Utilisateur non créé, ce nom d'utilisateur est non-disponible.")
        except SQLAlchemyError:
            abort(500, message="Utilisateur non créé, une erreur est survenue lors de la création de l'utilisateur.")
        return {"message": "Utilisateur créé avec succès."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        sqlAlch.session.delete(user)
        sqlAlch.session.commit()
        return {"message": "Utilisateur supprimé."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"],
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            # le user_id est inscrit dans le JWT payload "sub" (subject)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            # JWT must be private and safe, anybody with the JWT can impersonate the user

        abort(401, message="Identifiants invalides.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        # returns dict of the payload of jwt, and then the jti value which is the jwt identifier
        BLOCKLIST.add(jti)
        # blocklist should be saved in a database..
        # ..or in Redis commonly used fot this sort of thing
        return {"message": "Déconnexion réussie."}


@blp.route("/refresh")
class UserProvideNonFreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user_jti = get_jwt_identity()  # as #jti = get_jwt()["jti"]
        new_token = create_access_token(identity=current_user_jti, fresh=False)
        # can set expiration time of refresh token
        return {"access_token": new_token}
