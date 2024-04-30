import pandas as pd
import re
import os


class DataCleanser:

    def cleanse_raw_data(
        self, df, custom_mappings=None, drop_na_columns=None, columns_to_extract=None
    ):
        column_mappings = {
            col: self._map_column_names(name=col, custom_mappings=custom_mappings)
            for col in df.columns
        }
        # Rename columns using the mappings
        df = df.rename(columns=column_mappings)

        # If drop_na_columns are provided, drop rows with missing values in those columns
        if drop_na_columns:
            df = self._drop_missing_values(df, drop_na_columns)

        # If columns_to_extract are provided, extract only those columns
        if columns_to_extract:
            df = self._extract_columns(df, columns_to_extract)

        return df

    def _map_column_names(self, name, custom_mappings=None):
        # Check for custom mappings
        if custom_mappings and name in custom_mappings:
            return custom_mappings[name]

        # Replace '%' with 'percentage' using a regular expression
        name = re.sub("%", "_percentage", name)

        # Convert to lowercase and replace special characters and spaces with underscores
        s1 = re.sub(r"([^0-9a-zA-Z_])", "_", name.lower())

        # Replace multiple occurrences of underscores with a single underscore
        s2 = re.sub(r"_+", "_", s1)

        # Remove leading characters until we find a letter or underscore
        s3 = re.sub(r"^[^a-zA-Z_]+", "", s2)

        return s3

    def _drop_missing_values(self, df, drop_na_columns):
        # Drop rows with missing values in the specified columns
        df_with_drops = df.dropna(subset=drop_na_columns)

        # Write the rows being dropped to a log file
        rows_dropped = df.shape[0] - df_with_drops.shape[0]

        if rows_dropped > 0:
            self._log_filtered_rows(rows_dropped, drop_na_columns)

        return df_with_drops

    def _extract_columns(self, df, columns_to_extract):
        # Extract only the specified columns from the DataFrame

        return df[columns_to_extract]

    def _log_filtered_rows(self, rows_dropped, drop_na_columns):
        # Write the rows being dropped to a log file
        if os.path.exists("data/logs") == False:
            os.makedirs("data/logs")
        with open("data/logs/dropped_rows.log", "a") as f:
            f.write(
                f"Dropped {rows_dropped} rows with missing values in {drop_na_columns}\n"
            )

        return
