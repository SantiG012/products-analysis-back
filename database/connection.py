import os
from pymongo import MongoClient

DATABASE_NAME = "project_db"
COLLECTION_NAME = "products"


def _get_connection_string()->str:
    return os.getenv("CONNECTION_STRING")

def _get_client_with(connection_string:str)->MongoClient:
    return MongoClient(connection_string)

def _connect_to_mongo()->MongoClient:
    connection_string = _get_connection_string()
    client = _get_client_with(connection_string)
    return client

async def fetch_products():
    client = _connect_to_mongo()
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    return await collection.find({})