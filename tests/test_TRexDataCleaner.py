import pytest
import numpy as np
import pandas as pd
# Import classes from src/data_manipulation
from src.data_manipulation.TRexDataTester import TRexDataTester
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_manipulation.NPZer import NPZer

dataCleaner = TRexDataCleaner()

def test_cleanedDataStructure():
    data = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X', 'Y'])
    dataCleaner = TRexDataCleaner()
    cleaned, removed = dataCleaner.renderDiscontinuities(data = data, vmax = 50)
    tester = TRexDataTester(timeTracked = True, dtype = np.floating)
    tester.testAll(cleaned)

def test_calculateVelocity():
    pi = (0, 0)
    pf = (3, 4)
    dtime = 5
    velocity = dataCleaner.calculateVelocity(pi, pf, dtime)
    expectedVelocity = 1.0  # distance of 5 in 5 seconds = velocity of 1
    assert pytest.approx(velocity, 0.01) == expectedVelocity

def testDiscontinuity():
    pi = (0, 0)
    pf = (3, 4)
    vmax = 1.0
    ti = 0
    tf = 5
    assert not dataCleaner.isDiscontinuity(pi, pf, vmax, ti, tf)
    
    # higher velocity now, should be a discontinuity
    assert dataCleaner.isDiscontinuity(pi, pf, vmax, ti = 0, tf = 1)
    
    pf = (np.inf, np.inf)
    assert dataCleaner.isDiscontinuity(pi, pf, vmax, ti = 0, tf = 1)

def test_renderDiscontinuities():
    dataCleaner = TRexDataCleaner()
    vmax = 5
    sampleData = pd.DataFrame.from_dict({
        'time': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        'X': [0.0, 1.0, 2.0, 20.0, 3.0, 4.0],
        'Y': [0.0, 1.0, 2.0, 2.0, 3.0, 4.0]
    }).reset_index(drop=True)
    
    cleanedData, removedData = dataCleaner.renderDiscontinuities(sampleData, vmax)
    
    expected_cleanedData = pd.DataFrame.from_dict({
        'time': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        'X': [0.0, 1.0, 2.0, np.inf, 3.0, 4.0],
        'Y': [0.0, 1.0, 2.0, np.inf, 3.0, 4.0]
    }).reset_index(drop=True)
    
    expected_removedData = pd.DataFrame.from_dict({
        'time': [3.0],
        'X': [20.0],
        'Y': [2.0]
    }).reset_index(drop=True)

    pd.testing.assert_frame_equal(cleanedData, expected_cleanedData)
    pd.testing.assert_frame_equal(removedData, expected_removedData)

pytest.main()
