import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from missing_data_dev.plot_path_dev.visualizer import DaphniaAnimation

npz_path = r"data/npz_file/single_7_9_fish1.MP4_fish0.npz"


animation = DaphniaAnimation(npz_path, start_index=3320)
animation.create_animation()


if __name__ == "__main__":
    pass