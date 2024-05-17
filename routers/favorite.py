from flask import Blueprint, jsonify
from utils import token_required

favorite_router = Blueprint("api favorite item", __name__)


@favorite_router.get("/fidea/v1/user/favorite")
@token_required()
async def add_favorite_item():
    pass
