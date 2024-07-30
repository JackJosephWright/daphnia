import pandas as pd
from matplotlib import pyplot as plt
import numpy as np



def plotDetail(df, xlabel = None, ylabel = None, invert_y =False, title ="placeholder_title"):

    "this function is used to plot the path of the daphnia"


    csfont = {'fontname':'Comic Sans MS', 'color':'blue', 'size':20}
    hfont = {'fontname':'Helvetica', 'color':'blue', 'size':12}
    if invert_y:
        df['Y'] = -df['Y']
    plt.title(title,fontdict=csfont)
    if xlabel is None:
        xlabel = "X"
    if ylabel is None:
        ylabel = "Y"
    plt.xlabel(xlabel,fontdict=hfont)
    plt.ylabel(ylabel,fontdict=hfont)
    plt.plot(df['X'], df['Y'])
    plt.show()
