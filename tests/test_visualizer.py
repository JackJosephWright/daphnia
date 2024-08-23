import pytest
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from missing_data_dev.plot_path_dev.visualizer import DaphniaAnimation

@pytest.fixture
def sample_data():
    """Fixture to create sample data for tests"""
    return pd.DataFrame({
        'time': [0, 1, 2, 3, 4, 5],
        'X': [0, 1, 2, 20, 3, 4],
        'Y': [0, 1, 2, 2, 3, 4]
    })

@pytest.fixture
def daphnia_animation(sample_data):
    """Fixture to create a DaphniaAnimation instance"""
    return DaphniaAnimation(df=sample_data, start_index=0, interval=100)

def test_plot_detail(daphnia_animation):
    """Test if plot detail is set correctly"""
    daphnia_animation.plot_detail(title="Test Title", xlabel="X Axis", ylabel="Y Axis")
    assert daphnia_animation.ax.get_title() == "Test Title"
    assert daphnia_animation.ax.get_xlabel() == "X Axis"
    assert daphnia_animation.ax.get_ylabel() == "Y Axis"

def test_init_animation(daphnia_animation):
    """Test if animation is initialized correctly"""
    line = daphnia_animation.init_animation()
    assert line[0].get_data() == ([], [])

def test_animate(daphnia_animation):
    """Test if animation updates correctly frame by frame"""
    daphnia_animation.animate(3)
    # Convert xdata and ydata to NumPy arrays
    xdata = np.array(daphnia_animation.line.get_xdata())
    ydata = np.array(daphnia_animation.line.get_ydata())
    expected_x = np.array([0, 1, 2, 20])
    expected_y = np.array([0, 1, 2, 2])
    assert np.array_equal(xdata, expected_x)
    assert np.array_equal(ydata, expected_y)

# Edge case
def test_create_animation_edge_cases():
    """Test create_animation handles edge cases"""
    empty_df = pd.DataFrame(columns=['time', 'X', 'Y'])
    # Expect IndexError due to empty DataFrame
    with pytest.raises(IndexError, match="start_index is out of bounds"):
        DaphniaAnimation(df=empty_df).create_animation()

    inf_df = pd.DataFrame({
        'time': [0, 1, 2],
        'X': [np.inf, np.inf, np.inf],
        'Y': [np.inf, np.inf, np.inf]
    })
    with pytest.raises(ValueError, match="No valid data points available to set axis limits."):
        DaphniaAnimation(df=inf_df).create_animation()

def test_create_animation_normal_case(daphnia_animation):
    """Test create_animation works with valid data"""
    daphnia_animation.create_animation()
    # Check if the plot was created
    assert daphnia_animation.ax.get_xlim() is not None
    assert daphnia_animation.ax.get_ylim() is not None
    # Here you would assert conditions based on what should happen in a successful animation creation
    # Since it's hard to assert animations, this is generally where you would rely on visual inspection or mock objects

# Tests that should fail
def test_out_of_bounds_index():
    """Test using an out-of-bounds start index."""
    df = pd.DataFrame({'time': [0, 1, 2], 'X': [1, 2, 3], 'Y': [4, 5, 6]})
    with pytest.raises(IndexError):
        DaphniaAnimation(df, start_index=10)  # Index out of range

def test_invalid_data_types():
    """Test handling of invalid data types."""
    # DataFrame with strings instead of numeric values
    df_with_strings = pd.DataFrame({
        'time': ['a', 'b', 'c'],
        'X': ['x', 'y', 'z'],
        'Y': ['p', 'q', 'r']
    })

    # DataFrame with some numeric values replaced with empty strings
    df_with_empty_values = pd.DataFrame({
        'time': [0, 1, 2],
        'X': [1, '', 3],
        'Y': [4, 5, '']
    })

    # Test with DataFrame containing strings
    with pytest.raises(ValueError):
        DaphniaAnimation(df_with_strings)

    # Test with DataFrame containing empty strings
    with pytest.raises(ValueError):
        DaphniaAnimation(df_with_empty_values)

if __name__ == "__main__":
    pytest.main()