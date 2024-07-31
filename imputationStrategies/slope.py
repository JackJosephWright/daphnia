import numpy as np
import pandas as pd

def impute(data: pd.DataFrame = None) -> pd.DataFrame:
    if data is None:
        return "Imputes data between two points through slope"
    
    data.reset_index()
    for row in data.iterrows():
        data.iloc[row[0]] = [1, 1, 1]
    
    return data