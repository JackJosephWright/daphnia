# Import necessary tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from src.data_manipulation.NPZer import NPZer

SOURCE_DIR = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz'
PARAMS = ['time', 'X', 'Y']
INVERT_Y = True


npzer = NPZer()
unzippedData = NPZer.pandafy(source_dir=SOURCE_DIR, invertY=INVERT_Y, params=PARAMS)

# Print data in form of pandas table
print('TRex Data:\n', unzippedData)

# Import necessary tools
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner

dataCleaner = TRexDataCleaner()
VMAX = 15

if TRexDataCleaner.isDiscontinuity(pi=unzippedData.loc[2], pf=unzippedData.loc[3], vmax=VMAX):
    unzippedData.drop(3)

# Print cleaned data
print('Cleaned Data:\n', cleanedData)

# Import necessary tools
from src.data_manipulation.TRexImputer import TRexImputer

imputer = TRexImputer()

DATA = pd.DataFrame({
    'X': [1.0, 2.0, np.inf, 4.0],
    'Y': [1.0, 2.0, np.inf, 4.0],
    'time': [0.0, 1.0, 2.0, 3.0]
})
FUNCTION = 'avgValue'

imputedData = imputer.impute(data=DATA, function=FUNCTION)


# Print original data
print('Original Data:\n', cleanedData)

# Print imputed data
print('Imputed Data:\n', imputedData)
plt.plot(imputedData['X'], imputedData['Y'])
plt.show()





import pandas as pd
from src.data_manipulation.NPZer import NPZer

DATA = pd.DataFrame({
    'X': [1, 2, 3, 4],
    'Y': [1, 2, 3, 4],
    'time': [0, 1, 2, 3]
})
SAVE_DIR = 'data/zipped.npz'
PARAMS = ['X', 'Y', 'time']

npzer = NPZer()
npzer.npzip(data=DATA, save_dir=SAVE_DIR, params=PARAMS)

from src.data_manipulation.calculateVelocity import calculateVelocity
import pandas as pd

data = pd.DataFrame({
    'X': [1, 2, 3, 4],
    'Y': [1, 2, 3, 4],
    'time': [0, 1, 2, 3]
})

calculateVelocity(pi=data.loc[0], pf=data.loc[1])