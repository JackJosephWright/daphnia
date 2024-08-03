from imputation_strategies import avgValue
import matplotlib.pyplot as plt

import pandas as pd

impute = avgValue.impute

cols = ['X#wcentroid', 'Y#wcentroid', 'time']
fishDataPandas = pd.read_csv("/Users/gvitale/Documents/GitHub/daphnia/data/clean_fish_data/fish_data_clean.csv")
fishDataPandas.drop(columns = ['Unnamed: 0'], inplace=True)
fishDataPandas.columns = cols
print("Original Data:\n ", fishDataPandas)

fishDataPandas = impute(fishDataPandas)


plt.plot(fishDataPandas["X#wcentroid"], fishDataPandas["Y#wcentroid"])
plt.show()