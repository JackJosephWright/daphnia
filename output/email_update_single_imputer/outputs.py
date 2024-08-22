# Import necessary tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from src.data_manipulation.NPZer import NPZer

NPZer = NPZer()

# Set desired parameters
SOURCE_DIR = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz'
PARAMS = ['time', 'X', 'Y']
INVERT_Y = True

# Unzip and turn data into a pandas table
unzippedData = NPZer.pandafy(source_dir=SOURCE_DIR, invertY=INVERT_Y, params=PARAMS)

# Unzip to nparray
unzippedData = NPZer.unzipNpz(source_dir=SOURCE_DIR, params=PARAMS)

# Print data in form of pandas table
print('TRex Data:\n', unzippedData)

# Import necessary tools
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner

dataCleaner = TRexDataCleaner()

# Set desired parameters
VMAX = 20

# Set sample of original data
originalData = unzippedData.reset_index(drop=True)

# Print sample of original data
print('Original Data:\n', originalData)

originalData = pd.DataFrame({
    'X': [1.0, 2.0, 10.0, 4.0],
    'Y': [1.0, 2.0, 10.0, 4.0],
    'time': [0.0, 1.0, 2.0, 3.0]
})

# Clean data
cleanedData, removedData = dataCleaner.renderDiscontinuities(data=originalData, vmax=VMAX)

# Print cleaned data
print('Cleaned Data:\n', cleanedData)

# Import necessary tools
from src.data_manipulation.TRexImputer import TRexImputer

imputer = TRexImputer()

# Set desired parameters
DATA = pd.DataFrame({
    'X': [1.0, 2.0, np.inf, 4.0],
    'Y': [1.0, 2.0, np.inf, 4.0],
    'time': [0.0, 1.0, 2.0, 3.0]
})
FUNCTION = 'avgValue'

# Impute data
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