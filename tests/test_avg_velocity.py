import pytest
import numpy as np
import os
import pandas as pd
# Import classes from src/data_manipulation
# from src.data_manipulation.NPZer import NPZer
# from src.data_manipulation.TRexDataTester import TRexDataTester

from missing_data_dev.max_velocity.avg_velocity import calc_velocity, avg_velocity
# directory containing csv table files
direct_path = "/Users/ibrahimrahat/Documents/GitHub/daphnia/data/table_data"

all_files = os.listdir(direct_path)

dataframes = []

# loop through csv files and read each one 
for file in all_files:
    file_path = os.path.join(direct_path, file)
    # print(file_path)
    df = pd.read_csv(file_path)
    dataframes.append(df)
    # break

first_dataframe = dataframes[0]
# print(first_dataframe)
p1 = first_dataframe.iloc[0]
p2 = first_dataframe.iloc[1]
print('first df :', first_dataframe)
print(calc_velocity(p1,p2))
