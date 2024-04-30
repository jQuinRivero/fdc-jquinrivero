import pytest
from unittest.mock import patch
from fig_data_challenge.main import main
import pandas as pd


@pytest.fixture
def mock_data_reader():
    with patch("fig_data_challenge.main.DataReader") as mock:
        mock_instance = mock.return_value
        mock_instance.read_data.side_effect = lambda filepath, sheet_name: pd.DataFrame(
            {"store" if sheet_name == "Restaurant Menu Items" else "product_category": []}
        )
        yield mock_instance


@pytest.fixture
def mock_data_cleanser():
    with patch("fig_data_challenge.main.DataCleanser") as mock:
        mock_instance = mock.return_value
        mock_instance.cleanse_raw_data.return_value = pd.DataFrame(
            {"store": [], "product_category": [], "fig_category_1": []}
        )
        yield mock_instance


@pytest.fixture
def mock_data_transformer():
    with patch("fig_data_challenge.main.DataTransformer") as mock:
        mock.merge.return_value = pd.DataFrame(
            {"store": [], "product_category": [], "fig_category_1": []}
        )
        def drop_duplicates_and_na(df):
            return df.drop_duplicates().dropna()

        mock.drop_duplicates_and_na.side_effect = drop_duplicates_and_na
        yield mock


def test_main_integration(
    mock_data_reader, mock_data_cleanser, mock_data_transformer
):
    # Call the main function
    main()

    mock_data_reader.read_data.assert_called()
    mock_data_cleanser.cleanse_raw_data.assert_called()
    mock_data_transformer.merge.assert_called()
    mock_data_transformer.drop_duplicates_and_na.assert_called()
