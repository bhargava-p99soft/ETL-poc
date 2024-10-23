from dotenv import load_dotenv

load_dotenv() 
from os import getenv


db_config = {
    "user": getenv("user"),
    "password": getenv("password"),
    "account": getenv("account")
}