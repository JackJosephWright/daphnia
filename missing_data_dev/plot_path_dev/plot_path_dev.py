
"""
take a look at the npz file and the subfiles. We need to extract the relevant file (maybe timestamp X and Y to create the df)
"""


from ..npz_zip_dev import zip
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
#npz_path = r"C:\Users\jwright\Documents\GitHub\daphnia\data\npz_file\small_100_fish0.npz"
#npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/small_100_fish0.npz"
npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/single_7_9_fish1.MP4_fish0.npz"

#use np.load to load the npz file
data = np.load(npz_path)



timestamp = data['timestamp']

X = data['X']
Y = data['Y']

df = pd.DataFrame(
    {
        "X": X,
        "Y": Y,
        "time": timestamp
    }
)

#plt.plot(X, Y)
#plt.show()
#print(df)


def plotDetail(title, xlable, ylabel):
    plt.title(title)
    plt.xlabel(xlable)
    plt.ylabel(ylabel)

plt.plot(X, Y)
plotDetail("NPZ","X value","Y value")
plt.show()

#if __name__ == "__main__":
