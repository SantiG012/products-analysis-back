from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI
from  database.connection import fetch_products
import pandas as pd

app = FastAPI()


@app.get("/")
def read_root():
    load_dotenv()
    products = fetch_products()
    products = pd.DataFrame(products)
    try:
        return products.to_dict(orient="records")
    except Exception as e:
        return f"An error occurred: {e}"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
