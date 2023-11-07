from pydantic import BaseModel


class Correlation_dto(BaseModel):
    correlation: float
    correlation_df: list[dict]