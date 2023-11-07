import pandas as pd

def calculate_correlation_between(series_a: pd.Series,series_b: pd.Series)->float:
    if not _has_numeric_values(series_a) and not _has_numeric_values(series_b):
       raise Exception("Series must contain numeric values")
    
    return series_a.corr(series_b)
    


def _has_numeric_values(series: pd.Series)->bool:
    return series.dtype == "float64" or series.dtype == "int64"