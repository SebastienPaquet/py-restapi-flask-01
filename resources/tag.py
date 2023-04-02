from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema


blp = Blueprint("tags", __name__, description="Operations on tags")
# (name, import_name, description_for_API_doc )


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
        #     abort(400, message="Un tag avec ce nom existe déjà pour ce magasin.")
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Retourné si Suppression du tag puisqu'aucun item associé.",  # documentation purpose
        example={"message": "Tag supprimé."},
    )
    @blp.alt_response(404, description="Retourné si Tag non trouvé.")
    @blp.alt_response(
        400,
        description="Retourné si le tag est associé à au moins un autre article et le tag n'est donc pas supprimé.",
    )
    # alternative responses
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag supprimé."}
        abort(400, message="Tag non supprimé, Validez que le tag n'est pas associé à un article puis réessayez.")


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinksTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store.id != tag.store.id:
            abort(400, message="L'article et le tag doivent être pour le même store.")

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Une erreur est survenue à l'association du tag à l'article.")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store.id != tag.store.id:
            abort(400, message="L'article et le tag doivent être pour le même store.")

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Une erreur est survenue à la déassociation du tag et l'article.")

        return {"message": "Tag désassocié de l'article", "article": item, "tag": tag}
