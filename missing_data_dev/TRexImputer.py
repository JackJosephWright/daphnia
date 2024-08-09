import os
import numpy as np
import importlib.util
from src.data_manipulation.TRexDataTester import TRexDataTester
from src.data_manipulation.NPZer import NPZer
import pandas as pd

class TRexImputer:
    """Handles TRex data imputation
    
    Functions:
    ----------
    impute:
        Imputes data's faulty values
    functions:
        Describes imputation strategies
    """
    def __init__(self, strategy_dir='imputation_strategies'):
        self.imputationStrategies = {}
        strategy_dir_path = os.path.abspath(strategy_dir)
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
        
    def impute(self, data: pd.DataFrame, function: str = 'avgValue', tester: TRexDataTester = None) -> pd.DataFrame:
        """Imputes data's faulty values

        Parameters:
        -----------
        function: str, default 'avgValue'
            Function used to impute
        data: pd.DataFrame
            Data to impute
        tester: TRexDataTester, optional

        Returns:
        --------
        pd.DataFrame: imputed data
        """
        if tester is not None:
            tester.testAll(data)
        
        assert function in self.imputationStrategies, f"Imputation function '{function}' is not in self.imputationStrategies. Available functions: {list(self.imputationStrategies.keys())}"
        
        print(f"Imputing with: {function}()")
        imputedData = self.imputationStrategies[function](data)
        
        return imputedData
    
    def functions(self):
        """Describes imputation strategies"""
        print("Imputation functions: \n")
        for function in self.imputationStrategies:
            print(f"{function}(): {self.imputationStrategies[function]()}\n")
        
        
if __name__ == '__main__':
    imputer = TRexImputer()
    
    data = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
    
    imputer.functions()
    
    print(imputer.impute(data))
