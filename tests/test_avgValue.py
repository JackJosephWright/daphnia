import pytest
import numpy as np
import pandas as pd

from imputation_strategies import avgValue
impute = avgValue.impute
calculateVelocity = avgValue.calculateVelocity

def test_impute():
    data = pd.DataFrame({
        'time': [0.0, 1.0, 2.0, 3.0, 4.0],
        'X': [0.0, np.inf, np.inf, np.inf, 4.0],
        'Y': [0.0, np.inf, np.inf, np.inf, 4.0]
    })
    expected_output = pd.DataFrame({
        'time': [0.0, 1.0, 2.0, 3.0, 4.0],
        'X': [0.0, 1.0, 2.0, 3.0, 4.0],
        'Y': [0.0, 1.0, 2.0, 3.0, 4.0]
    })
    
    result = impute(data)
    print(result, '\n', expected_output)
    pd.testing.assert_frame_equal(result, expected_output)

def test_imputeCleanData():
    data = pd.DataFrame({
        'time': [0.0, 1.0, 2.0, 3.0, 4.0],
        'X': [0.0, 1.0, 2.0, 3.0, 4.0],
        'Y': [0.0, 1.0, 2.0, 3.0, 4.0]
    })
    expected_output = data.copy()
    
    result = impute(data)
    pd.testing.assert_frame_equal(result, expected_output)
    
def test_calculateVelocity():
    pi = 0
    pf = 4
    ti = 0
    tf = 4
    expected_velocity = 1.0
    
    velocity = calculateVelocity(pi = pi, pf = pf, dtime = tf - ti)
    assert velocity == expected_velocity


