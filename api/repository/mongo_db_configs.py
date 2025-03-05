from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

mongo_db_infos = {
    "HOST": os.getenv("MONGO_HOST"),
    "PASSWORD": quote_plus(os.getenv("MONGO_PASSWORD")),
    "USERNAME": quote_plus(os.getenv("MONGO_USERNAME")),
    "DB_NAME": os.getenv("MONGO_DB_NAME")
}
