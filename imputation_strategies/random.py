import numpy as np
import pandas as pd

def impute(data: pd.DataFrame = None) -> pd.DataFrame:
    if data is None:
        return "Imputes data by random"
    return data.iloc[0]