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

segments = turning_funcs.split_on_nan(faultyData, 'X')




# for segment in segments:
#     if len(segment)>200:
#         smoothed = turning_funcs.rolling_avg(segment)
#         smoothed = smoothed.dropna().reset_index(drop=True)
#         running_theta = turning_funcs.running_theta_sum(smoothed)

#         turns, turn_index_list, slope_list =  turning_funcs.count_turns(running_theta)
#         turning_funcs.plot_turns_and_path(smoothed, turns,turn_index_list, running_theta, slope_list)
#         # wait for input to close plot and continue
#         input("Press Enter to continue...")
#         plt.close()


# for segment in segments:
#     if len(segment)>200:
#         smoothed = turning_funcs.rolling_avg(segment)
#         smoothed = smoothed.dropna().reset_index(drop=True)
#         running_theta = turning_funcs.running_theta_sum(smoothed)

#         turns, turn_index_list, slope_list =  turning_funcs.count_turns(running_theta)
#         turning_funcs.plot_turns_and_path(smoothed, turns,turn_index_list, running_theta, slope_list)
#         # wait for input to close plot and continue
#         input("Press Enter to continue...")
#         plt.close()
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
    
    smoothed = turning_funcs.rolling_avg(df, smoothing_window)
    #smoothed = smoothed.dropna().reset_index(drop=True)
    
    running_theta = turning_funcs.running_theta_sum(smoothed)
    # print('df length:', len(smoothed))
    # print('running_theta_length: ', len(running_theta))
    # create tidy df which is smoothed with running theta as an additional column
    if len(running_theta) != len(smoothed):
        print('length of running theta and smoothed do not match')
        #print diagnostics 
        print('length of running_theta:', len(running_theta))
        print('length of smoothed:', len(smoothed))
        # look for 
        return None
    tidy_df = smoothed
    tidy_df['running_theta'] = running_theta
    turns, turn_index_list, slope_list =  turning_funcs.count_turns(running_theta, turn_window)
    print('turn index list after return:')
    print(turn_index_list)  
    df_length = len(tidy_df)
    turn_col = gen_turn_column(df_length, turn_index_list)
    tidy_df['turn_id'] = turn_col
    print('unique vals in turn_id:', tidy_df['turn_id'].unique())
    return tidy_df



for seg in segments:
    if len(seg)> 200:
        single_seg = generate_turning_df(seg)
        break

single_seg.to_csv("single_seg.csv") 
