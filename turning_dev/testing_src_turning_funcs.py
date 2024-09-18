from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs

dataCleaner = TRexDataCleaner()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
print(f"Faulty Data: \n {faultyData}")

cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)
print("Cleaned Data: \n", cleanedData)
print("Removed Data: \n", removedData)





# Define the data points
data = {
    'time': [0, 1, 2, 3, 0, 1, 2, 3],
    'X': [0, 1, 0, -1, 0, 1, 0, -1],
    'Y': [1, 0, -1, 0, 1, 0, -1, 0],
    'Z': [0, 0, 0, 0, 0, 0, 0, 0]  # Z is always 0
}

# Create the DataFrame
df_cw = pd.DataFrame(data)

print(turning_funcs.running_sum(df_cw))

#plot df_right
plt.plot(turning_funcs.running_sum(df_cw))
plt.title('Running Sum of Clockwise')
plt.show()

data_left = {
    'time': [0, 1, 2, 3, 4, 5, 6, 7],
    'X': [1, 0, -1, 0, 1, 0, -1, 0],
    'Y': [0, 1, 0, -1, 0, 1, 0, -1],
    'Z': [0, 0, 0, 0, 0, 0, 0, 0]  # Z is always 0
}
df_ccw = pd.DataFrame(data_left)
plt.plot(turning_funcs.running_sum(df_ccw))
plt.title('Running Sum of counter-clockwise')
plt.show()



# actual data with rolling average



# Apply rolling average with a specified window size
window_size = 10  # Adjust this window size as needed
r1_sum = turning_funcs.running_sum(cleanedData)



window_size = 3  # Adjust this window size as needed
r2 = turning_funcs.rolling_avg(cleanedData, window_size)
r2_sum = turning_funcs.running_sum(r2)


#plot r1_sum and r2_sum on the same plot
plt.plot(r1_sum, label='Real Data')
plt.plot(r2_sum, label='Rolling Average Data')
plt.title('Running Sum of Real Data and Rolling Average Data')

plt.legend()
plt.show()