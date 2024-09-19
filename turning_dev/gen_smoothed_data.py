from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs
dataCleaner = TRexDataCleaner()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
print(f"Faulty Data: \n {faultyData}")

cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)
print("Cleaned Data: \n", cleanedData)
print("Removed Data: \n", removedData)

smoothed = turning_funcs.rolling_avg(cleanedData, 10)



#save the smoothed data 

smoothed.to_csv('smoothed_data.csv')


