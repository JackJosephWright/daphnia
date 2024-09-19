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
segmented_data = smoothed[4060:4200]
return_plot = turning_funcs.plot_trajectory(segmented_data, return_figure = True)


sum_1 = turning_funcs.running_theta_sum(segmented_data)



#make a figure with 2 subplots

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

#plot the trajectory
ax1.plot(segmented_data['X'], segmented_data['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
ax1.set_title('Detailed Trajectory of Daphnia in a Dish')
ax1.set_xlabel('X Position')
ax1.set_ylabel('Y Position')
ax1.invert_yaxis()
ax1.legend()
ax1.grid(True)

#plot the running sum
ax2.plot(sum_1)
ax2.set_title('Running Sum of dtheta')
ax2.set_xlabel('Time')
ax2.set_ylabel('Running Sum')
ax2.grid(True)

plt.tight_layout()
plt.show()