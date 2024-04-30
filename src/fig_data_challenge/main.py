from .data_reader import DataReader
from .data_cleanser import DataCleanser
from .data_transformer import DataTransformer
from .database_handler import DatabaseHandler

def main():
    try:
        print("Starting the data processing pipeline...")
        # Phase 1: Data Reading
        data_reader = DataReader()

        print("Reading the restaurant menu items data...")
        # Read the restaurant menu items data
        restaurant_menu_items_df = data_reader.read_data(
            filepath="data/restaurant_data.xlsx", sheet_name="Restaurant Menu Items"
        )

        # Read the reference categories data
        reference_categories_df = data_reader.read_data(
            filepath="data/restaurant_data.xlsx", sheet_name="Reference categories"
        )

        print("Data read successfully!")
        # Phase 2: Data Cleansing
        print("Starting the data cleansing process...")
        data_cleanser = DataCleanser()

        # Cleanse the restaurant menu items data
        restaurant_menu_items_df = data_cleanser.cleanse_raw_data(
            df=restaurant_menu_items_df,
            custom_mappings={"#": "id", "Unnamed: 1": "date_acquisition"},
            drop_na_columns=["ingredients_on_product_page", "product_name"],
            columns_to_extract=[
                "store",
                "product_name",
                "ingredients_on_product_page",
                "allergens_and_warnings",
                "url_of_primary_product_picture",
                "product_category",
            ],
        )

        # Cleanse the reference categories data
        reference_categories_df = data_cleanser.cleanse_raw_data(
            df=reference_categories_df,
            custom_mappings={
                "Restaurant original category": "product_category",
                "Restaurant name": "store",
            },
        )

        # Phase 3: Data Transformation
        # Merge the restaurant menu items data with the reference categories data
        merged_df = DataTransformer.merge(
            df1=restaurant_menu_items_df,
            df2=reference_categories_df,
            columns=["product_category", "store"],
            how="left",
        )

        print("Data cleansing and transformation completed successfully!")
        # Phase 4: Database Handling
        # Initialize the DatabaseHandler
        print("Starting the database handling process...")
        db_handler = DatabaseHandler(db_path="database.db")

        # Dedup and drop NA values from the Master values
        unique_stores_df = DataTransformer.drop_duplicates_and_na(merged_df[["store"]])
        unique_categories_df = DataTransformer.drop_duplicates_and_na(
            merged_df[["product_category"]]
        )
        unique_fig_categories_df = DataTransformer.drop_duplicates_and_na(
            merged_df[["fig_category_1"]]
        )

        # Upsert the unique store names into the Stores table
        store_id_mapping = {}
        for store_name in unique_stores_df["store"].unique():
            store_id = db_handler.get_store_id(store_name) or db_handler.upsert_store(
                store_name
            )
            store_id_mapping[store_name] = store_id

        # Upsert the unique category names into the Categories table
        category_id_mapping = {}
        for category_name in unique_categories_df["product_category"].unique():
            category_id = db_handler.get_category_id(
                category_name
            ) or db_handler.upsert_category(category_name)
            category_id_mapping[category_name] = category_id

        # Upsert the unique fig category names into the FigCategories table
        fig_category_id_mapping = {}
        for fig_category_name in unique_fig_categories_df["fig_category_1"].dropna().unique():
            fig_category_id = db_handler.get_fig_category_id(
                fig_category_name
            ) or db_handler.upsert_fig_category(fig_category_name)
            fig_category_id_mapping[fig_category_name] = fig_category_id

        # Upsert products using the mappings for foreign keys
        for _, row in merged_df.iterrows():
            store_id = store_id_mapping.get(row["store"])
            category_id = category_id_mapping.get(row["product_category"])
            fig_category_id = fig_category_id_mapping.get(row.get("fig_category_1"))

            db_handler.upsert_product(
                store_id=store_id,
                category_id=category_id,
                fig_category_id=fig_category_id,
                product_name=row["product_name"],
                ingredients=row.get("ingredients_on_product_page", ""),
                allergens=row.get("allergens_and_warnings", ""),
                picture_url=row["url_of_primary_product_picture"],
            )

        print("Data successfully inserted into the database!")

    except Exception as e:
        print(f"Error occurred while processing data: {e}")

if __name__ == "__main__":
    main()