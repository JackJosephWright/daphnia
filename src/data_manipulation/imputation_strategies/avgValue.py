import numpy as np
import pandas as pd
from typing import Union

import numpy as np
import pandas as pd
from typing import Union

def impute(data: pd.DataFrame = None, function: str = 'avgValue') -> pd.DataFrame:
    if data is None:
        return "Fill values with an average velocity to connect two disconnected segments"
    
    assert all(col in data.columns for col in ['time', 'X', 'Y']), f"Expected columns of ['time', 'X', 'Y']\nReceived: {data.columns}"
    data = data.copy(deep=True)
    data.reset_index(drop=True, inplace=True)
    
    lastValidIndex = 0
    
    for f in range(1, len(data)):
        if data.loc[f, 'X'] in ('infinity', np.inf):
            i = f
            while i < len(data) and data.loc[i, 'X'] in ('infinity', np.inf):
                i += 1
            
            # If we reach the end of the DataFrame and it's still invalid, use the last valid index
            if i >= len(data):
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
    """Calculates velocity between two points.
    
    Parameters:
    -----------
    pi: float or np.floating
        Initial position of the entity.
    pf: float or np.floating
        Final position of the entity.
    dtime: float or np.floating
        Time difference between pi and pf.
    
    Returns:
    --------
    float: Calculated velocity.
    """
    assert dtime != 0, "dtime must be non-zero to calculate velocity."
    return (pf - pi) / dtime
