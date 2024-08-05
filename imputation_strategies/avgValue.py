import os
import numpy as np
import pandas as pd
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from typing import Union


def impute(data: pd.DataFrame = None) -> pd.DataFrame:
    if data is None:
        return "fill values with an avg velocity to connect two disconnected segments"
    
    assert all(col in data.columns for col in ['time', 'X', 'Y']), f"Expected columns of ['time', 'X', 'Y']\nRecieved: {[col for col in data.columns]}"
    
    data.reset_index(drop=True)
    
    lastValidIndex = 0
    
    for f in range(1, len(data)):
        if data.loc[f, 'X'] in ('infinity', np.inf): 
            i = f
            while(data.loc[i, 'X'] in ('infinity', np.inf)):
                i = i + 1
                continue
            nextValidIndex = i

            dtime = data.loc[nextValidIndex, 'time'] - data.loc[lastValidIndex, 'time']
            velocityX = calculateVelocity(pi = data.loc[lastValidIndex, 'X'], pf = data.loc[nextValidIndex, 'X'], dtime = dtime)
            velocityY = calculateVelocity(pi = data.loc[lastValidIndex, 'Y'], pf = data.loc[nextValidIndex, 'Y'], dtime = dtime)
            
            for imputeIndex in range(lastValidIndex + 1, nextValidIndex):
                data.loc[imputeIndex, 'X'] = data.loc[lastValidIndex, 'X'] + (velocityX * (dtime / (imputeIndex - lastValidIndex)))
                data.loc[imputeIndex, 'Y'] = data.loc[lastValidIndex, 'Y'] + (velocityY * (dtime / (imputeIndex - lastValidIndex)))
        else:
            lastValidIndex = f
        
    return data
    
def calculateVelocity(pi: Union[float, np.floating], pf: Union[float, np.floating], dtime: Union[float, np.floating]) -> float:
    """Calculates velocity between two points
            Parameters:
            -----------
            pi: (float, float) or (np.floating, np.floating)
                initial position of entity. Given as (x-coordinate, y-coordinate)
            pf: (float, float) or (np.floating, np.floating)
                final position of entity. Given as (x-coordinate, y-coordinate)
            dtime: float or np.floating, default 1s
                difference in time between pi and pf
            Returns:
            --------
            Float: calculated velocity
    """
    return (pf - pi)/dtime
    