# ==== DATA ====

import pandas as pd

DATA_PATH = "./US_Accidents_March23.csv"

# Load once (global)
_df = pd.read_csv(DATA_PATH)


def get_all_data():
    return _df


def get_limited_data(n):
    return _df.head(n)