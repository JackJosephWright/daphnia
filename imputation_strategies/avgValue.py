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
        ti = data['time'][validIndex]
        tf = data['time'][f]
        
        if dataCleaner.isDiscontinuity(pi, pf, vmax, ti, tf): 
            print("Discontinuity")
            continue
        
        validIndexTime = data['time'][validIndex]
        
        velocityX = pf[0] - pi[0]
        velocityY = pf[1] - pi[1]
        timeStep = (tf-ti)/(f-validIndex)
        
        for i in range(validIndex + 1, f):
            rate = i - validIndex
            newX = pi[0] + (velocityX * rate)
            newY = pi[1] + (velocityY * rate)
            data.iloc[i] = [validIndexTime + (timeStep * rate), newX, newY]
        
        validIndex = f

    return data