import pandas as pd
import pytest
from fig_data_challenge.data_cleanser import DataCleanser


def test_map_column_names():
    data_cleanser = DataCleanser()
    custom_mappings = {"Col 1": "column_one", "col-2": "column_two"}
    mapped_name = data_cleanser._map_column_names(
        "Col 1", custom_mappings=custom_mappings
    )
    assert mapped_name == "column_one"
    mapped_name = data_cleanser._map_column_names(
        "col-2", custom_mappings=custom_mappings
    )
    assert mapped_name == "column_two"

    mapped_name = data_cleanser._map_column_names("Col @#$ 3")
    assert mapped_name == "col_3"


def test_drop_missing_values():
    data_cleanser = DataCleanser()
    df = pd.DataFrame({"col1": [1, 2, None], "col2": [4, None, 6]})
    cleansed_df = data_cleanser._drop_missing_values(df, ["col1"])
    assert cleansed_df.shape[0] == 2


def test_cleanse_raw_data():
    data_cleanser = DataCleanser()
    df = pd.DataFrame(
        {"Col 1": [1, 2, None], "col-2": [4, None, 6], "extra_col": [7, 8, 9]}
    )
    custom_mappings = {"Col 1": "column_one", "col-2": "column_two"}
    cleansed_df = data_cleanser.cleanse_raw_data(
        df,
        custom_mappings=custom_mappings,
        drop_na_columns=["Col 1"],
        columns_to_extract=["column_one", "column_two"],
    )
    assert "column_one" in cleansed_df.columns
    assert "column_two" in cleansed_df.columns
    assert "extra_col" not in cleansed_df.columns
    assert cleansed_df.shape[0] == 2


if __name__ == "__main__":
    pytest.main()
