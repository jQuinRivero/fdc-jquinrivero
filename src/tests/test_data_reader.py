import pytest
import pandas as pd
from fig_data_challenge.data_reader import DataReader


# Fixture to create and delete temporary test files
@pytest.fixture(scope="module")
def test_files(tmp_path_factory):
    # Create a temporary directory
    tmp_dir = tmp_path_factory.mktemp("data")
    # CSV test file
    csv_file = tmp_dir / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")
    # Excel test file
    excel_file = tmp_dir / "test.xlsx"
    df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    df.to_excel(excel_file, index=False)
    # Return file paths
    yield {
        "csv": str(csv_file),
        "excel": str(excel_file),
    }
    # Teardown (optional, since tmp_path_factory will handle cleanup)


def test_read_csv(test_files):
    data_reader = DataReader()
    df = data_reader.read_data(test_files["csv"])
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1


def test_read_excel(test_files):
    data_reader = DataReader()
    df = data_reader.read_data(test_files["excel"])
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]
    assert df.iloc[0]["col1"] == 1


def test_unsupported_extension():
    data_reader = DataReader()
    with pytest.raises(NotImplementedError):
        data_reader.read_data("test.unsupported")


def test_invalid_file_path():
    data_reader = DataReader()
    with pytest.raises(FileNotFoundError):
        data_reader.read_data("non_existent_file.csv")


if __name__ == "__main__":
    pytest.main()
