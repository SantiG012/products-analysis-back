from typing import Union
from dotenv import load_dotenv

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    load_dotenv()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
