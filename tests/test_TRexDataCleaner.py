import pytest
import numpy as np
import pandas as pd
# Import classes from src/data_manipulation
from data_manipulation.TRexDataTester import TRexDataTester
from data_manipulation.TRexDataCleaner import TRexDataCleaner
from data_manipulation.NPZer import NPZer

dataCleaner = TRexDataCleaner()

def test_cleanedDataStructure():
    data = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X#wcentroid', 'Y#wcentroid'])
    dataCleaner = TRexDataCleaner()
    cleaned = dataCleaner.renderDiscontinuities(data = data, vmax = 50)
    tester = TRexDataTester(timeTracked = True, dtype = np.floating)
    tester.testAll(cleaned)
    
sampleData = pd.DataFrame.from_dict({
    'time': [0, 1, 2, 3, 4, 5],
    'X#wcentroid': [0, 1, 2, 20, 3, 4],
    'Y#wcentroid': [0, 1, 2, 2, 3, 4]
})

def test_calculateVelocity():
    pi = (0, 0)
    pf = (3, 4)
    dtime = 5
    velocity = dataCleaner.calculateVelocity(pi, pf, dtime)
    expectedVelocity = 1.0  # distance of 5 in 5 seconds = velocit of 1
    assert pytest.approx(velocity, 0.01) == expectedVelocity

def testDiscontinuity():
    pi = (0, 0)
    pf = (3, 4)
    vmax = 1.0
    dtime = 5
    assert not dataCleaner.isDiscontinuity(pi, pf, vmax, dtime)
    
    # higher velocity now, should be a discontinuity
    dtime = 1
    assert dataCleaner.isDiscontinuity(pi, pf, vmax, dtime)
    
    # 'infinity' value
    pf = (np.inf, np.inf)
    assert dataCleaner.isDiscontinuity(pi, pf, vmax, dtime)

def test_renderDiscontinuities():
    vmax = 10
    cleanedData, removedData = dataCleaner.renderDiscontinuities(sampleData, vmax)
    
    # Expected cleaned data
    expected_cleanedData = pd.DataFrame({
        'time': [0, 1, 2, 'infinity', 4, 5],
        'X#wcentroid': [0, 1, 2, 'infinity', 3, 4],
        'Y#wcentroid': [0, 1, 2, 'infinity', 3, 4]
    }).reset_index(drop=True)
    
    # Expected removed data
    expected_removedData = pd.DataFrame({
        'time': [3],
        'X#wcentroid': [20],
        'Y#wcentroid': [2]
    }).reset_index(drop=True)
    
    pd.testing.assert_frame_equal(cleanedData, expected_cleanedData)
    pd.testing.assert_frame_equal(removedData, expected_removedData)

    
    