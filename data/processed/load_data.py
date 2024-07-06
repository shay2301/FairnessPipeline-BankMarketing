import pandas as pd

def load_data(file_path, delimiter=";"):
    data = pd.read_csv(file_path, delimiter=delimiter)
    return data
