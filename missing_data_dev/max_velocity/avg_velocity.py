import pandas as pd
import os
import numpy as np

# from data import table_data

# directory containing csv table files
direct_path = "/Users/ibrahimrahat/Documents/GitHub/daphnia/data/table_data"

all_files = os.listdir(direct_path)

dataframes = []

def calc_velocity(point1, point2):
    print("point 1:", point1)
    print("point 2:", point2)

    delta_x = point2["X"] - point1["X"]
    delta_y = point2["Y"] - point1["Y"]
    print("delta_x: ", delta_x, "delta_y: ", delta_y)
    displacement = np.sqrt(delta_x**2 + delta_y**2)
    print("displacement:", displacement)

    delta_time = point2["time"] - point1["time"]
    print("delta_time:", delta_time)

    velocity = displacement / delta_time
    
    return velocity


     
def avg_velocity(df):
    V = []
    print('length of df:',len(df))
    for i in range(1, len(df)):
        # print(i)
        point2 = df.iloc[i]
        point1 = df.iloc[i - 1]
        # print('point 1:', point1)
        # print('point 2:', point2)
        V.append(calc_velocity(point1, point2))
    return V


#collect all the velocities and put in one vector

def all_velocity(df):
    all_v = []
    

#get avg velocity with standard deviation 


#plot the velocities as a ccontinuous density function (or histogram)