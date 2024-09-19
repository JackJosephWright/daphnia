# this loads the smoothed data for testing dr kogans turn demarcation idea

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression



from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs



smooth_df = pd.read_csv('smoothed_data.csv')
start = 3900
end = 4200
window = 20
segmented_data = smooth_df[start:end]
running_theta = turning_funcs.running_theta_sum(segmented_data)

"""
Jack,

So, I have a proposal for the algorithm to count CW and CCW pieces.

We select a window of time that's much larger than the typical time of small fluctuations, but much smaller than the typical time of a rotation.  Here, such a window would be 20 seconds.  
In each window we measure the sign of the slope: 1 or -1.  

This results in a string of 1 and -1.  In your example, such a string would be  +1, +1, +1, -1, -1, -1, -1.

Every time there's a change from +1 to -1 or the other way around - that's a change from CW to CCW or vice versa.  

And we just count these changes.

This algorithm is based on three assumptions that there is such a thing as a typical time of rotations, and that there is such a thing as a typical time of noise fluctuations, and that these timescales remain sell-separated.  

Ultimately, we just have to try this idea and see how well it works on various videos. 

Oleg.
"""




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

window_list = grab_window(running_theta, window, start_idx=0)


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
        turn_index_list.append((index*window_size)+start)
    print('turn index_list:')
    print(turn_index_list)
    return turns, turn_index_list
        
turns, turn_index_list = count_turns(running_theta, window)
print(turns)




def plot_turns_and_path(segmented_data, turns, turn_index_list):
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
