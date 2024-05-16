from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.environ.get("DB_URL")
debug_mode = os.environ.get("DEBUG_MODE")
jwt_key = os.environ.get("JWT_KEY")
algorithm = os.environ.get("ALGORITHM")
reset_password_key = os.environ.get("RESET_PASSWORD_KEY")
smtp_password = os.environ.get("SMTP_PASSWORD")
smtp_email = os.environ.get("SMTP_EMAIL")
smtp_port = os.environ.get("SMTP_PORT")
smtp_server = os.environ.get("SMTP_SERVER")
api_url = os.environ.get("API_URL")
fidea_url = os.environ.get("FIDEA_URL")
account_active_key = os.environ.get("ACCOUNT_ACTIVE_KEY")
