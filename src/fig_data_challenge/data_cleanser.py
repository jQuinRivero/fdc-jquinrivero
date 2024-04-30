import pandas as pd
import re
import os
from typing import List, Dict, Optional
from pandas import DataFrame


class DataCleanser:
    def cleanse_raw_data(
        self,
        df: DataFrame,
        custom_mappings: Optional[Dict[str, str]] = None,
        drop_na_columns: Optional[List[str]] = None,
        columns_to_extract: Optional[List[str]] = None,
    ) -> DataFrame:
        """
        Cleanses the raw data according to the provided parameters.

        :param df: The DataFrame to cleanse.
        :param custom_mappings: A dictionary of custom column name mappings.
        :param drop_na_columns: A list of column names for which rows with missing values should be dropped.
        :param columns_to_extract: A list of column names to extract from the DataFrame.
        :return: The cleansed DataFrame.
        """
        try:
            column_mappings = {
                col: self._map_column_names(name=col, custom_mappings=custom_mappings)
                for col in df.columns
            }
            df = df.rename(columns=column_mappings)

            if drop_na_columns:
                updated_drop_na_columns = [
                    column_mappings.get(col, col) for col in drop_na_columns
                ]
                df = self._drop_missing_values(df, updated_drop_na_columns)

            if columns_to_extract:
                df = df[columns_to_extract]

            return df
        except Exception as e:
            print(f"Error occurred while cleansing data: {e}")
            return pd.DataFrame()

    def _map_column_names(
        self, name: str, custom_mappings: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Maps column names according to the provided custom mappings or default rules.

        :param name: The original column name.
        :param custom_mappings: A dictionary of custom column name mappings.
        :return: The mapped column name.
        """
        try:
            if custom_mappings and name in custom_mappings:
                return custom_mappings[name]

            name = re.sub("%", "_percentage", name)
            s1 = re.sub(r"([^0-9a-zA-Z_])", "_", name.lower())
            s2 = re.sub(r"_+", "_", s1)
            s3 = re.sub(r"^[^a-zA-Z_]+", "", s2)

            return s3
        except Exception as e:
            print(f"Error occurred while mapping column names: {e}")
            return name

    def _drop_missing_values(
        self, df: DataFrame, drop_na_columns: List[str]
    ) -> DataFrame:
        """
        Drops rows with missing values in the specified columns.

        :param df: The DataFrame from which to drop rows.
        :param drop_na_columns: A list of column names for which rows with missing values should be dropped.
        :return: The DataFrame with rows dropped.
        """
        try:
            df_with_drops = df.dropna(subset=drop_na_columns)
            rows_dropped = df.shape[0] - df_with_drops.shape[0]

            if rows_dropped > 0:
                self._log_filtered_rows(rows_dropped, drop_na_columns)

            return df_with_drops
        except Exception as e:
            print(f"Error occurred while dropping missing values: {e}")
            return df

    def _log_filtered_rows(self, rows_dropped: int, drop_na_columns: List[str]) -> None:
        """
        Logs the number of rows dropped due to missing values in the specified columns.

        :param rows_dropped: The number of rows dropped.
        :param drop_na_columns: The columns for which rows were dropped.
        """
        try:
            if not os.path.exists("data/logs"):
                os.makedirs("data/logs")
            with open("data/logs/dropped_rows.log", "a") as f:
                f.write(
                    f"Dropped {rows_dropped} rows with missing values in {drop_na_columns}\n"
                )
            print("File with dropped rows logged successfully! Saved to data/logs/dropped_rows.log")
        except Exception as e:
            print(f"Error occurred while logging filtered rows: {e}")
