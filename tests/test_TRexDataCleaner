# tests/test_NPZer.py
import pytest
import numpy as np
# Import classes from src/data_manipulation
from data_manipulation.TRexDataTester import TRexDataTester
from data_manipulation.TRexDataCleaner import TRexDataCleaner
from data_manipulation.NPZer import NPZer

data = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'])
dataCleaner = TRexDataCleaner()
cleaned = dataCleaner.renderDiscontinuities(data = data, vmax = 50)

def test_cleanedDataStructure():
    tester = TRexDataTester(timeTracked = True, dtype = np.floating)
    tester.testAll(TRexDataCleaner)
    
    
    