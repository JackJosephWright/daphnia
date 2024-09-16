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

def rolling_avg(df, window):
    df_local = df.copy()
    df_local[['X', 'Y']] = df_local[['X', 'Y']].rolling(window=window).mean()
    return df_local

# Apply rolling average with a specified window size
window_size = 10  # Adjust this window size as needed
r1 = rolling_avg(cleanedData, window_size)

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

# Run the running_sum function on the cleaned real data
dtheta_list = running_sum(r1)


#plot the dtheta_list
plt.plot(dtheta_list)
plt.show()



# Generate time data (200 samples)
time = np.linspace(0, 20, 200)

# Generate X and Y for a continuous right-hand curve (e.g., a quarter circle)
radius = 10
theta = np.linspace(0, np.pi / 2, 200)  # Angle going from 0 to 90 degrees

# X and Y values for the curve
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Create the DataFrame
synthetic_data = pd.DataFrame({
    'time': time,
    'X': x,
    'Y': y
})



synthetic_right = running_sum(synthetic_data)

# Plot the synthetic data
plt.plot(synthetic_right)
plt.show()




# Generate time data (200 samples)
time = np.linspace(0, 20, 200)

# Generate X and Y for a continuous left-hand curve (e.g., a quarter circle)
radius = 10
theta = np.linspace(np.pi / 2, np.pi, 200)  # Angle going from 90 to 180 degrees

# X and Y values for the left-hand curve
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Create the DataFrame
synthetic_data_left = pd.DataFrame({
    'time': time,
    'X': x,
    'Y': y
})

# Apply running_sum on the left-hand curve data
synthetic_left = running_sum(synthetic_data_left)

# Plot the synthetic left-hand turn data
plt.plot(synthetic_left)
plt.title("Cumulative dtheta for Left-hand Turn")
plt.xlabel("Sample Index")
plt.ylabel("Cumulative dtheta (radians)")
plt.grid(True)
plt.show()
