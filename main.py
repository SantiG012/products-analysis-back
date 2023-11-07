from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI
from  database.connection import fetch_products
import pandas as pd
from data_processing.correlations.rating_reviews import calculate_correlation_between
from dtos.correlation_dto import Correlation_dto

app = FastAPI()


@app.get("/")
def read_root():
    load_dotenv()
    products = fetch_products()
    products = pd.DataFrame(products)
    correlation = calculate_correlation_between(products["stars"], products["price"])
    correlation_df =products[['stars','price']]
    correlation_dto = Correlation_dto(correlation=correlation,correlation_df=correlation_df.to_dict(orient='records'))
    try:
        return correlation_dto
    except Exception as e:
        return f"An error occurred: {e}"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
