import numpy as np


def load_data(file_path):

    # Specify the file path
    #file_path = 'activity.csv'

    # Use numpy.genfromtxt to read the CSV data from the file into a NumPy array
    data_array = np.genfromtxt(file_path, delimiter=',', dtype=None, names=True)

    # Transpose the array to have each column in a separate NumPy array
    column_names = data_array.dtype.names
    column_arrays = {column: data_array[column] for column in column_names}

    # Print each column
    #for column, array in column_arrays.items():
    #    print(f"{column}: {array}")

    return column_arrays



  