import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
#npz_path = r"C:\Users\jwright\Documents\GitHub\daphnia\data\npz_file\small_100_fish0.npz"
#npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/small_100_fish0.npz"
# npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/single_7_9_fish1.MP4_fish0.npz"
npz_path = r"data/npz_file/single_7_9_fish1.MP4_fish0.npz"

#use np.load to load the npz file
data = np.load(npz_path)

time = data['time']

X = data['X']
Y = data['Y']
Y = -Y

df = pd.DataFrame(
    {
        "X": X,
        "Y": Y,
        "time": time
    }
)


# Drop missing or infinite data
df.replace(['', np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)


df_subset = df.loc[3320:]


#set up the plot
fig, ax = plt.subplots()
line, = ax.plot([],[],'b-')

#set limits 
ax.set_xlim(df_subset['X'].min(), df_subset['X'].max())
ax.set_ylim(df_subset['Y'].min(), df_subset['Y'].max())


def plotDetail(title, xlable, ylabel):
    csfont = {'fontname':'Comic Sans MS', 'color':'blue', 'size':20}
    hfont = {'fontname':'Helvetica', 'color':'blue', 'size':12}
    plt.title(title,fontdict=csfont)
    plt.xlabel(xlable,fontdict=hfont)
    plt.ylabel(ylabel,fontdict=hfont)


# plt.plot(df_subset['X'], df_subset['Y'])
# plotDetail("Single Fish Data","X value","Y value")
# plt.show()

if __name__ == "__main__":
    #writing csv
    import csv
    df_subset.to_csv('data/clean_fish_data/fish_data_clean.csv', index=False)

# check how many rows of missing data
    # df.replace(['', np.inf, -np.inf], np.nan, inplace=True)
    # miss = df_subset[df_subset.isnull().any(axis=1)]
    # print(miss)