# Import necessary tools
import pytest
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from missing_data_dev.max_velocity.avg_velocity import calc_velocity, avg_velocity, all_velocity, plot_histogram

# Create and declare the directory for all the CSV files
#direct_path = "/Users/ibrahimrahat/Documents/GitHub/daphnia/data/table_data"
relative_path = "data/table_data"
all_files = os.listdir(relative_path)

# Create an empty dataframe
dataframes = []

# Loop through and have pandas read each CSV file
for file in all_files:
    file_path = os.path.join(relative_path, file)
    df = pd.read_csv(file_path)
    dataframes.append(df)



# Use the function all_velocity and store all the velocities into a variable
all_velo = all_velocity(dataframes)

# Plot the velocities in a histogram
plot_histogram(all_velo)