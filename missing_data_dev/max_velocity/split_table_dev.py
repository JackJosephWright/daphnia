"""if x or y is inf/NaN,
save tables as dataframes
    break and start new table
"""


import pandas as pd
import numpy as np


Clean_data = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/clean_fish_data/fish_data_clean.csv"

df = pd.read_csv(Clean_data)


def split_table(df):
    tables = []  #list to store dataframes
    index = 0  #starting index

    for i, row in df.iterrows():
        # print(i)
        # print(row)
        if np.isinf(row['X']) or np.isinf(row['Y']):
            # creates a df for the current iteration
            new_table = df.iloc[index:i]
            tables.append(new_table)
            index = i + 1 # update index for next segment

    if index < len(df):
        new_table = df.iloc[index:]
        tables.append(new_table)
    
    return tables


def save_tables(tables):
    for index, table in enumerate(tables):
        table.to_csv(f'table_{index}.csv', index=False)

tables = split_table(df)
save_tables(tables)




    # for df["X","Y"] in df:
    #     if df["X","Y"] == pd.isinf(x)
    #     break

