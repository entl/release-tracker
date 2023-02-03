from dotenv import load_dotenv
from os import getenv

load_dotenv()

CREDENTIALS = {
    "CLIENT_ID":getenv("client_id"), 
    "CLIENT_SECRET": getenv("client_secret"), 
    "SCOPE":"user-top-read, user-follow-read, user-library-read",
    "REDIRECT_URI": "https://google.com"
    }
6