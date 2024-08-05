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
# print(calc_velocity(p1,p2))
print(avg_velocity(first_dataframe))

#make synthetic dataframe

#test it check that its right


# Generate synthetic data
# def generate_synthetic_data():
#     data = {
#         'X': [0, 1, 2, 3, 4],
#         'Y': [0, 1, 2, 3, 4],
#         'time': [0, 1, 2, 3, 4]
#     }
#     df = pd.DataFrame(data)
#     return df

# # Test the avg_velocity function
# df = generate_synthetic_data()
# print("Synthetic Data:\n", df)

# velocities = avg_velocity(df)
# print("Calculated Velocities:\n", velocities)