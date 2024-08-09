import numpy as np
import pandas as pd
from typing import Union

class TRexDataTester:
    """ Tester for TRex data

        Attributes:
        -----------
            timeTracked: bool, default False
                Set True to check if TRex data tracks time correctly. If time is not in the data, then set False or do not give this argument
            dtype: class or list of classes, default None
                Sets classes to check if data is of specified type(s)
        Functions:
        ----------
        test_datastruct:
            Tests if data is a Numpy ndarray or Pandas DataFrame
        test_columns:
            Tests if all columns have data
        test_homogenous
            Tests if all columns are homogenous, i.e., they have the same length
        test_dtype:
            Tests if all data is of specified type(s)
        test_startZero:
            Tests if time parameter starts at zero
        test_timeOrder:
            Tests if time data is in order, e.g., 1, 2, 3...
    """

    def __init__(self, timeTracked: bool = False, dtype: Union[float, np.floating] = None):
        self.timeTracked = timeTracked
        self.dtype = dtype

    def test_datastruct(self, data: Union[np.ndarray, pd.DataFrame]):
        assert isinstance(data, np.ndarray) or isinstance(data, pd.DataFrame), f"\nExpected numpy ndarray or pandas DataFrame \nReceived: {type(data)}"

    def test_columns(self, data: Union[np.ndarray, pd.DataFrame]):
        if isinstance(data, pd.DataFrame):
            numCols = data.shape[1]
            colLengths = [len(data.loc[col])for col in range(numCols)]
        else:
            numCols = len(data)
            colLengths = [len(col) for col in data]
        
        for i, length in enumerate(colLengths):
            assert length > 0, f"\nExpected non-empty columns \nReceived: column index {i} of length {length}"
    
    def test_homogenous(self, data: Union[np.ndarray, pd.DataFrame]):
        if isinstance(data, pd.DataFrame):
            lengths = [data.shape[0] for col in range(data.shape[1])]
        else:
            lengths = [len(col) for col in data]

        assert all(length == lengths[0] for length in lengths), f"\nExpected homogeneously-shaped data \nReceived column lengths: {lengths}"

    def test_dtype(self, data: Union[np.ndarray, pd.DataFrame]):
        if isinstance(data, pd.DataFrame):
            for col in range(data.shape[1]):
                for row in range(data.shape[0]):
                    num = data.iat[row, col]
                    if num in ('infinity', np.inf): continue
                    assert isinstance(num, self.dtype), f"\nExpected data type: {self.dtype}\nReceived: {data.columns[col]} value {num} as {type(num)} at row {row}"
        else:
            for colNum, col in enumerate(data): 
                for rowNum, num in enumerate(col):
                    if num in ('infinity', np.inf): continue
                    assert isinstance(num, self.dtype), f"\nExpected data type: {self.dtype}\nReceived: value {num} as {type(num)} in column {colNum} at row {rowNum}"

    def test_startZero(self, data: Union[np.ndarray, pd.DataFrame]):
        assert self.timeTracked, f"Time is not tracked and cannot be checked for starting at zero"
        if isinstance(data, pd.DataFrame):
            assert data.iloc[0, 0] == 0, f"\nExpected starting time: 0.00s \nReceived: {data.iloc[0, 0]}s"
        else:
            assert data[0, 0] == 0, f"\nExpected starting time: 0.00s \nReceived: {data[0, 0]}s"

    def test_timeOrder(self, data: Union[np.ndarray, pd.DataFrame]):
        if isinstance(data, pd.DataFrame):
            times = data.get('time')
        else:
            times = data[0]
            
        for i in range(1, len(times)):
            if 'infinity' in (times[i - 1], times[i]): continue
            assert times[i - 1] < times[i], f'\nTime increments are not in order: Time {times[i - 1]} is after Time {times[i]} at index {i}'

    def testAll(self, data: Union[np.ndarray, pd.DataFrame]):
        self.test_datastruct(data)
        self.test_columns(data)
        self.test_homogenous(data)
        if self.dtype is not None: self.test_dtype(data)
        if self.timeTracked: 
            self.test_timeOrder(data)
            self.test_startZero(data)