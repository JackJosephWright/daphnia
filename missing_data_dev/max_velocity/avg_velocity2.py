import pandas as pd
import os
import numpy as np

# from data import table_data

# directory containing csv table files
direc_path = "/Users/ibrahimrahat/Documents/GitHub/daphnia/data/table_data"

all_files = os.listdir(direc_path)

dataframes = []

# loop through csv files and read each one 
for file in all_files:
    file_path = os.path.join(direc_path, file)
    # print(file_path)
    df = pd.read_csv(file_path)
    dataframes.append(df)

first_dataframe = dataframes[0]
# print(first_dataframe)


def calc_avg_velocity(df):

    x = df['X']
    y = df['Y']
    time = df['time']
    time = time / 100000
    # differences in positions (displacements)
    delta_x = x.diff().iloc[1:]
    delta_y = y.diff().iloc[1:]
    # print(delta_x)
    # print(delta_y)
    
    # Euclidean distance (total displacement)
    displacement = np.sqrt(delta_x**2 + delta_y**2)
    # print(displacement)

    # differences in time
    delta_time = time.diff().iloc[1:]
    # print(delta_time)

    # instantaneous velocities
    velocity = displacement / delta_time
    # print(velocity)

    avg_velocity = velocity.mean()

    return avg_velocity


# calculate average velocities in all dataframes
total_avg_velocity = [calc_avg_velocity(df) for df in dataframes]
"wont calculate avg_velocity for tables with one value of data, most likely bc of iloc[1:]"

# loop thru and print it
for i, avg_velo in enumerate(total_avg_velocity):
    print(f"Average Velocity for file {i+1}: {avg_velo:.2f}")



# print(calc_avg_velocity(df))





