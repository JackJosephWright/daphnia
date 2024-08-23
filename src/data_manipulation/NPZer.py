import numpy as np
import pandas as pd
from typing import Union, List

class NPZer:
    """
    A utility class for handling Numpy .npz files and Pandas DataFrames.

    Functions:
    ----------
    npzip:
        Converts a Pandas DataFrame or a Numpy matrix into a zipped .npz file.
    unzipNpz:
        Unzips a .npz file and returns its contents as a Numpy array.
    pandafy:
        Converts unzipped .npz data into a Pandas DataFrame.
    """

    @staticmethod
    def npzip(data: Union[pd.DataFrame, np.ndarray], save_dir: str, params: List[str] = []):
        """
        Converts a Pandas DataFrame or a Numpy matrix into a zipped .npz file.
        
        Parameters:
        -----------
        data : Union[pd.DataFrame, np.ndarray]
            The data to be zipped.
        save_dir : str
            The file path where the zipped data will be saved.
        params : List[str], optional
            A list of parameters to zip. If not specified, all parameters will be zipped.
        """
        
        if isinstance(data, pd.DataFrame):
            if not params:
                params = data.columns
            np.savez(file=save_dir, **{param: data[param].values for param in params})
        else:  # Assuming data is a numpy array
            if not params:
                params = [f"param_{i}" for i in range(data.shape[0])]
            np.savez(file=save_dir, **{params[i]: data[i] for i in range(len(params))})

    @staticmethod
    def pandafy(data: np.ndarray = None, source_dir: str = None, invertY: bool = False, params: List[str] = []) -> pd.DataFrame:
        """
        Converts unzipped .npz data or a Numpy array into a Pandas DataFrame.
        
        Parameters:
        -----------
        data : np.ndarray, optional
            The Numpy array to be converted into a Pandas DataFrame.
        source_dir : str, optional
            The file path of the .npz file to be converted into a Pandas DataFrame.
        invertY : bool, optional
            If True, inverts the Y values in the DataFrame. Default is False.
        params : List[str], optional
            A list of parameters to extract. If not specified, all parameters will be extracted.
            
        Returns:
        --------
        pd.DataFrame
            A Pandas DataFrame containing the extracted data.
        """
        
        assert (data is not None) or (source_dir is not None), f"No data source provided. data exists: {data is None}, source_dir exists: {source_dir is None}"
        
        if source_dir is not None:
            assert source_dir.endswith('.npz'), "Provided file is not a .npz file"
            with np.load(source_dir) as openedData:
                pandaDataFrame = pd.DataFrame({key: openedData[key] for key in openedData.keys() if openedData[key].ndim == 1})
                
                if params:
                    pandaDataFrame = pandaDataFrame[params]

                if invertY:
                    assert 'Y' in pandaDataFrame.columns, f"Data has no parameter Y"
                    pandaDataFrame['Y'] = -pandaDataFrame['Y']
            
                return pandaDataFrame
        else:
            
            if params:
                pandaDataFrame = pd.DataFrame(data=data, columns=params)  
            else:
                pandaDataFrame = pd.DataFrame(data=data)
            
            if invertY:
                assert 'Y' in pandaDataFrame.columns, f"No Y parameter in dataset"
                pandaDataFrame['Y'] = -pandaDataFrame['Y']
            
            return pandaDataFrame
