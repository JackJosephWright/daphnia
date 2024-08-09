
"""
take a look at the npz file and the subfiles. We need to extract the relevant file (maybe timestamp X and Y to create the df)
"""


from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataTester import TRexDataTester
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
npz_path = r'data/npz_file/small_100_fish0.npz'
#npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/small_100_fish0.npz"
#npz_path = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/npz_file/single_7_9_fish1.MP4_fish0.npz"

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

df_subset = df.loc[3320:]
print(df_subset)
#writing csv
df_subset.to_csv('fish_data_clean.csv')

def plotDetail(title, xlable, ylabel):
    csfont = {'fontname':'Comic Sans MS', 'color':'blue', 'size':20}
    hfont = {'fontname':'Helvetica', 'color':'blue', 'size':12}
    plt.title(title,fontdict=csfont)
    plt.xlabel(xlable,fontdict=hfont)
    plt.ylabel(ylabel,fontdict=hfont)


# plt.plot(df_subset['X'], df_subset['Y'])
# plotDetail("Single Fish Data","X value","Y value")
# plt.show()

#if __name__ == "__main__":
