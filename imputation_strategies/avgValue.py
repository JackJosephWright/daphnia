import os
import numpy as np
import pandas as pd
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from typing import Union


def impute(data: pd.DataFrame = None, function: str = 'avgValue') -> pd.DataFrame:
    if data is None:
        return "fill values with an avg velocity to connect two disconnected segments"
    
    assert all(col in data.columns for col in ['time', 'X', 'Y']), f"Expected columns of ['time', 'X', 'Y']\nReceived: {data.columns}"
    
    data.reset_index(drop=True, inplace=True)
    
    lastValidIndex = 0
    
    for f in range(1, len(data)):
        if data.loc[f, 'X'] in ('infinity', np.inf): 
            i = f
            while data.loc[i, 'X'] in ('infinity', np.inf):
                i += 1
                if i == len(data) - 1:
                    break
            nextValidIndex = i
            
            dtime = data.loc[nextValidIndex, 'time'] - data.loc[lastValidIndex, 'time']
            velocityX = calculateVelocity(data.loc[lastValidIndex, 'X'], data.loc[nextValidIndex, 'X'], dtime)
            velocityY = calculateVelocity(data.loc[lastValidIndex, 'Y'], data.loc[nextValidIndex, 'Y'], dtime)
            
            for imputeIndex in range(lastValidIndex + 1, nextValidIndex):
                data.loc[imputeIndex, 'X'] = data.loc[lastValidIndex, 'X'] + velocityX * (data.loc[imputeIndex, 'time'] - data.loc[lastValidIndex, 'time'])
                data.loc[imputeIndex, 'Y'] = data.loc[lastValidIndex, 'Y'] + velocityY * (data.loc[imputeIndex, 'time'] - data.loc[lastValidIndex, 'time'])
        else:
            lastValidIndex = f
        
    return data
def calculateVelocity(pi: Union[float, np.floating], pf: Union[float, np.floating], dtime: Union[float, np.floating]) -> float:
    """Calculates velocity between two points
    Parameters:
    -----------
    pi: (float, float) or (np.floating, np.floating)
        Initial position of entity. Given as (x-coordinate, y-coordinate)
    pf: (float, float) or (np.floating, np.floating)
        Final position of entity. Given as (x-coordinate, y-coordinate)
    dtime: float or np.floating, default 1s
        Difference in time between pi and pf
    Returns:
    --------
    Float: calculated velocity
    """
    return (pf - pi) / dtime
    