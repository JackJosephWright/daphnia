"""if x or y is inf/NaN,
save tables as dataframes
    break and start new table
"""

import pandas as pd
import numpy as np


clean_data = r"/Users/ibrahimrahat/Documents/GitHub/daphnia/data/clean_fish_data/fish_data_clean.csv"

df = pd.read_csv(clean_data, index_col=False)


def split_table(df):
    #remove unwanted columns
    for col in df.columns:
        print(col)
        if col not in ['X','Y','time']:
            df = df.drop(columns = col)
    
    tables = []  #list to store dataframes
    temp_table = None

    for _, row in df.iterrows():
        
        if np.isinf(row['X']) or np.isinf(row['Y']):
            if temp_table is not None:
                tables.append(temp_table)
                temp_table = None
            else:
                continue
        else:
            if temp_table is None:
                temp_table = row.to_frame().T
            else:
                temp_table.loc[len(temp_table)] = row.tolist()
    if temp_table is not None:
        tables.append(temp_table)
                
    return tables


def save_tables(tables):
    for index, table in enumerate(tables):
        table.to_csv(f'table_{index}.csv', index=False)



