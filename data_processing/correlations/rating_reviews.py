import pandas as pd

def calculate_correlation_between(rating: pd.Series,reviews: pd.Series)->float:
    return rating.corr(reviews)

