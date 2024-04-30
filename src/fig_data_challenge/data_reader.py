import pandas as pd
import os


class DataReader:
    def read_data(self, filepath, **kwargs):
        """
        Reads data from a file based on the extension and returns a pandas DataFrame.

        :param filepath: The path to the data file.
        :param kwargs: Additional keyword arguments to pass to the pandas read function.
        :return: pandas DataFrame containing the data from the file.
        """
        # Determine the file extension
        _, extension = os.path.splitext(filepath)
        extension = extension.lower()

        # Select the appropriate pandas read function based on file extension
        if extension == ".csv":
            return pd.read_csv(filepath, **kwargs)
        elif extension in [".xls", ".xlsx"]:
            return pd.read_excel(filepath, **kwargs)
        # Add additional conditions for other file types if necessary
        else:
            raise NotImplementedError(
                f"Reading data from files with extension '{extension}' is not supported."
            )
