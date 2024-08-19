import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.data_manipulation.TRexDataCleaner import TRexDataCleaner
from src.data_manipulation.TRexImputer import TRexImputer

# Parameters
num_rows = 100
max_velocity = 20

# Generate time values
time = np.arange(num_rows)

# Initialize X and Y coordinates
X = np.zeros(num_rows)
Y = np.zeros(num_rows)
np.random.seed(12)
# Generate random movements with a maximum velocity constraint
for i in range(1, num_rows):
    dx = np.random.uniform(-max_velocity, max_velocity)
    dy = np.random.uniform(-max_velocity, max_velocity)
    
    X[i] = X[i-1] + dx
    Y[i] = Y[i-1] + dy

# Create a DataFrame
data = pd.DataFrame({
    'time': time,
    'X': X,
    'Y': Y
})

# Define the function to zero out specific rows
def zero_out_rows(df, index1, index2):
    """
    Set the values of X and Y to 100 for the given row indices in the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    index1 (int): The index of the first row to modify.
    index2 (int): The index of the second row to modify.
    
    Returns:
    pd.DataFrame: The modified DataFrame with specified rows' X and Y values set to 100.
    """
    # Check if indices are within the range of the DataFrame
    if index1 < 0 or index2 < 0 or index1 >= len(df) or index2 >= len(df):
        raise IndexError("Index out of range.")
    
    # Set the values of X and Y for the specified indices to 100
    df.loc[[index1, index2], ['X', 'Y']] = 100
    
    return df

# Apply the function to zero out rows at indices 50 and 75
data_modified = zero_out_rows(data, 50, 75)

# Clean the data
data_cleaned, _ = TRexDataCleaner().renderDiscontinuities(data = data_modified, vmax = 40)

# Deep copy of the data
dat_to_impute = data_cleaned.copy()
imputer = TRexImputer()

# Impute the data using the 'avgValue' strategy
imputed_data = imputer.impute(dat_to_impute, function='avgValue')

# Create a single figure with subplots
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot original data
axs[0].plot(data['X'], data['Y'])
axs[0].set_title('Original Data')
axs[0].set_xlabel('X')
axs[0].set_ylabel('Y')

# Plot modified data
axs[1].plot(data_cleaned['X'], data_cleaned['Y'])
axs[1].set_title('Modified Data')
axs[1].set_xlabel('X')
axs[1].set_ylabel('Y')

# Plot imputed data
axs[2].plot(imputed_data['X'], imputed_data['Y'])
axs[2].set_title('Imputed Data')
axs[2].set_xlabel('X')
axs[2].set_ylabel('Y')

plt.tight_layout()
plt.show()
