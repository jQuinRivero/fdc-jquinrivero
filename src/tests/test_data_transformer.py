import pandas as pd  
import pytest  
from fig_data_challenge.data_transformer import DataTransformer  
  
def test_merge_inner():  
    df1 = pd.DataFrame({'key': [1, 2], 'value1': [10, 20]})  
    df2 = pd.DataFrame({'key': [2, 3], 'value2': [30, 40]})  
    merged_df = DataTransformer.merge(df1, df2, 'key', 'inner')  
    assert len(merged_df) == 1  
    assert merged_df['value1'].iloc[0] == 20  
    assert merged_df['value2'].iloc[0] == 30  
  
def test_merge_left():  
    df1 = pd.DataFrame({'key': [1, 2], 'value1': [10, 20]})  
    df2 = pd.DataFrame({'key': [2, 3], 'value2': [30, 40]})  
    merged_df = DataTransformer.merge(df1, df2, 'key', 'left')  
    assert len(merged_df) == 2  
    assert pd.isna(merged_df['value2'].iloc[0])  
  
def test_merge_multiple_keys():  
    df1 = pd.DataFrame({'key1': [1, 1], 'key2': ['A', 'B'], 'value1': [10, 20]})  
    df2 = pd.DataFrame({'key1': [1, 1], 'key2': ['B', 'C'], 'value2': [30, 40]})  
    merged_df = DataTransformer.merge(df1, df2, ['key1', 'key2'], 'inner')  
    assert len(merged_df) == 1  
    assert merged_df['value1'].iloc[0] == 20  
    assert merged_df['value2'].iloc[0] == 30  
  
def test_drop_duplicates_and_na():  
    df = pd.DataFrame({  
        'key': [1, 2, 2, None],  
        'value': [10, 20, 20, 30]  
    })  
    processed_df = DataTransformer.drop_duplicates_and_na(df)  
    assert len(processed_df) == 2  
    assert processed_df['key'].tolist() == [1, 2]  
    assert processed_df['value'].tolist() == [10, 20]  
  
if __name__ == "__main__":  
    pytest.main()  
