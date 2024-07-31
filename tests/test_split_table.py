from  missing_data_dev.max_velocity.split_table_dev import split_table
import pandas as pd

Clean_data = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/clean_fish_data/fish_data_clean.csv"

df = pd.read_csv(Clean_data)

print(df)
