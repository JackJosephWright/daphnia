import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt


from missing_data_dev.max_velocity.avg_velocity import calc_velocity, avg_velocity, all_velocity, plot_histogram
# directory containing csv table files
#direct_path = "/Users/ibrahimrahat/Documents/GitHub/daphnia/data/table_data"
direct_path = r'data/table_data'
all_files = os.listdir(direct_path)

dataframes = []

# loop through csv files and read each one 
for file in all_files:
    file_path = os.path.join(direct_path, file)
    # print(file_path)
    df = pd.read_csv(file_path)
    dataframes.append(df)

first_dataframe = dataframes[0]
p1 = first_dataframe.iloc[0]
p2 = first_dataframe.iloc[1]
#print('first df :', first_dataframe)
print(calc_velocity(p1,p2))
all_velo = all_velocity(dataframes)


plot_histogram(all_velo)


# # Generate synthetic data
# def generate_synthetic_data():
#     data = {
#         'X': [0, 1, 2, 3, 4],
#         'Y': [0, 1, 2, 3, 4],
#         'time': [0, 1, 2, 3, 4]
#     }
#     df = pd.DataFrame(data)
#     return df
# synth1 = generate_synthetic_data()
# synth2 = generate_synthetic_data()

# df_list = [synth1, synth2]

# synthetic_velocities = all_velocity(df_list)
# print('synthetic velos:', synthetic_velocities)

# plot_histogram(synthetic_velocities)
# # Test the avg_velocity function
# df = generate_synthetic_data()
# print("Synthetic Data:\n", df)

# velocities = avg_velocity(df)
# print("Calculated Velocities:\n", velocities)