import numpy as np
import pandas as pd

# array of x, y, time vectors
data = [['time', 'x', 'y']] + [[i, i, i] for i in range(10)]
print("Original data: ", data)

# zip array
def zipArray(data: list, save_dir: str):
    np.savez(save_dir, data)

#unzip array
def unzipArray(source_dir: str) -> list:
    unzippedArray = np.load(source_dir)
    unzippedArray = [unzippedArray[i] for i in unzippedArray.keys()]

    return unzippedArray[0]

def pandafy(data: list):
    return pd.DataFrame(data = data[1:], columns = data[0])

zipArray(data, 'zipped.npz')

unzippedArray = unzipArray('zipped.npz')
print("Unzipped data: ", unzippedArray)

print("Panda table: \n", pandafy(unzippedArray))

