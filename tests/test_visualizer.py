# # tests/test_visualizer.py
# import pandas as pd
# from matplotlib import pyplot as plt
# import numpy as np
# from matplotlib.animation import FuncAnimation
# # Import classes from src/data_manipulation
# from missing_data_dev.plot_path_dev.visualizer import DaphniaAnimation
# from src.data_manipulation.NPZer import NPZer
# from src.data_manipulation.TRexDataTester import TRexDataTester
# from src.data_manipulation.TRexImputer import TRexImputer


# data = NPZer.unzipNpz(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', params = ['time', 'X', 'Y'])
    
# tester = TRexDataTester(timeTracked = True, dtype = np.floating)
# tester.testAll(data)
    
# # print("Unzipped data:\n", data)

# pandasData = NPZer.pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = ['time', 'X', 'Y'], )
# # print("Pandafied Directly:\n", pandasData)


# imputedData = TRexImputer().impute(pandasData)

# df = imputedData
# # invert y
# df['Y'] = -df['Y']
# animation = DaphniaAnimation(df, start_index=3320)
# animation.create_animation()


# # if __name__ == "__main__":
# #     pass




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
    return DaphniaAnimation(df=sample_data, start_index=0)

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
    assert np.array_equal(daphnia_animation.line.get_xdata(), [0, 1, 2])
    assert np.array_equal(daphnia_animation.line.get_ydata(), [0, 1, 2])

def test_create_animation_edge_cases():
    """Test create_animation handles edge cases"""
    empty_df = pd.DataFrame(columns=['time', 'X', 'Y'])
    with pytest.raises(ValueError, match="No valid data points available to set axis limits."):
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
    # Here you would assert conditions based on what should happen in a successful animation creation
    # Since it's hard to assert animations, this is generally where you would rely on visual inspection or mock objects

if __name__ == "__main__":
    pytest.main()