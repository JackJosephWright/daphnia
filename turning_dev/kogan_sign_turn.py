# this loads the smoothed data for testing dr kogans turn demarcation idea

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs



smooth_df = pd.read_csv('smoothed_data.csv')
segmented_data = smooth_df[4060:4600]
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


window = 20 

def grab_window(theta_list, window_size, start_idx):
    half_window = window_size // 2
    
    if start_idx < half_window:
        # write an error that the window is too close to the beginning
        print("Error: The window is too close to the beginning.")
        return False
    
    if start_idx + half_window >= len(theta_list):
        # write an error that the window is too close to the end
        print("Error: The window is too close to the end.")
        return False
    
    window = theta_list[start_idx - half_window: start_idx + half_window]
    return window

def sign_of_angle(theta):
    if theta > 0:
        return 1
    else:
        return -1

test_list = [20,10,4,5,6,14,165,-10,-4,-40,-110,-1231,-1230321]

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def get_windowed_slope(df, sign_only = False):

    if sign_only:
        slope  = df['theta'].apply(sign_of_angle).sum()
        return slope, None
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['theta'].values
    
    # Perform linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict the values
    y_pred = model.predict(X)
    
    # Calculate slope
    slope = model.coef_[0]
    
    # get r_squared
    variance = r2_score(y, y_pred)
    
    return slope, variance

for i in range(len(test_list)):
    window = grab_window(test_list, 4, i)
    # print('new window')
    # print(window)
    if window:
        # print('new df window:')
        df_window = pd.DataFrame(window)
        df_window.columns = ['theta']
        slope, rsq = get_windowed_slope(df_window)
        # print('slope:', slope)
        # print('r squared:', rsq)
    else:
        slope = None
        rsq = None


def generate_slope_and_variance_df(theta_list, window_size = 30, sign_only = False):
    slope_theta_df = pd.DataFrame(columns = ['slope', 'r_squared'])
    for i in range(len(theta_list)):
        window = grab_window(theta_list, window_size, i)
        if window:
            df_window = pd.DataFrame(window)
            df_window.columns = ['theta']
            slope, rsq = get_windowed_slope(df_window, sign_only)
            slope_theta_df = slope_theta_df._append({'slope': slope, 'r_squared': rsq}, ignore_index = True)
        else:
            slope_theta_df = slope_theta_df._append({'slope': None, 'r_squared': None}, ignore_index = True)
    return slope_theta_df


slope_theta_df = generate_slope_and_variance_df(running_theta)
sign_sum_theta_df = generate_slope_and_variance_df(running_theta, sign_only = True)
#print(slope_theta_df)



# Normalize the data to bring them to a similar scale
def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# Normalize all three series
normalized_running_theta = normalize(running_theta)
normalized_slope = normalize(slope_theta_df['slope'])
normalized_r_squared = normalize(slope_theta_df['r_squared'])
normalized_sign_sum = normalize(sign_sum_theta_df['slope'])

print('normed vals')
print(normalized_running_theta)
print(normalized_slope)
print(normalized_r_squared)




#make a figure with 2 subplots



fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

#plot the trajectory
ax1.plot(segmented_data['X'], segmented_data['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
ax1.set_title('Detailed Trajectory of Daphnia in a Dish')
ax1.set_xlabel('X Position')
ax1.set_ylabel('Y Position')
ax1.invert_yaxis()
ax1.legend()
ax1.grid(True)

#plot the running sum
ax2.plot(normalized_running_theta, label='Normalized Running Theta')
ax2.set_xlabel('Time')
ax2.set_ylabel('Running Sum')
ax2.grid(True)

ax2.plot(normalized_slope, label='Normalized Slope')
ax2.set_xlabel('Time')
ax2.set_ylabel('Running Sum')
ax2.grid(True)

ax2.legend()

plt.tight_layout()
plt.show()