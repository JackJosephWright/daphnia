from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataTester import TRexDataTester
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
#npz_path = r"C:\Users\jwright\Documents\GitHub\daphnia\data\npz_file\small_100_fish0.npz"
#npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/small_100_fish0.npz"
npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/single_7_9_fish1.MP4_fish0.npz"

#use np.load to load the npz file
data = np.load(npz_path)

timestamp = data['timestamp']

X = data['X']
Y = data['Y']
Y = -Y

df = pd.DataFrame(
    {
        "X": X,
        "Y": Y,
        "time": timestamp
    }
)


# Drop missing or infinite data
# df.dropna(inplace=True)
# df.replace(['', np.inf, -np.inf], np.nan, inplace=True)
# df.dropna(inplace=True)


df_subset = df.loc[3320:]


#set up the plot
fig, ax = plt.subplots()
line, = ax.plot([],[],'b-')

#set limits 
# ax.set_xlim(df_subset['X'].min(), df_subset['X'].max())
# ax.set_ylim(df_subset['Y'].min(), df_subset['Y'].max())


def plotDetail(title, xlable, ylabel):
    csfont = {'fontname':'Comic Sans MS', 'color':'blue', 'size':20}
    hfont = {'fontname':'Helvetica', 'color':'blue', 'size':12}
    plt.title(title,fontdict=csfont)
    plt.xlabel(xlable,fontdict=hfont)
    plt.ylabel(ylabel,fontdict=hfont)

plotDetail("Single Fish Data","X value","Y value")


# Initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# Animation function: this is called sequentially
def animate(i):
    x = df_subset['X'][:i]
    y = df_subset['Y'][:i]
    line.set_data(x, y)
    return line,

# Call the animator
ani = FuncAnimation(fig, animate, init_func=init, frames=len(df_subset), interval=50, blit=True)


# plt.plot(df_subset['X'], df_subset['Y'])
plt.show()





#if __name__ == "__main__":

# print(df_subset)
#writing csv
# df_subset.to_csv('fish_data_clean.csv')

# check how many rows of missing data
# df.replace(['', np.inf, -np.inf], np.nan, inplace=True)
# miss = df_subset[df_subset.isnull().any(axis=1)]
# print(miss)