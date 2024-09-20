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


seg_num = 0 
for segment in segments:
   
    print('working on segment, ', seg_num)
    seg_num += 1
    if len(segment)>200:
        
        turning_df = turning_funcs.generate_turning_df(segment)
        print('new_turning_df')
        print(turning_df.head())
        print(turning_df.describe())
        