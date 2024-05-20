from flask import jsonify


async def handle_429(error):
    return jsonify({"message": "too many requests", "status_code": 429}), 429


async def handle_404(error):
    return jsonify({"message": "endpoint not found", "status_code": 404}), 404


async def handle_415(error):
    return jsonify({"message": "unsupported media type", "status_code": 415}), 415


async def handle_400(error):
    return jsonify({"message": "bad request", "status_code": 400}), 400


async def handle_401(error):
    return jsonify({"message": "authorization invalid", "status_code": 401}), 401


async def handle_403(error):
    return jsonify({"message": "user invalid", "status_code": 403}), 403


async def handle_405(error):
    return jsonify({"message": "method not allowed", "status_code": 405}), 405
