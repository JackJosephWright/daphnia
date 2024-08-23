import numpy as np
import pandas as pd

def impute(data: pd.DataFrame = None) -> pd.DataFrame:
    """
    This is just an example of how to create an impute functiom

    Parameters:
    -----------
    data: pd.DataFrame, optional Defaults to None.

    Returns:
    --------
    pd.DataFrame: 
        imputed dataframe
    """
    if data is None:
        return "Imputes data by random"
    return data.iloc[0]