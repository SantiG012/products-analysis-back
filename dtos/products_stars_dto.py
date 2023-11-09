from pydantic import BaseModel

class ProductsByStarsDto(BaseModel):
    productsByStars_df: list[dict]