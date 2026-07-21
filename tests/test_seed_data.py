from faker import Faker

from seed_data import (
    NUM_CUSTOMERS,
    NUM_ORDERS,
    NUM_PRODUCTS,
    generate_customers,
    generate_orders,
    generate_products,
)


def test_generate_customers_has_expected_columns_and_row_count():
    fake = Faker()
    Faker.seed(1)
    df = generate_customers(fake)
    assert len(df) == NUM_CUSTOMERS
    assert list(df.columns) == ["customer_id", "name", "email", "signup_date"]
    assert df["customer_id"].tolist() == list(range(1, NUM_CUSTOMERS + 1))


def test_generate_products_has_expected_columns_and_row_count():
    fake = Faker()
    Faker.seed(1)
    df = generate_products(fake)
    assert len(df) == NUM_PRODUCTS
    assert list(df.columns) == ["product_id", "name", "category", "price"]
    assert (df["price"] > 0).all()


def test_generate_orders_references_valid_customer_and_product_ids():
    fake = Faker()
    Faker.seed(1)
    df = generate_orders(fake)
    assert len(df) == NUM_ORDERS
    assert list(df.columns) == [
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "order_date",
    ]
    assert df["customer_id"].between(1, NUM_CUSTOMERS).all()
    assert df["product_id"].between(1, NUM_PRODUCTS).all()
    assert (df["quantity"] >= 1).all()
