#import pytest
import numpy as np
import pandas as pd
# Import classes from src/data_manipulation
from src.data_manipulation.TRexDataTester import TRexDataTester
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_manipulation.TRexImputer import TRexImputer
from src.imputation_strategies import avgValue

imputer = TRexImputer()

sampleData = pd.DataFrame.from_dict({
    'time': [0, 1, 2, 'infinity', 'infinity', 'infinity', 6, 7],
    'X#wcentroid': [0, 1, 2, 'infinity', 'infinity', 'infinity', 6, 7],
    'Y#wcentroid': [0, 1, 2, 'infinity' , 'infinity', 'infinity', 6, 7]
})

print(imputer.impute(sampleData))