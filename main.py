from flask import Flask, jsonify
from flask_cors import CORS
from config import debug_mode, database_limiter_url
from databases import db_session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import (
    handle_404,
    handle_415,
    handle_429,
    handle_400,
    handle_401,
    handle_403,
    handle_405,
)
from routers.account_active import account_active_router
from routers.reset_password import reset_password_router
from routers.email import email_router
from routers.product import product_router
from routers.user import user_router
from routers.cart import cart_router
from routers.checkout import checkout_router
from routers.login import login_router
from routers.register import register_router
from routers.wallet import wallet_router
from routers.store import store_router
from routers.favorite import favorite_router
from routers.refresh_token import refresh_token_router

app = Flask(__name__)
CORS(app, supports_credentials=True)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[""],
    storage_uri=database_limiter_url,
    strategy="fixed-window",
)

limiter.limit("20/minute")(product_router)
limiter.limit("20/minute")(user_router)
limiter.limit("20/minute")(cart_router)
limiter.limit("20/minute")(checkout_router)
limiter.limit("20/minute")(reset_password_router)
limiter.limit("20/minute")(account_active_router)
limiter.limit("20/minute")(email_router)
limiter.limit("20/minute")(login_router)
limiter.limit("20/minute")(register_router)
limiter.limit("20/minute")(wallet_router)
limiter.limit("20/minute")(store_router)
limiter.limit("20/minute")(favorite_router)
limiter.limit("1 per 10 minute")(favorite_router)
app.register_blueprint(product_router)
app.register_blueprint(user_router)
app.register_blueprint(cart_router)
app.register_blueprint(checkout_router)
app.register_blueprint(reset_password_router)
app.register_blueprint(account_active_router)
app.register_blueprint(email_router)
app.register_blueprint(login_router)
app.register_blueprint(register_router)
app.register_blueprint(wallet_router)
app.register_blueprint(store_router)
app.register_blueprint(favorite_router)
app.register_blueprint(refresh_token_router)
app.register_error_handler(429, handle_429)
app.register_error_handler(404, handle_404)
app.register_error_handler(415, handle_415)
app.register_error_handler(400, handle_400)
app.register_error_handler(401, handle_401)
app.register_error_handler(403, handle_403)
app.register_error_handler(405, handle_405)


@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Authorization, X-Forwarded-For, User-Agent"
    )
    return response


@app.teardown_appcontext
async def shutdown_session(exception=None):
    db_session.remove()


@app.get("/")
async def home():
    return jsonify("welcome to ecommerce api"), 200


if __name__ == "__main__":
    app.run(debug=debug_mode)
