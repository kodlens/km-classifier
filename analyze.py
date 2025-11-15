import pandas as pd

def summary_stats(df: pd.DataFrame):
    """
    Return basic summary statistics of the dataset.
    """
    return df.describe()
