import pandas as pd
import os
import numpy as np

# from data import table_data
# directory containing csv table files
relative_path = "data/table_data"
all_files = os.listdir(relative_path)
dataframes = []

def calc_velocity(point1, point2):
    """"""

    delta_x = point2["X"] - point1["X"]
    delta_y = point2["Y"] - point1["Y"]
    #print("delta_x: ", delta_x, "delta_y: ", delta_y)
    displacement = np.sqrt(delta_x**2 + delta_y**2)
    #print("displacement:", displacement)

    delta_time = point2["time"] - point1["time"]
    #print("delta_time:", delta_time)

    velocity = displacement / delta_time
    
    return velocity


     
def avg_velocity(df):
    V = []
    #print('length of df:',len(df))
    for i in range(1, len(df)):
        point2 = df.iloc[i]
        point1 = df.iloc[i - 1]
        V.append(calc_velocity(point1, point2))
    return V


#collect all the velocities and put in one vector

def all_velocity(df_list):
    all_v = []
    for df in df_list:
        v_vector = avg_velocity(df)
        all_v.extend(v_vector)
    return all_v
    


#plot the velocities as a continuous density function (or histogram)

import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(data, bins=10):
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel('Velocity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Velocities')
    plt.grid(True)
    plt.show()