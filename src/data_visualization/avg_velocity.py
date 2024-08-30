import pandas as pd
import os
import numpy as np

def calc_velocity(point1, point2):
    """
    Calculates the velocity between two points based on their X, Y coordinates and time

    Parameters:
    -----------
    point1 : pd.Series
        The first point containing 'X', 'Y', and 'time' values
    point2 : pd.Series
        The second point containing 'X', 'Y', and 'time' values

    Returns:
    --------
    float
        The calculated velocity between the two points
    """
    delta_x = point2["X"] - point1["X"]
    delta_y = point2["Y"] - point1["Y"]

    displacement = np.sqrt(delta_x**2 + delta_y**2)

    delta_time = point2["time"] - point1["time"]

    velocity = displacement / delta_time
    return velocity


def avg_velocity(df):
    """
    Calculates the average velocity between consecutive points in a DataFrame

    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame containing 'X', 'Y', and 'time' columns

    Returns:
    --------
    list
        A list of velocities between consecutive points in the DataFrame
    """
    V = []
    for i in range(1, len(df)):
        point2 = df.iloc[i]
        point1 = df.iloc[i - 1]
        V.append(calc_velocity(point1, point2))
    return V


def all_velocity(df_list):
    """
    Collects all velocities from a list of DataFrames and returns them as a single list

    Parameters:
    -----------
    df_list : list
        A list of DataFrames, each containing 'X', 'Y', and 'time' columns

    Returns:
    --------
    list
        A list of all velocities calculated from the DataFrames
    """
    all_v = []
    for df in df_list:
        v_vector = avg_velocity(df)
        all_v.extend(v_vector)
    return all_v
    


import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(data, bins=10):
    """
    Plots a histogram of the given data, representing the distribution of velocities

    Parameters:
    -----------
    data : list
        A list of velocity values to be plotted
    bins : int, optional
        The number of bins to use in the histogram (default is 10)
    """
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel('Velocity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Velocities')
    plt.grid(True)
    plt.show()
