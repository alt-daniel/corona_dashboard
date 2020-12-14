import pandas as pd

def create_dataframe():
    return pd.DataFrame()


def create_csv_from_dataframe(source, seperator = ';'):
    return pd.read_csv(source, sep=seperator)