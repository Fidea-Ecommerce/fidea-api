from flask import jsonify


async def handle_429(error):
    return jsonify({"message": "too many requests", "status_code": 429}), 429


async def handle_404(error):
    return jsonify({"message": "endpoint not found", "status_code": 404}), 404


async def handle_415(error):
    return jsonify({"message": "unsupported media type", "status_code": 415}), 415


async def handle_400(error):
    return jsonify({"message": "bad request", "status_code": 400}), 400
