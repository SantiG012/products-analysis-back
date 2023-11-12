from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from  database.connection import fetch_products
import pandas as pd
from dtos.correlation_dto import Correlation_dto
from dtos.products_stars_dto import ProductsByStarsDto
from dtos.topProduct_dto import TopProductDTO
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

@app.get("/topProductsByCategoryName/{category_name}")
def calculate_ranking_score(category_name: str):
    """
    Calcula la puntuación de los mejores productos en una categoría específica.

    Args:
        category_name (str): El nombre de la categoría.

    Returns:
        TopProductDTO: DTO con información sobre los mejores 5 productos de la categoría.
    """
    if not _products_fetched():
        raise HTTPException(status_code=500, detail="Products must be fetched first")
    
    if __category_exists(category_name):
        raise HTTPException(status_code=404, detail=f"The category '{category_name}' was not found.")
    
    BEST_SELLER_WEIGHT = 1
    STARS_WEIGHT = 0.5
    REVIEWS_WEIGHT = 0.3
    DISCOUNT_WEIGHT = 0.1
    BOUGHT_WEIGHT = 0.1

    category_df = products[(products['categoryName'] == category_name)].copy()
    category_df['discount_percentage'] = ((category_df['listPrice'] - category_df['price']) / category_df['listPrice']) * 100

    category_df['RankingScore'] = (
        (category_df['isBestSeller'].astype(int) * BEST_SELLER_WEIGHT) +
        (category_df['stars'] * STARS_WEIGHT) +
        (category_df['reviews'] * REVIEWS_WEIGHT) +
        (category_df['discount_percentage'] * DISCOUNT_WEIGHT) +
        (category_df['boughtInLastMonth'] * BOUGHT_WEIGHT)
    )

    top_products = category_df.sort_values(by='RankingScore', ascending=False)

    columns_to_show = ["title", "imgUrl", "stars", "price", "reviews", "isBestSeller"]

    top_products_list = top_products[columns_to_show].head(5)

    return TopProductDTO(Products_df = top_products_list.to_dict(orient="records"))

@app.get("/categories")
def get_categories():
    """
    Obtiene las categorías de los productos.

    Returns:
        list: Lista de categorías.
    """
    if not _products_fetched():
        raise HTTPException(status_code=500, detail="Products must be fetched first")
    
    return products["categoryName"].unique().tolist()


def _products_fetched():
    return products is not None

def _column_exists(column: str):
    return column in products.columns

def __category_exists(category_name: str):
    return category_name not in products["categoryName"].unique()
