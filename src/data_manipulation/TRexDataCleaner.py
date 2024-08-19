import pandas as pd
import numpy as np
import math
from typing import Union, Tuple
from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.calculateVelocity import calculateVelocity

class TRexDataCleaner:
    """
    A class for cleaning TRex data by removing invalid data, such as sudden jumps or missing data points.
    
    Functions:
    ----------
    renderDiscontinuities:
        Identifies and removes discontinuities from TRex data, such as jumps or missing data, and marks them as 'infinity'.
    
    isDiscontinuity:
        Checks if there is a discontinuity between two data points.
    
    calculateVelocity:
        Computes the velocity between two points given their positions and the time elapsed.
    """

    def renderDiscontinuities(self, data: pd.DataFrame, vmax: Union[float, np.floating]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Removes discontinuities from the input data based on the specified maximum velocity (vmax).

        Parameters:
        -----------
        data : pd.DataFrame
            The TRex data to clean. Must include 'time', 'X', and 'Y' columns.
        vmax : float or np.floating
            The maximum velocity considered valid for the entity.

        Returns:
        --------
        Tuple[pd.DataFrame, pd.DataFrame]
            A tuple containing two DataFrames: the cleaned data and the data points identified as faulty.
        """
        assert all(col in data.columns for col in ['time', 'X', 'Y']), f"Expected columns of ['time', 'X', 'Y']\nReceived: {[col for col in data.columns]}"
        assert vmax > 0, f"Expected vmax > 0\nReceived: {vmax}"
        
        cleanedData = pd.DataFrame({
            'time': [data.loc[0, 'time']],
            'X': [data.loc[0, 'X']],
            'Y': [data.loc[0, 'Y']]
        })
        removedData = pd.DataFrame(columns=data.columns)
        
        validIndex = 0
        
        for f in range(1, len(data)):
            pi = data.iloc[validIndex]
            pf = data.iloc[f]
            
            if self.isDiscontinuity(pi=pi, pf=pf, vmax=vmax):
                removedData = pd.concat([removedData, pd.DataFrame([data.iloc[f]])], ignore_index=True)
                cleanedData = pd.concat([cleanedData, pd.DataFrame({'time': [data.loc[f, 'time']], 'X': [np.inf], 'Y': [np.inf]})], ignore_index=True)
            else:
                cleanedData = pd.concat([cleanedData, pd.DataFrame([data.iloc[f]])], ignore_index=True)
                validIndex = f

        return cleanedData.reset_index(drop=True), removedData.reset_index(drop=True)

    def isDiscontinuity(self, pi: pd.DataFrame, pf: pd.DataFrame, vmax: Union[float, np.floating]) -> bool:
        """
        Determines if there is a discontinuity between two points based on their positions and the time interval.

        Parameters:
        -----------
        pi : DataFrame
            The initial point of the entity, given as a section of a pandas DataFrame.
        pf : DataFrame
            The final position of the entity, given as a section of a pandas DataFrame.
        vmax : float or np.floating
            The maximum allowable velocity for the entity.

        Returns:
        --------
        bool
            True if there is a discontinuity, False otherwise.
        """
        if pf['X'] in ('infinity', np.inf) or pf['X'] in ('infinity', np.inf) or pi['Y'] in ('infinity', np.inf) or pi['Y'] in ('infinity', np.inf):
            return True
        velocity = calculateVelocity(pi=pi, pf=pf)
        return velocity > vmax

if __name__ == "__main__":
    dataCleaner = TRexDataCleaner()
    
    faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
    print(f"Faulty Data: \n{faultyData}")

    cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)
    print("Cleaned Data: \n", cleanedData)
    print("Removed Data: \n", removedData)
