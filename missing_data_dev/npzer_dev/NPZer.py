import numpy as np
import pandas as pd
from typing import Union
from TRexDataTester import TRexDataTester

class NPZer:
    """ Handles Numpy .npz data and Pandas DataFrames

        Functions:
        ----------
        npzip:
            Converts Pandas DataFrame or Numpy matrix into a zipped npz file
        unzipNpz:
            Unzips .npz file
        pandafy:
             Converts unzipped npz data to a Pandas DataFrame
        
    """

    def npzip(data: Union[pd.DataFrame, np.ndarray], save_dir: str, params: list = [], tester: TRexDataTester = None):
        """ Converts Pandas DataFrame or Numpy matrix into a zipped npz file
            
            Parameters:
            -----------
                data: Pandas DataFrame or Numpy Matrix
                    Data to be zipped
                save_dir: str/path
                    File path to save zipped data to
                params: List, optional
                    Selects which parameters to zip. If not specified, all parameters will be zipped.
                tester: TRexDataTester, optional
                    Tests data to check if it is structured correctly
        """
        
        if isinstance(tester, TRexDataTester):
            tester.testAll(data)
        
        assert len(params) > 0, f"\nExpected at least 1 parameter to be saved. \nReceived: {len(params)}"
        
        if isinstance(data, pd.DataFrame):
            if len(params) > 0 : np.savez(file=save_dir, **{f"{param}": data[param].values for param in params})
            else: np.savez(file=save_dir, **{f"{param}": data[param].values for param in data.columns})
        else:
            if len(params) > 0: np.savez(file=save_dir, **{f"{params[i]}": data[i] for i in range(len(params))})
            else: np.savez(file=save_dir, **{f"{params[i]}": data[i] for i in range(len(data))})
    
    def unzipNpz(source_dir: str, params: list = [], tester: TRexDataTester = None,) -> np.ndarray:
        """ Unzips .npz file
            
            Parameters:
            -----------
                source_dir: str/path
                    .npz file path to be unzipped
                params: List, optional
                    Selects which parameters to save. If not specified, all parameters will be saved.
                tester: TRexDataTester, optional
                    Tests data to check if it is structured correctly
        """
        
        assert source_dir.endswith('.npz')
        
        with np.load(file = source_dir) as openedArray:
            if len(params) > 0:
                for param in params:
                    assert param in openedArray.keys(), f"{param} is not a valid parameter in the data"
                unzippedArray = np.array([openedArray[param] for param in params])
            else:
                unzippedArray = np.array([openedArray[key] for key in openedArray.keys()])
            
            if isinstance(tester, TRexDataTester):
                tester.testAll(data)
            
            return unzippedArray


    def pandafy(data: np.ndarray, invertY: bool = False, params: list = [], tester: TRexDataTester = None) -> pd.DataFrame:
        """ Converts unzipped npz data to a Pandas DataFrame
            
            Parameters:
            -----------
                data: np.ndarray
                    Data to be converted into pandas DataFrame
                invertY: bool, optional
                    Invert Y values if true, otherwise false
                params: List, optional
                    Selects which parameters to save. If not specified, all parameters will be saved.
                tester: TRexDataTester, optional
                    Tests data to check if it is structured correctly
        """

        if isinstance(tester, TRexDataTester):
            tester.testAll(data)
        
        if len(params) > 0: pandaDataFrame = pd.DataFrame(data = data, index = [param for param in params])  
        else: pd.DataFrame(data = data, columns = [i for i in range(len(data))])
        
        if invertY:
            pandaDataFrame.loc['Y#wcentroid'] = -pandaDataFrame.loc['Y#wcentroid']
        
        return pandaDataFrame.T



if __name__ == "__main__":
    data = NPZer.unzipNpz(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', params = ['time', 'X#wcentroid', 'Y#wcentroid'])
    
    tester = TRexDataTester(timeTracked = True, dtype = np.floating)
    tester.testAll(data)
    
    print("Unzipped data:\n", data)
    
    pandasData = NPZer.pandafy(data = data, invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'], tester = tester)
    print("Pandafied:\n", pandasData)

    NPZer.npzip(data = pandasData, save_dir = 'missing_data_dev/npzer_dev/zipped.npz', tester = tester, params = ['time', 'X#wcentroid', 'Y#wcentroid'])
    unzipped = NPZer.unzipNpz(source_dir = 'missing_data_dev/npzer_dev/zipped.npz', params = ['time', 'X#wcentroid', 'Y#wcentroid'])
    print("Unzipped again:\n", unzipped)

    pandasData = NPZer.pandafy(data = unzipped, invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'], tester = tester)
    print("Pandafied again:\n", pandasData)