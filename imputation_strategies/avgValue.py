import os
import numpy as np
import pandas as pd
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner


def impute(data: pd.DataFrame = None, vmax: float = 1) -> pd.DataFrame:
    if data is None:
        return "fill values with an avg velocity to connect two disconnected segments"
    
    assert all(col in data.columns for col in ['time', 'X#wcentroid', 'Y#wcentroid']), f"Expected columns of ['time', 'X#wcentroid', 'Y#wcentroid']\nRecieved: {[col for col in data.columns]}"
    
    dataCleaner = TRexDataCleaner()
    
    data.reset_index(drop=True)
    
    validIndex = 0
    
    for f in range(1, len(data)):
        pi = (data['X#wcentroid'][validIndex], data['Y#wcentroid'][validIndex])
        pf = (data['X#wcentroid'][f], data['Y#wcentroid'][f])  
        dtime = data['time'][f] - data['time'][validIndex]
        
        if dataCleaner.isDiscontinuity(pi, pf, vmax, dtime): 
            continue
        
        validIndexTime = data['time'][validIndex]
        
        velocityX = pf[0] - pi[0]
        velocityY = pf[1] - pi[1]
        timeStep = dtime/(f-validIndex)
        
        for i in range(validIndex + 1, f):
            rate = i - validIndex
            newX = pi[0] + (velocityX * rate)
            newY = pi[1] + (velocityY * rate)
            data.at[i, 'time'] = validIndexTime + (timeStep * rate)
            data.at[i, 'X#wcentroid'] = newX
            data.at[i, 'Y#wcentroid'] = newY
        
        validIndex = f

    return data