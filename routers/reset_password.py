from flask import Blueprint, render_template, request, jsonify, redirect
from utils import TokenResetPassword
import smtplib
from email.mime.text import MIMEText
from config import (
    smtp_password,
    smtp_email,
    smtp_server,
    smtp_port,
    api_url,
    fidea_url,
)
from databases import UserCRUD, ResetPasswordCRUD
import datetime
from sqlalchemy.exc import IntegrityError
from utils import UserNotFoundError
from flask_bcrypt import Bcrypt

reset_password_router = Blueprint("route reset password", __name__)
user_database = UserCRUD()
token_database = ResetPasswordCRUD()
bcrypt = Bcrypt()


@reset_password_router.route(
    "/fidea/v1/user/reset/reset-password/<string:token>", methods=["POST", "GET"]
)
async def reset_password(token):
    valid_token = await TokenResetPassword.get(token)
    if request.method == "POST":
        user_change_password = await user_database.get(
            "email", email=valid_token["email"]
        )
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        password_error = ""
        confirm_password_error = ""
        if not password.strip():
            password_error = "password is required"
        if not confirm_password.strip():
            confirm_password_error = "confirm password is required"
        if password.strip() != confirm_password.strip():
            password_error = "password do not match"
            confirm_password_error = "password do not match"
        if not password_error and not confirm_password_error:
            hashed_password = bcrypt.generate_password_hash(password.strip()).decode(
                "utf-8"
            )
            try:
                await user_database.update(
                    "password",
                    email=user_change_password.email,
                    password=user_change_password.password,
                    new_password=hashed_password,
                )
                await token_database.delete("user_id", user_id=user_change_password.id)
            except:
                pass
            return redirect(fidea_url)
        return render_template(
            "reset_password.html",
            password_error=password_error,
            confirm_password_error=confirm_password_error,
        )
    if valid_token:
        try:
            user_token_database = await token_database.get(
                "token", user_id=valid_token["user_id"], token=token
            )
        except:
            await token_database.delete("user_id", user_id=valid_token["user_id"])
        else:
            return render_template("reset_password.html")
    return render_template("not_found.html")


@reset_password_router.post("/fidea/v1/user/email-reset-password")
async def email_reset_password():
    data = request.json
    email = data.get("email")
    try:
        user = await user_database.get("email", email=email)
    except UserNotFoundError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {email} not found",
                }
            ),
            404,
        )
    else:
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        expired_at = created_at + (datetime.timedelta(hours=7).total_seconds())
        token = await TokenResetPassword.insert(user.id, email)
        try:
            await token_database.insert(user.id, token, created_at, expired_at)
        except IntegrityError:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"failed send email to {email!r}",
                    }
                ),
                400,
            )
        except Exception:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"bad request",
                    }
                ),
                400,
            )
        else:
            msg = MIMEText(
                f"""<h1>Hi, Welcome {email}</h1>

<p>Di Sini Kami Telah Mengirimkan Anda Untuk Merubah Password Anda: </p>
<a href={api_url}/fidea/v1/user/reset/reset-password/{token}>Click Ini Untuk Reset Password</a>
""",
                "html",
            )
            msg["Subject"] = "Reset Password"
            msg["From"] = smtp_email
            msg["To"] = email
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_email, smtp_password)
                    server.send_message(msg)
                    server.quit()
            except:
                return (
                    jsonify(
                        {
                            "status_code": 400,
                            "message": f"failed send email to {email!r}",
                        }
                    ),
                    400,
                )
            else:
                return (
                    jsonify(
                        {
                            "status_code": 201,
                            "message": f"success send email to {email!r}",
                        }
                    ),
                    201,
                )
