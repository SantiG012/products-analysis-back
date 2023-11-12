from pydantic import BaseModel
from typing import List

class TopProductDTO(BaseModel):
    Products_df: list[dict]