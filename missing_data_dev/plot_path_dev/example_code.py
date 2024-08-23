# tests/test_visualizer.py
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# Import classes from src/data_manipulation

from src.data_manipulation.TRexDataTester import TRexDataTester
from src.data_manipulation.NPZer import NPZer

data = NPZer.unzipNpz(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', params = ['time', 'X', 'Y'])
    
tester = TRexDataTester(timeTracked = True, dtype = np.floating)
tester.testAll(data)
    
# print("Unzipped data:\n", data)

from missing_data_dev.plot_path_dev.visualizer import DaphniaAnimation

pandasData = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X', 'Y'], )

animation = DaphniaAnimation(df=pandasData, start_index=3320)
animation.create_animation()






from  missing_data_dev.max_velocity.split_table_dev import split_table
import pandas as pd

clean_data = r"data/clean_fish_data/fish_data_clean.csv"

df = pd.read_csv(clean_data)

# set save_to_folder to True if you want to create a folder of tables in explorer 
tables = split_table(df, save_to_folder=False, folder_path='output_folder')

# can choose index of what table you want to access
first_table = tables[0]
print(first_table)

# prints number of tables
num_tables = len(tables)
print(num_tables)






import numpy as np
import os
import pandas as pd
from missing_data_dev.max_velocity.avg_velocity import all_velocity, plot_histogram

# directory containing csv table files
direct_path = r'data/table_data'
all_files = os.listdir(direct_path)

dataframes = []

# loop through csv files and read each one 
for file in all_files:
    file_path = os.path.join(direct_path, file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

# calculates velocities of all tables
all_velo = all_velocity(dataframes)

# plots histogram of all calculated velocities
plot_histogram(all_velo)