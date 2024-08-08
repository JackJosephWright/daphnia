from imputation_strategies import avgValue
import matplotlib.pyplot as plt
from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner

import pandas as pd

impute = avgValue.impute

cols = ['X', 'Y', 'time']
fishDataPandas = NPZer().pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = cols)
#fishDataPandas = pd.read_csv('data/clean_fish_data/fish_data_clean.csv')
#fishDataPandas.drop(columns = ['Unnamed: 0'], inplace=True)
fishDataPandas, _ = TRexDataCleaner().renderDiscontinuities(data = fishDataPandas, vmax = 1.4*(10**-5))

fishDataPandas = impute(data = fishDataPandas)


plt.plot(fishDataPandas["X"], fishDataPandas["Y"])
plt.show()