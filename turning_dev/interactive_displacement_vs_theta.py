import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs

# Initialize the data cleaner
dataCleaner = TRexDataCleaner()

# Load and clean the data
faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)
smoothed = turning_funcs.rolling_avg(cleanedData, 10)

# Define the interactive plotting function
def interactive_plot(start, end):
    # Ensure valid range
    if start >= end:
        print("Start index must be less than end index.")
        return
    
    # Slice the data
    segmented_data = smoothed[start:end]
    
    # Calculate running sum
    sum_1 = turning_funcs.running_sum(segmented_data)
    
    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot the trajectory
    ax1.plot(segmented_data['X'], segmented_data['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
    ax1.set_title('Detailed Trajectory of Daphnia in a Dish')
    ax1.set_xlabel('X Position')
    ax1.set_ylabel('Y Position')
    ax1.invert_yaxis()
    ax1.legend()
    ax1.grid(True)
    
    # Plot the running sum
    ax2.plot(sum_1)
    ax2.set_title('Running Sum of dtheta')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Running Sum')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# Create sliders for start and end points
start_slider = IntSlider(min=0, max=len(smoothed)-1, step=1, value=4060, description='Start')
end_slider = IntSlider(min=0, max=len(smoothed)-1, step=1, value=4200, description='End')

# Use interact to update the plot based on slider values
interact(interactive_plot, start=start_slider, end=end_slider)
