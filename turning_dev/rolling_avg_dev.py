from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
dataCleaner = TRexDataCleaner()
    
faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
print(f"Faulty Data: \n {faultyData}")

cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)
print("Cleaned Data: \n", cleanedData)
print("Removed Data: \n", removedData)


import pandas as pd
import matplotlib.pyplot as plt

def rolling_avg(df, window):
    """
    Calculate the rolling average for the columns 'X' and 'Y' in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The input dataframe containing 'time', 'X', and 'Y' columns.
    window (int): The window size for calculating the rolling average.
    
    Returns:
    pd.DataFrame: A dataframe with the rolling average applied to 'X' and 'Y'.
    """
    df[['X', 'Y']] = df[['X', 'Y']].rolling(window=window).mean()
    return df
import matplotlib.pyplot as plt

def plot_trajectory(df):
    """
    Plot the trajectory of a Daphnia in a dish using X and Y coordinates with a focus on more detail.
    
    Parameters:
    df (pd.DataFrame): The input dataframe containing 'X' and 'Y' columns representing positions.
    """
    plt.figure(figsize=(12, 8))
    
    # Creating a connected scatter plot with a very thin line and no markers
    plt.plot(df['X'], df['Y'], label='Trajectory', color='blue', linewidth=0.5, linestyle='-', alpha=0.8)
    
    # Adding titles and labels
    plt.title('Detailed Trajectory of Daphnia in a Dish')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    
    # Inverting the y-axis to better represent traditional coordinate systems (optional)
    plt.gca().invert_yaxis()
    
    # Adding a legend
    plt.legend()
    
    # Display the plot
    plt.grid(True)
    plt.show()


# Example with a window size of 3
window_size = 10
result = rolling_avg(cleanedData, window_size)
plot_trajectory(result)




import numpy as np

import numpy as np

def determine_turning_direction(df):
    """
    Determine the turning direction (left or right) of the Daphnia and return counts.
    
    Parameters:
    df (pd.DataFrame): The input dataframe containing 'X' and 'Y' columns representing positions.
    
    Returns:
    dict: A dictionary with the counts of 'Left', 'Right', and 'Straight' turns.
    """
    # Initialize a dictionary to count the directions
    turn_counts = {'Left': 0, 'Right': 0, 'Straight': 0}
    
    for i in range(1, len(df) - 1):
        # Vector from point n-1 to n
        vector_1 = np.array([df['X'].iloc[i] - df['X'].iloc[i-1], 
                             df['Y'].iloc[i] - df['Y'].iloc[i-1]])
        
        # Vector from point n to n+1
        vector_2 = np.array([df['X'].iloc[i+1] - df['X'].iloc[i], 
                             df['Y'].iloc[i+1] - df['Y'].iloc[i]])
        
        # Calculate the cross product (only the z-component is needed for 2D)
        cross_product = np.cross(vector_1, vector_2)
        
        # Determine direction based on the sign of the cross product and update the count
        if cross_product > 0:
            turn_counts['Left'] += 1
        elif cross_product < 0:
            turn_counts['Right'] += 1
        else:
            turn_counts['Straight'] += 1
    
    return turn_counts

# Example usage (assuming 'cleaned_data' is your dataframe)
# turn_counts = determine_turning_direction(cleaned_data)

# The function will return a dictionary with the counts of 'Left', 'Right', and 'Straight' turns.

# Example usage (assuming 'cleaned_data' is your dataframe)
# turning_directions = determine_turning_direction(cleaned_data)

# The function will return a list of 'Left', 'Right', or 'Straight' indicating the turning direction at each point.



turn_counts = determine_turning_direction(cleanedData)



def plot_turn_counts(turn_counts):
    """
    Plot the counts of left, right, and straight turns in a bar graph.
    
    Parameters:
    turn_counts (dict): A dictionary with the counts of 'Left', 'Right', and 'Straight' turns.
    """
    # Extract the keys (turn directions) and values (counts)
    directions = list(turn_counts.keys())
    counts = list(turn_counts.values())
    
    # Plotting the bar graph
    plt.figure(figsize=(8, 6))
    plt.bar(directions, counts, color=['blue', 'red', 'green'])
    
    # Adding titles and labels
    plt.title('Turn Counts of Daphnia')
    plt.xlabel('Turn Direction')
    plt.ylabel('Count')
    
    # Display the plot
    plt.show()

# Example usage
# Assuming turn_counts is the dictionary you obtained
turn_counts  = determine_turning_direction(cleanedData)
plot_turn_counts(turn_counts)