import numpy as np
import pandas as pd
from typing import Union

class TRexDataTester:
    """
    Tester for TRex data.

    This class provides various methods to test the integrity and correctness of TRex data, 
    including checks for data structure, column completeness, homogeneity, data types, 
    and time tracking.

    Attributes
    ----------
    timeTracked : bool, default False
        If True, checks if TRex data tracks time correctly. If time is not in the data, 
        set to False or leave as default.
    dtype : type or list of types, optional
        Specifies the expected data type(s) for the data being tested. If provided, the 
        `test_dtype` method will check that all data matches these types.

    Methods
    -------
    test_datastruct(data):
        Tests if the provided data is a Numpy ndarray or Pandas DataFrame.
    test_columns(data):
        Tests if all columns in the data have non-empty values.
    test_homogenous(data):
        Tests if all columns in the data have the same length.
    test_dtype(data):
        Tests if all data entries are of the specified type(s).
    test_startZero(data):
        Tests if the 'time' parameter starts at zero.
    test_timeOrder(data):
        Tests if the 'time' data is in sequential order.
    testAll(data):
        Runs all the tests on the provided data.
    """


    def __init__(self, timeTracked: bool = False, dtype: Union[float, np.floating] = None):
        self.timeTracked = timeTracked
        self.dtype = dtype

    def test_datastruct(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Tests if the provided data is a Numpy ndarray or Pandas DataFrame.

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If the data is not of type numpy.ndarray or pandas.DataFrame.
        """
        assert isinstance(data, np.ndarray) or isinstance(data, pd.DataFrame), f"\nExpected numpy ndarray or pandas DataFrame \nReceived: {type(data)}"

    def test_columns(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Tests if all columns in the provided data have non-empty values.

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If any column in the data is empty.
        """
        if isinstance(data, pd.DataFrame):
            numCols = data.shape[1]
            colLengths = [len(data.loc[col]) for col in range(numCols)]
        else:
            numCols = len(data)
            colLengths = [len(col) for col in data]
        
        for i, length in enumerate(colLengths):
            assert length > 0, f"\nExpected non-empty columns \nReceived: column index {i} of length {length}"

    
    def test_homogenous(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Tests if all columns in the data have the same length.

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If any column in the data does not have the same length as the others.
        """
        if isinstance(data, pd.DataFrame):
            lengths = [data.shape[0] for col in range(data.shape[1])]
        else:
            lengths = [len(col) for col in data]

        assert all(length == lengths[0] for length in lengths), f"\nExpected homogeneously-shaped data \nReceived column lengths: {lengths}"

    def test_dtype(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Tests if all data entries are of the specified type(s).

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If any data entry is not of the specified type(s).
        """
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
        """
        Tests if the 'time' parameter starts at zero.

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If the timeTracked attribute is False or if the time parameter does not start at zero.
        """
        assert self.timeTracked, f"Time is not tracked and cannot be checked for starting at zero"
        if isinstance(data, pd.DataFrame):
            assert data.iloc[0, 0] == 0, f"\nExpected starting time: 0.00s \nReceived: {data.iloc[0, 0]}s"
        else:
            assert data[0, 0] == 0, f"\nExpected starting time: 0.00s \nReceived: {data[0, 0]}s"

    def test_timeOrder(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Tests if the 'time' data is in sequential order.

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If the 'time' data is not in sequential order.
        """
        if isinstance(data, pd.DataFrame):
            times = data.get('time')
        else:
            times = data[0]
            
        for i in range(1, len(times)):
            if 'infinity' in (times[i - 1], times[i]): continue
            assert times[i - 1] < times[i], f'\nTime increments are not in order: Time {times[i - 1]} is after Time {times[i]} at index {i}'

    def testAll(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Runs all available tests on the provided data.

        Parameters
        ----------
        data : Union[np.ndarray, pd.DataFrame]
            The data to be tested.

        Raises
        ------
        AssertionError
            If any of the tests fail.
        """
        self.test_datastruct(data)
        self.test_columns(data)
        self.test_homogenous(data)
        if self.dtype is not None: self.test_dtype(data)
        if self.timeTracked: 
            self.test_timeOrder(data)
            self.test_startZero(data)