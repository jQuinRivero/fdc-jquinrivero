import pandas as pd
from typing import List, Union
from pandas import DataFrame

class DataTransformer:
    @staticmethod
    def merge(df1: DataFrame, df2: DataFrame, columns: Union[str, List[str]], how: str = "left") -> Union[DataFrame, None]:
        """
        Merges two DataFrames on the specified columns.

        :param df1: The first DataFrame to merge.
        :param df2: The second DataFrame to merge.
        :param columns: The column or list of columns to merge on.
        :param how: The type of merge to be performed. Default is "left".
        :return: The merged DataFrame.
        """
        try:
            merged_df = pd.merge(
                df1,
                df2,
                on=columns,
                how=how,
            )

            return merged_df
        except Exception as e:
            print(f"Error occurred while merging data: {e}")
            return None
    
    @staticmethod
    def drop_duplicates_and_na(df: DataFrame) -> Union[DataFrame, None]:
        """
        Drops duplicate rows and rows with missing values from the DataFrame.

        :param df: The DataFrame to process.
        :return: The processed DataFrame.
        """
        try:
            df = df.drop_duplicates().dropna().copy()

            return df
        except Exception as e:
            print(f"Error occurred while dropping duplicates and missing values: {e}")
            return None