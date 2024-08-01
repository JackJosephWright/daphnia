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
    
# first_dataframe = dataframes[0]
# print(first_dataframe)

x = df['X']
y = df['Y']
time = df['time']






# for i in dataframes:

