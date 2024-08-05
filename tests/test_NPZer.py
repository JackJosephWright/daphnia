# tests/test_NPZer.py
import pytest
import numpy as np
# Import classes from src/data_manipulation
from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataTester import TRexDataTester

print(NPZer, TRexDataTester)

def test_dummy():
    assert 1 == 1

if __name__ == "__main__":
    data = NPZer.unzipNpz(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', params = ['time', 'X', 'Y'])
    
    tester = TRexDataTester(timeTracked = True, dtype = np.floating)
    tester.testAll(data)
    
    print("Unzipped data:\n", data)

    pandasData = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X', 'Y'], )
    print("Pandafied Directly:\n", pandasData)
    
    pandasData = NPZer.pandafy(data = data, invertY = True, params = ['time', 'X', 'Y'], tester = tester)
    print("Pandafied from Unzipped:\n", pandasData)

    NPZer.npzip(data = pandasData, save_dir = 'data/npz_file/zipped.npz', tester = tester, params = ['time', 'X', 'Y'])
    unzipped = NPZer.unzipNpz(source_dir = 'data/npz_file/zipped.npz', params = ['time', 'X', 'Y'])
    print("Unzipped again:\n", unzipped)

    pandasData = NPZer.pandafy(data = unzipped, invertY = True, params = ['time', 'X', 'Y'], tester = tester)
    print("Pandafied again:\n", pandasData)

