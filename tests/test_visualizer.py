# tests/test_visualizer.py
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# Import classes from src/data_manipulation
from missing_data_dev.plot_path_dev.visualizer import DaphniaAnimation
from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataTester import TRexDataTester


data = NPZer.unzipNpz(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', params = ['time', 'X#wcentroid', 'Y#wcentroid'])
    
tester = TRexDataTester(timeTracked = True, dtype = np.floating)
tester.testAll(data)
    
# print("Unzipped data:\n", data)

pandasData = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'], )
# print("Pandafied Directly:\n", pandasData)

pandasData = NPZer.pandafy(data = data, invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'], tester = tester)
# print("Pandafied from Unzipped:\n", pandasData)

NPZer.npzip(data = pandasData, save_dir = 'data/npz_file/zipped.npz', tester = tester, params = ['time', 'X#wcentroid', 'Y#wcentroid'])
unzipped = NPZer.unzipNpz(source_dir = 'data/npz_file/zipped.npz', params = ['time', 'X#wcentroid', 'Y#wcentroid'])
# print("Unzipped again:\n", unzipped)

pandasData = NPZer.pandafy(data = unzipped, invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'], tester = tester)
print("Pandafied again:\n", pandasData)



df = pandasData
# invert y
df['Y#wcentroid'] = -df['Y#wcentroid']
animation = DaphniaAnimation(df, start_index=3320)
animation.create_animation()


# if __name__ == "__main__":
#     pass