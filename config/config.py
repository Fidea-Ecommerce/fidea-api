from dotenv import load_dotenv
import os

load_dotenv()

database_fidea_url = os.environ.get("DATABASE_FIDEA_URL")
database_limiter_url = os.environ.get("DATABASE_LIMITER_URL")
debug_mode = os.environ.get("DEBUG_MODE")
access_token_key = os.environ.get("ACCESS_TOKEN_KEY")
refresh_token_key = os.environ.get("REFRESH_TOKEN_KEY")
algorithm = os.environ.get("ALGORITHM")
reset_password_key = os.environ.get("RESET_PASSWORD_KEY")
smtp_password = os.environ.get("SMTP_PASSWORD")
smtp_email = os.environ.get("SMTP_EMAIL")
smtp_port = os.environ.get("SMTP_PORT")
smtp_server = os.environ.get("SMTP_SERVER")
api_url = os.environ.get("API_URL")
fidea_url = os.environ.get("FIDEA_URL")
account_active_key = os.environ.get("ACCOUNT_ACTIVE_KEY")
default_limiter = os.environ.get("DEFAULT_LIMITER")
refresh_token_limiter = os.environ.get("REFRESH_TOKEN_LIMITER")
