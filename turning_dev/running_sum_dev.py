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


v1 = [1,0,0]
v2 = [0,1,0]

print(calculate_dtheta(v1, v2)) # expect pi/2

v1 = [0,1,0]
v2 = [1,0,0]

print(calculate_dtheta(v1, v2)) # expect -pi/2




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



# Define the data points
data = {
    'time': [0, 1, 2, 3, 0, 1, 2, 3],
    'X': [0, 1, 0, -1, 0, 1, 0, -1],
    'Y': [1, 0, -1, 0, 1, 0, -1, 0],
    'Z': [0, 0, 0, 0, 0, 0, 0, 0]  # Z is always 0
}

# Create the DataFrame
df_right = pd.DataFrame(data)

print(running_sum(df_right))

#plot df_right
plt.plot(running_sum(df_right))
plt.title('Running Sum of Right Turn')
plt.show()

data_left = {
    'time': [0, 1, 2, 3, 4, 5, 6, 7],
    'X': [1, 0, -1, 0, 1, 0, -1, 0],
    'Y': [0, 1, 0, -1, 0, 1, 0, -1],
    'Z': [0, 0, 0, 0, 0, 0, 0, 0]  # Z is always 0
}
df_left = pd.DataFrame(data_left)
plt.plot(running_sum(df_left))
plt.title('Running Sum of Left Turn')
plt.show()



from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Initialize the data cleaner
dataCleaner = TRexDataCleaner()

# Load and clean the real data
faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)


# Apply rolling average with a specified window size
window_size = 10  # Adjust this window size as needed
r1_sum = running_sum(cleanedData)

# plt.plot(r1_sum)
# plt.title('Running Sum of Real Data')
# plt.show()


# Apply rolling average with a specified window size



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


window_size = 3  # Adjust this window size as needed
r2 = rolling_avg(cleanedData, window_size)
r2_sum = running_sum(r2)

#plot r1_sum and r2_sum on the same plot
plt.plot(r1_sum, label='Real Data')
plt.plot(r2_sum, label='Rolling Average Data')
plt.title('Running Sum of Real Data and Rolling Average Data')

plt.legend()
plt.show()