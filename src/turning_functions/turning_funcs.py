import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression




def calculate_dtheta(vector1, vector2):
    cross_product = np.cross(vector1, vector2)

    def mag(v):
        return np.sqrt(np.dot(v, v))
    magA  = mag(vector1)
    magB = mag(vector2)
    dtheta = np.arcsin(cross_product[2] / (magA * magB))
    return dtheta



def running_theta_sum(df):
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





def grab_window(theta_list, window_size, start_idx, second_scale = False):
    window_list = []
    if second_scale:
        time_per_sample = 1/30
        #this is here for when we switch to time as opposed to sample
        chunk_size = window_size/time_per_sample
    else:
        chunk_size = window_size
    n_chunks = len(theta_list) // chunk_size
    chunk = 0
    while (chunk < n_chunks):
        theta_list_chunk = theta_list[chunk*chunk_size:(chunk+1)*chunk_size]
        window_list.append(theta_list_chunk)
        chunk += 1
    return window_list



def get_windowed_slope_sign(chunk_list):
    X = np.arange(len(chunk_list)).reshape(-1, 1)
    y = chunk_list
    # Perform linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict the values
    y_pred = model.predict(X)
    
    # Calculate slope
    slope = model.coef_[0]
    
    slope_sign = np.sign(slope)
    return slope_sign



def count_turns (theta_list, window_size):
    window_list = grab_window(theta_list, window_size, start_idx=0)
    slope_list = []
    for window in window_list:
        slope_list.append(get_windowed_slope_sign(window))
    
    #get the difference between each element and the next element in slope_sign
    slope_diff = np.diff(slope_list)
    print(slope_diff)
    turns = np.count_nonzero(slope_diff)
    turn_indexes = np.where(slope_diff != 0)
    turn_index_list = []
    for index in turn_indexes:
        #multiply by window_size
        turn_index_list.append((index*window_size))
    print('turn index_list:')
    print(turn_index_list)
    return turns, turn_index_list
        



def plot_turns_and_path(segmented_data, turns, turn_index_list):
    #makes a plot of the path and the location of the turns
    # Create the plot
    plt.plot(segmented_data['X'], segmented_data['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
    # Add title
    plt.title('Detailed Trajectory of Daphnia in a Dish')


    # Add the text "Turns: {turns}" in the top-right corner (adjust x, y for placement)
    plt.text(0.8, 0.9, f'Turns: {turns}', fontsize=12, color='red', transform=plt.gca().transAxes)


    # find segmented_data['X'] and ['Y'] for each index in turn_index_list, put a mark there
    for index in turn_index_list:
        plt.scatter(segmented_data['X'][index], segmented_data['Y'][index], color='green', s=50, zorder=5)

    # Invert Y-axis
    plt.gca().invert_yaxis()

    # Add legend
    plt.legend()

    # Add grid
    plt.grid(True)

    # Display the plot
    plt.show()