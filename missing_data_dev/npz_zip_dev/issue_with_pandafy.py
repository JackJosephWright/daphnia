
"""
take a look at the npz file and the subfiles. We need to extract the relevant file (maybe timestamp X and Y to create the df)
"""


from ..npz_zip_dev import zip
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
npz_path = r"C:\Users\jwright\Documents\GitHub\daphnia\data\npz_file\small_100_fish0.npz"



#use np.load to load the npz file
data = np.load(npz_path)



timestamp = data['timestamp']

X = data['X']
Y = data['Y']

