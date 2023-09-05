from fastapi import FastAPI
app = FastAPI()
auth_app = FastAPI()
from pymongo import MongoClient

jwt_secret = "adnan_tech_com_1234567890"

protocol = "http"
host = "127.0.0.1"
port = 8000
base_url = protocol + "://" + host + ":" + str(port)

MONGO_CONNECTING_STRING = "mongodb://localhost:27017"
client = MongoClient(MONGO_CONNECTING_STRING)
db_name = "py_auth"
db = client[db_name]