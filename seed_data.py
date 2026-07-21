import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

DATA_DIR = Path(__file__).parent / "data"
NUM_CUSTOMERS = 50
NUM_PRODUCTS = 20
NUM_ORDERS = 500

CATEGORIES = ["electronics", "home", "clothing", "toys", "books"]


def generate_customers(fake: Faker) -> pd.DataFrame:
    rows = []
    for customer_id in range(1, NUM_CUSTOMERS + 1):
        rows.append(
            {
                "customer_id": customer_id,
                "name": fake.name(),
                "email": fake.email(),
                "signup_date": fake.date_between(start_date="-2y", end_date="-30d"),
            }
        )
    return pd.DataFrame(rows)


def generate_products(fake: Faker) -> pd.DataFrame:
    rows = []
    for product_id in range(1, NUM_PRODUCTS + 1):
        rows.append(
            {
                "product_id": product_id,
                "name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
                "category": random.choice(CATEGORIES),
                "price": round(random.uniform(5, 200), 2),
            }
        )
    return pd.DataFrame(rows)


def generate_orders(fake: Faker) -> pd.DataFrame:
    rows = []
    today = datetime.now().date()
    for order_id in range(1, NUM_ORDERS + 1):
        order_date = today - timedelta(days=random.randint(0, 30))
        rows.append(
            {
                "order_id": order_id,
                "customer_id": random.randint(1, NUM_CUSTOMERS),
                "product_id": random.randint(1, NUM_PRODUCTS),
                "quantity": random.randint(1, 5),
                "order_date": order_date.isoformat(),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    generate_customers(fake).to_csv(DATA_DIR / "customers.csv", index=False)
    generate_products(fake).to_csv(DATA_DIR / "products.csv", index=False)
    generate_orders(fake).to_csv(DATA_DIR / "orders.csv", index=False)
    print(
        f"Seeded {NUM_CUSTOMERS} customers, {NUM_PRODUCTS} products, "
        f"{NUM_ORDERS} orders into {DATA_DIR}"
    )


if __name__ == "__main__":
    main()
