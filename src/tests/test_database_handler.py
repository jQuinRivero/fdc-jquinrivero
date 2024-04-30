import pytest
from fig_data_challenge.database_handler import DatabaseHandler


@pytest.fixture
def db_handler():
    # Set up an in-memory database for testing
    handler = DatabaseHandler(db_path=":memory:")
    handler.create_tables()  # Assuming you have a method to create tables
    yield handler
    handler.conn.close()


def test_upsert_store(db_handler):
    store_name = "Test Store"
    store_id = db_handler.upsert_store(store_name)
    assert store_id is not None
    assert db_handler.get_store_id(store_name) == store_id


def test_upsert_store_duplicate(db_handler):
    store_name = "Test Store"
    store_id_1 = db_handler.upsert_store(store_name)
    store_id_2 = db_handler.upsert_store(store_name)
    assert store_id_1 == store_id_2


def test_upsert_category(db_handler):
    category_name = "Test Category"
    category_id = db_handler.upsert_category(category_name)
    assert category_id is not None
    assert db_handler.get_category_id(category_name) == category_id


def test_upsert_category_duplicate(db_handler):
    category_name = "Test Category"
    category_id_1 = db_handler.upsert_category(category_name)
    category_id_2 = db_handler.upsert_category(category_name)
    assert category_id_1 == category_id_2


def test_upsert_fig_category(db_handler):
    fig_category_name = "Test FigCategory"
    fig_category_id = db_handler.upsert_fig_category(fig_category_name)
    assert fig_category_id is not None
    assert db_handler.get_fig_category_id(fig_category_name) == fig_category_id


def test_upsert_fig_category_duplicate(db_handler):
    fig_category_name = "Test FigCategory"
    fig_category_id_1 = db_handler.upsert_fig_category(fig_category_name)
    fig_category_id_2 = db_handler.upsert_fig_category(fig_category_name)
    assert fig_category_id_1 == fig_category_id_2


def test_upsert_product(db_handler):
    # Assuming you have a method `upsert_product` and a way to retrieve product
    store_id = db_handler.upsert_store("Test Store")
    category_id = db_handler.upsert_category("Test Category")
    fig_category_id = db_handler.upsert_fig_category("Test FigCategory")
    product_info = {
        "store_id": store_id,
        "category_id": category_id,
        "fig_category_id": fig_category_id,
        "product_name": "Test Product",
        "ingredients": "Test Ingredients",
        "allergens": "Test Allergens",
        "picture_url": "http://testurl.com/testimage.jpg",
    }
    product_id = db_handler.upsert_product(**product_info)
    assert product_id is not None


if __name__ == "__main__":
    pytest.main()
