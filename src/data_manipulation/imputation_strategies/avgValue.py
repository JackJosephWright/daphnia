import numpy as np
import pandas as pd
from typing import Union

def impute(data: pd.DataFrame = None) -> pd.DataFrame:
    """
    Imputes missing or invalid data points in a DataFrame by filling in values based on average velocity.

    Parameters:
    -----------
    data : pd.DataFrame, optional
        A DataFrame with 'time', 'X', and 'Y' columns. Missing data points in the 'X' and 'Y' columns will be filled in.
   
    Returns:
    --------
    pd.DataFrame
        The DataFrame with missing or invalid data points imputed.
    """
    if data is None:
        raise ValueError("DataFrame cannot be None. Provide a DataFrame with 'time', 'X', and 'Y' columns.")

    required_columns = ['time', 'X', 'Y']
    assert all(col in data.columns for col in required_columns), f"Expected columns: {required_columns}\nReceived: {list(data.columns)}"
    
    data = data.copy(deep=True)
    data.reset_index(drop=True, inplace=True)
    
    lastValidIndex = 0
    
    for f in range(1, len(data)):
        if data.loc[f, 'X'] in ('infinity', np.inf):
            i = f
            while i < len(data) and data.loc[i, 'X'] in ('infinity', np.inf):
                i += 1
            
            if i >= len(data):  # End of DataFrame reached with still invalid data
                velocityX = calculateVelocity(data.loc[lastValidIndex, 'X'], data.loc[lastValidIndex, 'X'], data.loc[f, 'time'] - data.loc[lastValidIndex, 'time'])
                velocityY = calculateVelocity(data.loc[lastValidIndex, 'Y'], data.loc[lastValidIndex, 'Y'], data.loc[f, 'time'] - data.loc[lastValidIndex, 'time'])
                
                for imputeIndex in range(f, len(data)):
                    data.loc[imputeIndex, 'X'] = data.loc[lastValidIndex, 'X'] + velocityX * (data.loc[imputeIndex, 'time'] - data.loc[lastValidIndex, 'time'])
                    data.loc[imputeIndex, 'Y'] = data.loc[lastValidIndex, 'Y'] + velocityY * (data.loc[imputeIndex, 'time'] - data.loc[lastValidIndex, 'time'])
                break  # Exit loop since we've reached the end of the DataFrame

            nextValidIndex = i
            dtime = data.loc[nextValidIndex, 'time'] - data.loc[lastValidIndex, 'time']
            if dtime == 0:
                continue
            
            velocityX = calculateVelocity(data.loc[lastValidIndex, 'X'], data.loc[nextValidIndex, 'X'], dtime)
            velocityY = calculateVelocity(data.loc[lastValidIndex, 'Y'], data.loc[nextValidIndex, 'Y'], dtime)
            
            for imputeIndex in range(lastValidIndex + 1, nextValidIndex):
                data.loc[imputeIndex, 'X'] = data.loc[lastValidIndex, 'X'] + velocityX * (data.loc[imputeIndex, 'time'] - data.loc[lastValidIndex, 'time'])
                data.loc[imputeIndex, 'Y'] = data.loc[lastValidIndex, 'Y'] + velocityY * (data.loc[imputeIndex, 'time'] - data.loc[lastValidIndex, 'time'])
        else:
            lastValidIndex = f
    
    return data

def calculateVelocity(pi: Union[float, np.floating], pf: Union[float, np.floating], dtime: Union[float, np.floating]) -> float:
    """
    Calculates the velocity between two points.

    Parameters:
    -----------
    pi : float or np.floating
        The initial position of the entity.
    pf : float or np.floating
        The final position of the entity.
    dtime : float or np.floating
        The time difference between the initial and final positions.

    Returns:
    --------
    float
        The calculated velocity.
    """
    assert dtime != 0, "dtime must be non-zero to calculate velocity."
    return (pf - pi) / dtime
