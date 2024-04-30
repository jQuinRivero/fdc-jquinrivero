import pandas as pd

class DataTransformer:

    def merge(df1, df2, columns, how="left"):
        merged_df = pd.merge(
            df1,
            df2,
            on=columns,
            how=how,
        )

        return merged_df
    
    def extract_subset_columns(df, columns):
        return df[columns]