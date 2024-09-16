import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_dtheta(vector1, vector2):
    cross_product = np.cross(vector1, vector2)

    def mag(v):
        return np.sqrt(np.dot(v, v))
    magA  = mag(vector1)
    magB = mag(vector2)
    dtheta = np.arcsin(cross_product[2] / (magA * magB))
    return dtheta



def running_sum(df):
    print('runing sum')
    dtheta_list = []
    dtheta =  0

    for i in range(1, len(df) - 1):
        # print('working on row', i)
        if np.isnan(df['X'].iloc[i]) or np.isnan(df['Y'].iloc[i]) or np.isnan(df['X'].iloc[i-1]) or np.isnan(df['Y'].iloc[i-1]) or np.isnan(df['X'].iloc[i+1]) or np.isnan(df['Y'].iloc[i+1]):
            continue
        else:
            vector_1  = np.array([df['X'].iloc[i] - df['X'].iloc[i-1], 
                                  df['Y'].iloc[i] - df['Y'].iloc[i-1],
                                  0])

            vector_2 = np.array([df['X'].iloc[i+1] - df['X'].iloc[i], 
                                 df['Y'].iloc[i+1] - df['Y'].iloc[i],
                                 0])
            # print('vector 1:', vector_1)
            # print('vector 2:', vector_2)
            single_theta = calculate_dtheta(vector_1, vector_2)
            if np.isnan(single_theta):
                continue
            else:
                # print('single theta:', single_theta)
                dtheta += single_theta
                dtheta_list.append(dtheta)
                # print('dtheta:', dtheta)
                # print('dtheta list:', dtheta_list)
                
    return dtheta_list


def rolling_avg(df, window):
    df_local = df.copy()
    """
    Calculate the rolling average for the columns 'X' and 'Y' in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The input dataframe containing 'time', 'X', and 'Y' columns.
    window (int): The window size for calculating the rolling average.
    
    Returns:
    pd.DataFrame: A dataframe with the rolling average applied to 'X' and 'Y'.
    """
    df_local[['X', 'Y']] = df_local[['X', 'Y']].rolling(window=window).mean()
    return df_local



def plot_trajectory(df, pin_start = True, return_figure = False, title = None):

    # add t0 t end markers
    """
    Plot the trajectory of a Daphnia in a dish using X and Y coordinates with a focus on more detail.
    
    Parameters:
    df (pd.DataFrame): The input dataframe containing 'X' and 'Y' columns representing positions.
    """
    plt.figure(figsize=(12, 8))
    
    # Creating a connected scatter plot with a very thin line and no markers
    plt.plot(df['X'], df['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
    
    # Adding titles and labels
    if title is not None:
        plt.title(title)
    else:
        plt.title('Detailed Trajectory of Daphnia in a Dish')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')

    #add a red marker at the start of the trajectory
    if pin_start:
        plt.plot(df['X'].iloc[0], df['Y'].iloc[0], 'ro', label='Start')
    
    # Inverting the y-axis to better represent traditional coordinate systems (optional)
    plt.gca().invert_yaxis()
    
    # Adding a legend
    plt.legend()
    
    # Display the plot
    plt.grid(True)
    if return_figure:
        return plt
    else:
        plt.show()