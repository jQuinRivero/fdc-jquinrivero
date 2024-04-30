import os
import pandas as pd
from typing import Any, Dict, Union
from pandas import DataFrame


class DataReader:
    def read_data(
        self, filepath: str, **kwargs: Dict[str, Any]
    ) -> Union[DataFrame, None]:
        """
        Reads data from a file based on the extension and returns a pandas DataFrame.

        :param filepath: The path to the data file.
        :param kwargs: Additional keyword arguments to pass to the pandas read function.
        :return: pandas DataFrame containing the data from the file.
        """
        # Determine the file extension
        _, extension = os.path.splitext(filepath)
        extension = extension.lower() if extension else extension

        # Select the appropriate pandas read function based on file extension
        if extension == ".csv":
            return pd.read_csv(filepath, **kwargs)
        elif extension in [".xls", ".xlsx"]:
            return pd.read_excel(filepath, **kwargs)

        else:
            raise NotImplementedError(
                f"Reading data from files with extension '{extension}' is not supported."
            )
