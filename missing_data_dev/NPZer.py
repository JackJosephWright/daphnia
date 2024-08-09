import numpy as np
import pandas as pd
from typing import Union
from src.data_manipulation.TRexDataTester import TRexDataTester

class NPZer:
    """Handles Numpy .npz data and Pandas DataFrames

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
        """Converts Pandas DataFrame or Numpy matrix into a zipped npz file
            
        Parameters:
        -----------
        data: Pandas DataFrame or Numpy Matrix
            Data to be zipped
        save_dir: str
            File path to save zipped data to
        params: List, optional
            Selects which parameters to zip. If not specified, all parameters will be zipped.
        tester: TRexDataTester, optional
            Tests data to check if it is structured correctly
        """
        
        if tester is not None:
            tester.testAll(data)
        
        if isinstance(data, pd.DataFrame):
            if len(params) == 0:
                params = data.columns
            np.savez(file=save_dir, **{param: data[param].values for param in params})
        else:  # Assuming data is a numpy array
            if len(params) == 0:
                params = [f"param_{i}" for i in range(data.shape[0])]
            np.savez(file=save_dir, **{params[i]: data[i] for i in range(len(params))})
    
    def unzipNpz(source_dir: str, params: list = [], tester: TRexDataTester = None) -> np.ndarray:
        """Unzips .npz file
            
        Parameters:
        -----------
        source_dir: str
            .npz file path to be unzipped
        params: List, optional
            Selects which parameters to save. If not specified, all parameters will be saved.
        tester: TRexDataTester, optional
            Tests data to check if it is structured correctly
            
        Returns:
        --------
        np.ndarray: Numpy Matrix of data
        """
        
        assert source_dir.endswith('.npz'), "Provided file is not a .npz file"
        
        with np.load(source_dir) as openedArray:
            if len(params) > 0:
                for param in params:
                    assert param in openedArray.keys(), f"{param} is not a valid parameter in the data"
                unzippedArray = np.array([openedArray[param] for param in params])
            else:
                unzippedArray = np.array([openedArray[key] for key in openedArray.keys()])
            
            if tester is not None:
                tester.testAll(unzippedArray)
            
            return unzippedArray

    def pandafy(data: np.ndarray = None, source_dir: str = None, invertY: bool = False, params: list = [], tester: TRexDataTester = None) -> pd.DataFrame:
        """Converts unzipped npz data to a Pandas DataFrame
            
        Parameters:
        -----------
        data: np.ndarray
            Data to be converted into pandas DataFrame
        source_dir: str, optional
            .npz file to be converted into Pandas DataFrame
        invertY: bool, optional
            Invert Y values if true, otherwise false
        params: List, optional
            Selects which parameters to save. If not specified, all parameters will be saved.
        tester: TRexDataTester, optional
            Tests data to check if it is structured correctly
            
        Returns:
        --------
        pd.DataFrame: Pandas DataFrame of given data
        """
        
        assert (data is not None) or (source_dir is not None), f"No data source provided. data exists: {data is None}, source_dir exists: {source_dir is None}"
        
        if source_dir is not None:
            assert source_dir.endswith('.npz'), "Provided file is not a .npz file"
            with np.load(source_dir) as openedData:
                pandaDataFrame = pd.DataFrame.from_dict(data={key: openedData[key] for key in openedData.keys() if openedData[key].ndim == 1})
                
                if len(params) > 0: 
                    pandaDataFrame = pandaDataFrame[params]
                
                if tester is not None:
                    tester.testAll(pandaDataFrame)
                
                if invertY:
                    assert 'Y' in pandaDataFrame.columns, f"Data has no parameter Y"
                    pandaDataFrame['Y'] = -pandaDataFrame['Y']
            
                return pandaDataFrame
        else:
            if tester is not None:
                tester.testAll(data)
            
            if len(params) > 0:
                pandaDataFrame = pd.DataFrame(data=data, columns=params)  
            else:
                pandaDataFrame = pd.DataFrame(data=data)
            
            if invertY:
                assert 'Y' in pandaDataFrame.columns, f"No Y parameter in dataset"
                pandaDataFrame['Y'] = -pandaDataFrame['Y']
            
            return pandaDataFrame
