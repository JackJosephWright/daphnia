# this loads the smoothed data for testing dr kogans turn demarcation idea

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression



from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs


from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_visualization.visualizer import DaphniaAnimation
from src.turning_functions import turning_funcs
dataCleaner = TRexDataCleaner()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

faultyData = NPZer.pandafy(source_dir='data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY=True, params=['time', 'X', 'Y'])


#convert to np.nan
faultyData = faultyData.replace([np.inf, -np.inf], np.nan)

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
    segments = []
    
    # Track the current segment
    current_segment = []

    for index, row in df.iterrows():
        if pd.isna(row[column_name]):
            # If we hit a NaN, append the current segment to the list and start a new one
            if current_segment:
                #reset index
                segments.append(pd.DataFrame(current_segment).reset_index(drop=True))
                
                current_segment = []  # Reset the current segment
        else:
            # Add the row to the current segment
            current_segment.append(row)

    # Don't forget to add the last segment if it exists
    if current_segment:
        segments.append(pd.DataFrame(current_segment))
    
    return segments

# Apply the function to split the data based on NaN in column 'X'
segments = split_on_nan(faultyData, 'X')
smoothing_window = 50
turn_window  = 30


for segment in segments:
    if len(segment)>100:
        smoothed = turning_funcs.rolling_avg(segment, smoothing_window)
        running_theta = turning_funcs.running_theta_sum(smoothed)

        turns, turn_index_list =  turning_funcs.count_turns(running_theta, turn_window)
        turning_funcs.plot_turns_and_path(smoothed, turns,turn_index_list)
        # wait for input to close plot and continue
        input("Press Enter to continue...")
        plt.close()