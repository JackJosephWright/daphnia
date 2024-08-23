# tests/test_visualizer.py
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# Import classes from src/data_manipulation

from src.data_manipulation.TRexDataTester import TRexDataTester

data = NPZer.unzipNpz(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', params = ['time', 'X', 'Y'])
    
tester = TRexDataTester(timeTracked = True, dtype = np.floating)
tester.testAll(data)
    
# print("Unzipped data:\n", data)

from missing_data_dev.plot_path_dev.visualizer import DaphniaAnimation
from src.data_manipulation.NPZer import NPZer

pandasData = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X', 'Y'], )

animation = DaphniaAnimation(df=pandasData, start_index=3320)
animation.create_animation()
