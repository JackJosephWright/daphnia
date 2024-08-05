# Import necessary tools
import pandas as pd
import numpy as np
from src.data_manipulation.NPZer import NPZer

NPZer = NPZer()

# Set desired parameters
SOURCE_DIR = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz'
INVERT_Y = True
PARAMS = ['time', 'X', 'Y']

# Unzip and turn data into a pandas table
unzippedData = NPZer.pandafy(source_dir=SOURCE_DIR,
                              invertY=INVERT_Y,
                              params=PARAMS)

# Print data in form of pandas table
print('TRex Data:\n', unzippedData)

# Import necessary tools
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner

dataCleaner = TRexDataCleaner()

# Set desired parameters
VMAX = 10

# Set sample of original data
originalData = unzippedData[:25].reset_index(drop=True)

# Print sample of original data
print('Original Data:\n', originalData)

# Clean data
cleanedData, removedData = dataCleaner.renderDiscontinuities(data=originalData, vmax=VMAX)

# Print cleaned data
print('Cleaned Data:\n', cleanedData)

# Import necessary tools
from src.data_manipulation.TRexImputer import TRexImputer

imputer = TRexImputer()

# Set desired parameters
DATA = cleanedData
FUNCTION = 'avgValue'

# Print original data
print('Original Data:\n', cleanedData)

# Impute data
imputedData = imputer.impute(data=DATA, function=FUNCTION)

# Print imputed data
print('Imputed Data:\n', imputedData)