import pandas as pd
import numpy as np
import math
from typing import Union, Tuple
from NPZer import NPZer

class TRexDataCleaner:
    """ Removes invalid data from TRex data, e.g., sudden jumps, missing data

        Functions:
        ----------
        renderDiscontinuities: 
            Renders discontinuities from TRex data, e.g., jumps, missing data as 'infinity'
        isDiscontinuity:
            checks whether a point is a discontinuity from another
        calculateVelocity:
            calculates velocity between two points
    """    

    def renderDiscontinuities(self, data: pd.DataFrame, vmax: Union[float, np.floating]) -> Tuple[pd.DataFrame, pd.DataFrame]:        
        """ Removes discontinuities from data
        
            Parameters:
            -----------
            data: pd.DataFrame
                data to clean
            vmax: float or np.floating
                maximum velocity of entity
            
            Returns:
            -------- 
            Tuple of two Pandas DataFrames: (Cleaned DataFrame, Faulty rows from DataFrame)
        """

        assert all(col in data.columns for col in ['time', 'X#wcentroid', 'Y#wcentroid']), f"Expected columns of ['time', 'X#wcentroid', 'Y#centroid']\nRecieved: {[col for col in data.columns]}"
        assert vmax > 0, f"Expected vmax >0\nRecieved: {vmax}"
        
        cleanedData = pd.DataFrame(data = data.iloc[0], columns = data.columns)
        removedData = pd.DataFrame(columns = data.columns)
        
        validIndex = 0
        
        for f in range(1, len(data)):
            pi = (data['X#wcentroid'][validIndex], data['Y#wcentroid'][validIndex])
            pf = (data['X#wcentroid'][f], data['Y#wcentroid'][f])
            
            if self.isDiscontinuity(pi, pf, vmax, data['time'][f] - data['time'][validIndex]): 
                print(f"Faulty row: \nInitial: \n--------\n{data.iloc[validIndex]}\n|\nV\nFinal: \n------\n{data.iloc[f]} \n\n\n")
                removedData.loc[len(removedData)] = data.iloc[f]
                cleanedData.loc[len(cleanedData['time'])] = ['infinity', 'infinity', 'infinity']
                continue
            
            cleanedData.loc[len(cleanedData['time'])] = data.iloc[f]
            validIndex = f

        return (cleanedData.reset_index(drop = True), removedData.reset_index(drop = True))

    def isDiscontinuity(self, pi: Union[Tuple[float, float], Tuple[np.floating, np.floating]], pf: Union[Tuple[float, float], Tuple[np.floating, np.floating]], vmax: Union[float, np.floating], dtime: Union[float, np.floating] = 1.0) -> bool:
        """ Determines if a jump between two points is a discontinuity

            Parameters:
            -----------
                pi: (float, float) or (np.floating, np.floating)
                    initial position of entity. Given as (x-coordinate, y-coordinate)
                pf: (float, float) or (np.floating, np.floating)
                    final position of entity. Given as (x-coordinate, y-coordinate)
                vmax: float or np.floating
                    maximum velocity of entity
                dtime: float or np.floating, default 1s
                    difference in time between pi and pf
                    
            Returns:
            --------
            Boolean: Discontinuity or not
        """        
        if pf[1] in ('infinity', np.inf): return True
        
        velocity = self.calculateVelocity(pi, pf, dtime)
        return velocity > vmax

    def calculateVelocity(self, pi: Union[Tuple[float, float], Tuple[np.floating, np.floating]], pf: Union[Tuple[float, float], Tuple[np.floating, np.floating]], dtime: Union[float, np.floating] = 1.0) -> float:
        """ Calculates velocity between two points
        
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
        
        xDistance = pf[0] - pi[0]
        yDistance = pf[1] - pi[1]
        
        distance = math.sqrt(xDistance**2 + yDistance**2)
        velocity = distance / dtime
        
        return velocity


if __name__ == "__main__":
    dataCleaner = TRexDataCleaner()
    
    faultyData = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'])
    print(f"Faulty Data: \n {faultyData}")

    cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)
    print("Cleaned Data: \n", cleanedData)
    print("Removed Data: \n", removedData)
