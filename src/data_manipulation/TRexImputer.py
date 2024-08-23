import os
import numpy as np
import importlib.util
from src.data_manipulation.NPZer import NPZer
import pandas as pd

class TRexImputer:
    """
    Handles TRex data imputation.

    This class loads imputation strategies from Python files in a specified directory 
    and applies these strategies to impute faulty values in TRex data.

    Attributes
    ----------
    imputationStrategies : dict
        A dictionary storing the available imputation functions.

    Methods
    -------
    impute(data, function='avgValue'):
        Imputes faulty values in the provided data using the specified function.
    
    functions():
        Lists all available imputation strategies.
    """
    def __init__(self, strategy_dir='imputation_strategies'):
        """
        Initializes the TRexImputer class by loading imputation strategies.

        This method sets up the TRexImputer by locating and loading all available 
        imputation strategies from Python files in the specified directory. Each 
        imputation strategy should be a Python function named 'impute' within the 
        file, which will be added to the `imputationStrategies` dictionary.

        Parameters
        ----------
        strategy_dir : str, optional
            The directory containing the Python files with imputation strategies. 
            Defaults to 'imputation_strategies'.

        Raises
        ------
        FileNotFoundError
            If the specified strategy directory does not exist.
        
        Exception
            If an error occurs while loading a module, the error is caught and printed, 
            but the imputer continues to load other available strategies.
        """
        self.imputationStrategies = {}
        strategy_dir_path = os.path.abspath(os.path.join('src', 'data_manipulation', strategy_dir))
        if not os.path.exists(strategy_dir_path):
            raise FileNotFoundError(f"Directory {strategy_dir_path} does not exist.")
        
        for filename in os.listdir(strategy_dir_path):
            if filename.endswith('.py'):
                function = filename[:-3]
                file_path = os.path.join(strategy_dir_path, filename)
                
                # Import the function from the file
                spec = importlib.util.spec_from_file_location(function, file_path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Error loading module {filename}: {e}")
                    continue
                
                # Get the function and add it to the dictionary
                func = getattr(module, 'impute', None)
                if func:
                    self.imputationStrategies[function] = func
    
    def impute(self, data: pd.DataFrame, function: str = 'avgValue') -> pd.DataFrame:
        """
        Imputes faulty values in the provided data.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame containing the data to be imputed.
        function : str, optional
            The name of the imputation function to use. Defaults to 'avgValue'.

        Returns
        -------
        pd.DataFrame
            The DataFrame with imputed data.

        Raises
        ------
        AssertionError
            If the specified function is not found in the available imputation strategies.
        """

        assert function in self.imputationStrategies, f"Imputation function '{function}' is not in self.imputationStrategies. Available functions: {list(self.imputationStrategies.keys())}"
        
        print(f"Imputing with: {function}()")
        imputedData = self.imputationStrategies[function](data)
        
        return imputedData
    
    def functions(self):
        """
        Prints a list of all available imputation strategies.

        This method prints the names of the functions available for data imputation, 
        as well as a brief description if provided by the function.
        """
        print("Imputation functions: \n")
        for function in self.imputationStrategies:
            print(f"{function}(): {self.imputationStrategies[function]()}\n")

if __name__ == '__main__':
    imputer = TRexImputer()
    
    data = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
    
    imputer.functions()
    
    print(imputer.impute(data))
