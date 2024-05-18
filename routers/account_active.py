from databases import AccountActiveCRUD, UserCRUD
from flask import Blueprint, jsonify, request, render_template
from utils import AccountActive, UserNotFoundError
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
import datetime
from utils import AccountActive
import traceback
from utils import UserNotFoundError
from sqlalchemy.exc import IntegrityError

account_active_router = Blueprint("api account active", __name__)
account_active_database = AccountActiveCRUD()
user_database = UserCRUD()


@account_active_router.get("/fidea/v1/user/email-verify/<string:token>")
async def account_active(token):
    if valid_token := await AccountActive.get(token):
        try:
            user_token_database = await account_active_database.get(
                "token", user_id=valid_token["user_id"], token=token
            )
        except UserNotFoundError:
            return render_template("not_found.html")
        else:
            if (
                datetime.datetime.now(datetime.timezone.utc).timestamp()
                <= user_token_database.expired_at
            ):
                try:
                    await user_database.update(
                        "is_active",
                        is_active=True,
                        email=valid_token["email"],
                    )
                except:
                    await account_active_database.delete(
                        "user_id", user_id=user_token_database.user_id
                    )
                    return render_template("not_found.html")
                else:
                    await account_active_database.delete(
                        "user_id", user_id=user_token_database.user_id
                    )
                    return render_template("email_active.html", url=fidea_url)
    return render_template("not_found.html")


@account_active_router.post("/fidea/v1/user/email-verify")
async def account_active_email():
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
        if user.is_active:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"user {email!r} is active",
                    }
                ),
                400,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        expired_at = created_at + (datetime.timedelta(hours=7).total_seconds())
        token = await AccountActive.insert(user.id, email)
        try:
            await account_active_database.insert(
                user.id,
                token,
                created_at,
                expired_at,
            )
        except IntegrityError:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "result": f"failed send email to {email!r}",
                    }
                ),
                400,
            )
        except Exception:
            traceback.print_exc()
        else:
            msg = MIMEText(
                f"""<h1>Hi, Welcome {email}</h1>

<p>Di Sini Kami Telah Mengirimkan Anda Untuk Verif Account: </p>
<a href={api_url}/fidea/v1/user/email-verify/{token}>Click Ini Untuk Verify Email</a>
""",
                "html",
            )
            msg["Subject"] = "Verify Email"
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
                            "result": f"failed send email to {email!r}",
                        }
                    ),
                    400,
                )
            else:
                return (
                    jsonify(
                        {
                            "status_code": 201,
                            "result": f"success send email to {email!r}",
                        }
                    ),
                    201,
                )
