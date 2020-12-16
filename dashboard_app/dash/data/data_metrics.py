import pandas as pd


def get_total_sum_from_column(df, column):
    """
    Gets the total sum of a specific column
    @param df: Targeted DataFrame
    @param column: Targeted Column
    @return: returns an sum in a string
    """
    return str(df[column].sum())
