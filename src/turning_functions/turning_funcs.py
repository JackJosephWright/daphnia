import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



def calculate_dtheta(vector1, vector2):
    """
    Calculate the angle between two vectors in the XY plane.

    Args:
    vector1 (np.array): The first vector.
    vector2 (np.array): The second vector.

    Returns:
    float: The angle between the two vectors.
    """
    if not all(isinstance(vector, np.ndarray) for vector in [vector1, vector2]):
        raise ValueError('Input vectors must be numpy arrays.')
    
    cross_product = np.cross(vector1, vector2)

    def magnitude(v):
        return np.sqrt(np.dot(v, v))
    
    magA = magnitude(vector1)
    magB = magnitude(vector2)
    
    if magA == 0 or magB == 0:
        return 0  # If magnitude is zero, no turning occurs
    
    # Calculate the sine of the angle, ensuring values stay in the range [-1, 1]
    sin_theta = np.clip(cross_product[2] / (magA * magB), -1.0, 1.0)
    dtheta = np.arcsin(sin_theta)
    
    return dtheta



def running_theta_sum(df):
    print('running sum')
    dtheta_list = [float(0)]
    dtheta =  0

    for i in range(1, len(df) - 1):

        # print df selecting rows i-1, i, i+1
        # if i > 0 and i < len(df) - 1:
            
        #     print(df.iloc[i-1:i+2])
        # else:
        #     print("Index out of range for selecting rows i-1, i, i+1")


        if np.isnan(df['X'].iloc[i]) or np.isnan(df['Y'].iloc[i]) or np.isnan(df['X'].iloc[i-1]) or np.isnan(df['Y'].iloc[i-1]) or np.isnan(df['X'].iloc[i+1]) or np.isnan(df['Y'].iloc[i+1]):
            print('nan value found in running sum')
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
            # print('computed theta value: ', single_theta)
            if np.isnan(single_theta):
                continue
            else:
                # print('single theta:', single_theta)
                dtheta += single_theta
                dtheta_list.append(dtheta)
                # print('dtheta:', dtheta)
                # print('dtheta list:', dtheta_list)
        # print('theta list is now: ', dtheta_list)
        # input('press enter to continue')
    # dtheta_list.append(float(0))
    dtheta_list.append(np.nan)
    return dtheta_list


def rolling_avg(df, window =50):
    df_local = df.copy()
    """
    Calculate the rolling average for the columns 'X' and 'Y' in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The input dataframe containing 'time', 'X', and 'Y' columns.
    window (int): The window size for calculating the rolling average.
    
    Returns:
    pd.DataFrame: A dataframe with the rolling average applied to 'X' and 'Y'.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError('Input must be a DataFrame.')
    cols = df_local.columns
    if 'X' not in cols or 'Y' not in cols:
        raise ValueError('Input DataFrame must contain columns "X" and "Y".')
    df_local[['X', 'Y']] = df_local[['X', 'Y']].rolling(window=window).mean()
    df_local = df_local.dropna().reset_index(drop=True)
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

    """
    select a window of theta values from a list of theta values based on the window size and the starting index.

    Args:
    theta_list (list): A list of theta values.
    window_size (int): The window size for selecting the theta values.
    start_idx (int): The starting index for selecting the theta values.
    second_scale (bool): Whether the window size is in seconds or samples.


    """

    if not all(isinstance(theta, (int, float)) for theta in theta_list):
        raise ValueError('Theta list must contain only numbers.')
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
    """
    Calculate the sign of the slope of a list of values.

    Args:
    chunk_list (list): A list of values.

    Returns:
    int: The sign of the slope.
    """
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



def count_turns (theta_list, window_size =30):
    """
    Count the number of turns in a list of theta values.

    Args:
    theta_list (list): A list of theta values.
    window_size (int): The window size for calculating the slope sign.

    Returns:
    int: The number of turns.
    """
    # check theta list is a list of numbers
    if not all(isinstance(theta, (int, float)) for theta in theta_list):
        raise ValueError('Theta list must contain only numbers.')
    
    if not isinstance(window_size, int):
        raise ValueError('Window size must be an integer.')
    window_list = grab_window(theta_list, window_size, start_idx=0)
    slope_list = []
    for window in window_list:
        slope_list.append(get_windowed_slope_sign(window))
    
    #get the difference between each element and the next element in slope_sign
    slope_diff = np.diff(slope_list)
    print('slope diff')
    print(slope_diff)
    turns = np.count_nonzero(slope_diff)
    turn_indexes = np.where(slope_diff != 0)[0]
    # turn_index_list = []
    # for index in turn_indexes:
    #     #multiply by window_size
    #     turn_index_list.append(((index+1)*window_size))
    # print('turn index_list:')
    turn_index_list = (turn_indexes+1)*window_size
    print(turn_index_list)
    return turns, turn_index_list, slope_list


def split_on_nan(df, column_name):
    """
    Splits the DataFrame into continuous segments wherever NaN is encountered in the specified column.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    column_name (str): The column to check for NaN values.
    
    Returns:
    list: A list of DataFrames with continuous segments.
    """
    # Create a list to store the continuous segments

    #replace any inf (empty output value from TRex) with nan
    try:
        df = df.replace([np.inf, -np.inf], np.nan)
    except:
        pass
    segments = []
    
    # Track the current segment
    current_segment = []

    for index, row in df.iterrows():
        if pd.isna(row[column_name]):
            # If we hit a NaN, append the current segment to the list and start a new one
            if current_segment:
                #reset index
                df = pd.DataFrame(current_segment).dropna().reset_index(drop=True)
                
                segments.append(df)
                
                current_segment = []  # Reset the current segment
        else:
            # Add the row to the current segment
            current_segment.append(row)

    # Don't forget to add the last segment if it exists
    if current_segment:
        segments.append(pd.DataFrame(current_segment))
    
    return segments





def plot_turns_and_path(segmented_data, turns, turn_index_list, running_theta,  slope_list,turn_window =30):

    """
    plot the path of the daphnia and the cumulative theta values with markers at the turns.

    Args:
    segmented_data (pd.DataFrame): Pre segmented data for continuous segments, from split_on_nan.
    turns (int): The number of turns from count_turns.
    turn_index_list (list): A list of indexes where turns occur from count_turns.
    running_theta (list): A list of cumulative theta values from running_theta_sum.
    turn_window (int): The window size for calculating the slope sign.
    slope_list (list): A list of slope signs from count_turn to determine the number of total segments


    Returns:
    plot: A plot of the path of the daphnia with markers
    """
    
    #makes a plot of the path and the location of the turns
    # Create the plot
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(12, 8))
    ax1.plot(segmented_data['X'], segmented_data['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
    # Add title
    #ax1.title('Detailed Trajectory of Daphnia in a Dish')


    # Add the text "Turns: {turns}" in the top-right corner (adjust x, y for placement)
    plt.text(0.8, 0.9, f'Turns: {turns}', fontsize=12, color='red', transform=plt.gca().transAxes)

    ax2.plot(running_theta, label = 'normalized theta')
 
    # find segmented_data['X'] and ['Y'] for each index in turn_index_list, put a mark there
    for index in turn_index_list:
        print('index:', index)
        print('x value: ', segmented_data['X'][index])
        print('y value: ', segmented_data['Y'][index])
        if isinstance(index, np.ndarray) or isinstance(index, list):
            for idx in index:
                ax1.scatter(segmented_data['X'][idx], segmented_data['Y'][idx], color = 'green', s = 50, zorder = 5)
                ax2.axvline(x = idx, color = 'green')
        else:
            ax1.scatter(segmented_data['X'][index], segmented_data['Y'][index], color = 'green', s = 50, zorder = 5)
            ax2.axvline(x = index, color = 'green')
    for i in range(len(slope_list)):
        idx = (i+1) * turn_window
        if idx < len(segmented_data):
            ax1.scatter(segmented_data['X'][idx], segmented_data['Y'][idx], color = 'red', s = 50)
    # Add a star marker at the starting point and label it
    #segmented_data = segmented_data.dropna().reset_index(drop = True)    
    start_x = segmented_data['X'][0]
    start_y = segmented_data['Y'][0]

    print('start_x val:', start_x)
    print('start_y val:', start_y)
    ax1.scatter(start_x, start_y, color='orange', marker='*', s=100, label='Start', zorder=10)
    ax1.text(start_x, start_y, 'Start', fontsize=12, color='orange', verticalalignment='bottom', horizontalalignment='right')

    # Add legend
    ax1.legend()

    # Add grid
    ax1.grid(True)

    
    ax2.set_xticks(np.arange(0, len(running_theta), turn_window))
   
    ax2.set_xlabel('time')
    ax2.set_ylabel('theta')

    ax2.legend()
    plt.tight_layout()

    # Display the plot
    plt.show()

def gen_turn_column(df_length, turn_index_list):
    """
    for generating the turn_id column for the generating_turning_df function
    
    Args:
    df_length: int, the length of the dataframe
    turn_index_list: list of ints, the indices where the turn direction changes
    
    Returns:
    turn_id_list: list of ints, the turn_id column
    """

    turn_id_list = []
    # print('total length of df:', df_length)
    if len(turn_index_list) == 0:
        turn_id_list = [0] * df_length
    else:
        # create the initial turn list up until the first change of direction
        turn_id_list = [0] * turn_index_list[0]
        # print('turn_id_list:', turn_id_list)
        for i in range(len(turn_index_list)):
            start_idx = turn_index_list[i]
            end_idx = turn_index_list[i+1] if i+1 < len(turn_index_list) else df_length

            turn_id_list.extend([i+1] * (end_idx - start_idx))
        
    return turn_id_list
def generate_turning_df(df, smoothing_window = 50, turn_window = 30):
    
    smoothed = rolling_avg(df, smoothing_window)
    #smoothed = smoothed.dropna().reset_index(drop=True)
    
    running_theta = running_theta_sum(smoothed)
    # print('df length:', len(smoothed))
    # print('running_theta_length: ', len(running_theta))
    # create tidy df which is smoothed with running theta as an additional column
    tidy_df = smoothed
    tidy_df['running_theta'] = running_theta
    turns, turn_index_list, slope_list =  count_turns(running_theta, turn_window)
    print('turn index list after return:')
    print(turn_index_list)  
    df_length = len(tidy_df)
    turn_col = gen_turn_column(df_length, turn_index_list)
    tidy_df['turn_id'] = turn_col
    print('unique vals in turn_id:', tidy_df['turn_id'].unique())
    return tidy_df


# def plot_turns_and_path(segmented_data, turns, turn_index_list, running_theta, turn_window, slope_list):
#     # Create the plot
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
#     ax1.plot(segmented_data['X'], segmented_data['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)

#     # Add the text "Turns: {turns}" in the top-right corner (adjust x, y for placement)
#     plt.text(0.8, 0.9, f'Turns: {turns}', fontsize=12, color='red', transform=plt.gca().transAxes)

#     # Plot running theta on ax2
#     ax2.plot(running_theta, label='normalized theta')

#     # Mark turns with green dots
#     for index in turn_index_list:
#         if isinstance(index, np.ndarray) or isinstance(index, list):
#             for idx in index:
#                 ax1.scatter(segmented_data['X'][idx], segmented_data['Y'][idx], color='green', s=50, zorder=5)
#                 ax2.axvline(x=idx, color='green')
#         else:
#             ax1.scatter(segmented_data['X'][index], segmented_data['Y'][index], color='green', s=50, zorder=5)
#             ax2.axvline(x=index, color='green')

#     # Mark slope list points with red dots
#     for i in range(len(slope_list)):
#         idx = (i + 1) * turn_window
#         if idx < len(segmented_data):
#             ax1.scatter(segmented_data['X'][idx], segmented_data['Y'][idx], color='red', s=50)

#     # Add a star marker at the starting point and label it
#     start_x = segmented_data['X'].iloc[0]
#     start_y = segmented_data['Y'].iloc[0]
#     ax1.scatter(start_x, start_y, color='orange', marker='*', s=100, label='Start', zorder=10)
#     ax1.text(start_x, start_y, 'Start', fontsize=12, color='orange', verticalalignment='bottom', horizontalalignment='right')

#     # Add legend and grid to ax1
#     ax1.legend()

#     # Ensure the marker is visible by adjusting the axis limits if necessary
#     ax1.set_xlim(min(segmented_data['X']) - 10, max(segmented_data['X']) + 10)
#     ax1.set_ylim(min(segmented_data['Y']) - 10, max(segmented_data['Y']) + 10)

#     ax1.grid(True)

#     # Customize ax2 (theta plot)
#     ax2.set_xlabel('time')
#     ax2.set_ylabel('theta')
#     ax2.legend()

#     plt.tight_layout()

#     # Display the plot
#     plt.show()