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

print(all_files)