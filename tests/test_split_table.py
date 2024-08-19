from  missing_data_dev.max_velocity.split_table_dev import split_table
import pandas as pd

# clean_data = r"data/npz_file/single_7_9_fish1.MP4_fish0.npz"
clean_data = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/clean_fish_data/fish_data_clean.csv"

df = pd.read_csv(clean_data)

# set save_to_folder to True if you want to save to folder
tables = split_table(df, save_to_folder=False, folder_path='output_folder')

# index of what table you want to access
first_table = tables[0]
print(first_table)

# number of tables
num_tables = len(tables)
print(num_tables)

