from  missing_data_dev.max_velocity.split_table_dev import split_table, save_tables
import pandas as pd

# clean_data = r"data/npz_file/single_7_9_fish1.MP4_fish0.npz"
clean_data = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/clean_fish_data/fish_data_clean.csv"

df = pd.read_csv(clean_data)


tables = split_table(df)
print(tables)

# save_tables(tables)
