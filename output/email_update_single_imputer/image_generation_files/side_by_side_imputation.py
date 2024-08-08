from imputation_strategies import avgValue
import matplotlib.pyplot as plt
from src.data_manipulation.NPZer import NPZer
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner

import pandas as pd

impute = avgValue.impute

cols = ['X', 'Y', 'time']
#fishDataPandas = NPZer().pandafy(source_dir = 'data/npz_file/single_7_9_fish1.MP4_fish0.npz', invertY = True, params = cols)
fishDataPandas = pd.read_csv('data/clean_fish_data/fish_data_clean.csv')
fishDataPandas.drop(columns = ['Unnamed: 0'], inplace=True)
#fishDataPandas, _ = TRexDataCleaner().renderDiscontinuities(data = fishDataPandas, vmax = 40)




import matplotlib.pyplot as plt

# Create a figure and axis objects
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Plot unimputed data
axs[0].plot(fishDataPandas["X"], fishDataPandas["Y"], color='blue')
axs[0].set_title('Unimputed Data')
axs[0].set_xlabel('X')
axs[0].set_ylabel('Y')

fishDataPandasImputed = impute(data = fishDataPandas)

# Plot imputed data
axs[1].plot(fishDataPandasImputed["X"], fishDataPandasImputed["Y"], color='red')
axs[1].set_title('Imputed Data (Simple Linear Imputation)')
axs[1].set_xlabel('X')
axs[1].set_ylabel('Y')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show the plot
plt.show()
