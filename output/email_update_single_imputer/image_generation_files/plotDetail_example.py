# Import necessary tools
from src.data_manipulation.plotDetail import plotDetail
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# Copy the path of the NPZ file
npz_path = r"data/npz_file/single_7_9_fish1.MP4_fish0.npz"

# Use np.load to load the npz file
data = np.load(npz_path)


