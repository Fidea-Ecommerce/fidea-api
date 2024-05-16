from flask import Blueprint, jsonify
from email_validator import validate_email, EmailNotValidError

email_router = Blueprint("api email", __name__)


@email_router.get("/fidea/v1/user/email-validator/<string:email>")
async def email_validator(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
    except EmailNotValidError as e:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"email not valid {email!r}",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"email is valid {email!r}",
                }
            ),
            200,
        )
