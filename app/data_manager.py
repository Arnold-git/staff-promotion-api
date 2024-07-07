# Load data
import pandas as pd

def load_data(train_path):
    df_train = pd.read_csv(train_path)
    return df_train


