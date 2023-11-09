from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from  database.connection import fetch_products
import pandas as pd
from dtos.correlation_dto import Correlation_dto
from dtos.products_stars_dto import ProductsByStarsDto
from data_processing.correlations.rating_reviews import calculate_correlation_between

app = FastAPI()
products = None


@app.get("/")
def set_up():
    load_dotenv()
    try:
        global products 
        products = fetch_products()
        products = pd.DataFrame(products)
        print(products)
        return "Products fetched successfully!"
    except Exception as e:
        return f"An error occurred: {e}"
    

@app.get("/correlation/{column_a}/{column_b}")
def read_item(column_a: str, column_b: str):
    if not _products_fetched():
        raise HTTPException(status_code=500, detail="Products must be fetched first")
    
    if not _column_exists(column_a) or not _column_exists(column_b):
        raise HTTPException(status_code=404,detail=f"Either {column_a} or {column_b} does not exist")
    
    try:
        correlation = calculate_correlation_between(products[column_a], products[column_b])
        correlation_df = products[[column_a, column_b]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    correlation_dto = Correlation_dto(correlation=correlation, correlation_df=correlation_df.to_dict(orient="records"))

    return correlation_dto

#Retorna los datos necesarios para el pie chart, la cantidad de productos asociadas a un intervalo de rating o stars
@app.get("/productsByStars")
def countProductsByStars():
    if not _products_fetched():
        raise HTTPException(status_code=500, detail="Products must be fetched first")

    try:
        productsCountByStars_df = products.groupby("stars").size().reset_index(name="total_productos")
    
        bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
        interval_labels = ["0 - 0.5","0.5 - 1","1 - 1.5", "1.5 - 2","2 - 2.5", "2.5 - 3","3 - 3.5","3.5 - 4","4 - 4.5","4.5 - 5"]
        productsCountByStars_df["stars_interval"] = pd.cut(productsCountByStars_df["stars"], bins=bins, labels=interval_labels, right=False)
        productsCount = productsCountByStars_df.groupby("stars_interval")["total_productos"].sum().reset_index(name="total_productos")
        print(productsCount)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    productsByStarsDto = ProductsByStarsDto(productsByStars_df=productsCount.to_dict(orient="records"))

    return productsByStarsDto


def _products_fetched():
    return products is not None

def _column_exists(column: str):
    return column in products.columns