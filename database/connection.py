import os
from pymongo import MongoClient
from dotenv import load_dotenv

DATABASE_NAME = "project_db"
COLLECTION_NAME = "products"

def _get_connection_string() -> str:
    return os.getenv("CONNECTION_STRING")

def _get_client_with(connection_string: str) -> MongoClient:
    CLIENT = MongoClient(connection_string)
    return CLIENT 

def _connect_to_mongo() -> MongoClient:
    connection_string = _get_connection_string()
    client = _get_client_with(connection_string)
    return client

def _get_database_from(client: MongoClient)->MongoClient:
    return client[DATABASE_NAME]

def _get_collection_from(database: str)->MongoClient:
    return database[COLLECTION_NAME]

def _get_pipeline() -> list:
    pipeline = [
        {'$sample': {'size': 30000}},
        {'$project': {'_id': 0}}
    ]
    return pipeline

def fetch_products():
    client = _connect_to_mongo()
    database = _get_database_from(client)
    collection = _get_collection_from(database)
    pipeline = _get_pipeline()

    return collection.aggregate(pipeline)




if __name__ == "__main__":
    try:
        products = fetch_products()
    except Exception as e:
        print(f"An error occurred: {e}")

    load_dotenv()
    products = fetch_products()
    for product in products:
        print(product)
