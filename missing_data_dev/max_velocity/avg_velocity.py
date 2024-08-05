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
    # use the pythagorean theorem to calculate the displacement
    delta_x = point2["X"] - point1["X"]
    delta_y = point2["Y"] - point1["Y"]
    print("delta_x: ", delta_x, "delta_y: ", delta_y)
    displacement = np.sqrt(delta_x**2 + delta_y**2)
    print("displacement:", displacement)
    # calculate the difference in time (delta)
    delta_time = point2["time"] - point1["time"]
    print("delta_time:", delta_time)
    # divide the displacement by the difference in time
    velocity = displacement / delta_time
    
    # return the velocity
    return velocity


#write a function that 
     
def avg_velocity(df):
    V = []
    for i in len(df) + 1:
    point2 = df(i)
    point1 = df(i - 1)
    V.append(calc_velocity(point1, point2))


    