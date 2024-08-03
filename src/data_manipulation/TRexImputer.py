import os
import numpy as np
import importlib.util
from src.data_manipulation.TRexDataTester import TRexDataTester
from src.data_manipulation.NPZer import NPZer
import pandas as pd

class TRexImputer:
    """ Handles TRex data imputation
    
        Functions:
        ----------
        impute:
            Imputes data's faulty values
        functions:
            Describes imputation strategies
    """
    def __init__(self):
        self.imputationStrategies = {}
        for filename in os.listdir('imputation_strategies'):
            if filename.endswith('.py'):
                function = filename[:-3]
                file_path = os.path.join('imputation_strategies', filename)
                
                # Import the function from the file
                spec = importlib.util.spec_from_file_location(function, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Get the function and add it to the dictionary
                func = getattr(module, 'impute', None)
                if func:
                    self.imputationStrategies[function] = func
        
    def impute(self, data: pd.DataFrame, function: str = 'avgValue', tester: TRexDataTester = None) -> pd.DataFrame:
        """ Imputes data's faulty values

            Parameters:
            -----------
            function: str, default 'average'
                function used to impute
            data: pd.DataFrame
                data to impute
            tester: TRexDataTester, optional

            Returns:
            --------
            pd.DataFrame: imputed data
        """
        if tester is not None: tester.testAll(data)
        
        if function.endswith('py'): function = function[:-3]
        assert function in self.imputationStrategies, f"Imputation function {function} is not in self.imputationStrategies. See TRexImpute.functions() for guide"
        
        print(f"Imputing with: {function}()")
        imputedData = self.imputationStrategies[function](data)
        
        return imputedData
    
    def functions(self):
        """Describes imputation strategies"""
        print("Imputation functions: \n")
        for function in self.imputationStrategies:
            print(f"{function}(): {self.imputationStrategies[function]()}, \n")
        
        
if __name__ == '__main__':
    imputer = TRexImputer()
    
    data = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X', 'Y'])
    
    imputer.functions()
    
    print(imputer.impute(data))