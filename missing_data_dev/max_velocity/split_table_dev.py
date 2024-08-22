import pandas as pd
import numpy as np
import os

def split_table(df, save_to_folder=False, folder_path=None):
    """ Splits valid data into tables
    
    Parameters:
    -----------
        df: pd.dataframe
            The input dataframe to be split
        save_to_folder: 
    """
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


     # Save tables to folder if specified
    if save_to_folder and folder_path:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        save_tables(tables, folder_path)

    return tables


def save_tables(tables, folder_path):
    for index, table in enumerate(tables):
        table.to_csv(os.path.join(folder_path, f'table_{index}.csv'), index=False)



