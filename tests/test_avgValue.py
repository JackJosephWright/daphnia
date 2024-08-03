import numpy as np
import pandas as pd

from imputation_strategies import avgValue

sampleData = pd.DataFrame.from_dict({
    'time': [0, 1, 2, 3, 4, 5, 6, 7],
    'X': [0, 1, 2, 'infinity', 'infinity', 'infinity', 6, 7],
    'Y': [0, 1, 2, 'infinity' , 'infinity', 'infinity', 6, 7]
})

print(avgValue.impute(sampleData))

