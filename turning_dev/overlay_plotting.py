from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
import matplotlib.pyplot as plt


dataCleaner = TRexDataCleaner()


faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])
cleanedData, removedData = dataCleaner.renderDiscontinuities(data=faultyData, vmax=50)


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

import matplotlib.pyplot as plt


def plot_dataframes(df1, df2, x_col='X', y_col='Y', label1='DataFrame 1', label2='DataFrame 2'):
    plt.figure(figsize=(10, 6))

    # Plotting the first dataframe
    plt.plot(df1[x_col], df1[y_col], label=label1, color='blue', linestyle='-')

    # Plotting the second dataframe
    plt.plot(df2[x_col], df2[y_col], label=label2, color='orange', linestyle='-')

    # Adding labels and title
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title('Line Plot of DataFrames')

    # Adding a legend
    plt.legend()

    # Displaying the plot
    plt.show()

# Example with a window size of 1
window_size = 1
r1 = rolling_avg(cleanedData, window_size)

# # Example with a window size of 10
window_size = 10
r2 = rolling_avg(cleanedData, window_size)



plot_trajectory(r1)
plot_trajectory(r2)

plot_dataframes(r1, r2, label1='Window Size 1', label2='Window Size 10')





