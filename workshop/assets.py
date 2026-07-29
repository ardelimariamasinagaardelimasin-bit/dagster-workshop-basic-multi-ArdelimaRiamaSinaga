import pandas as pd
from dagster import AssetCheckResult, asset, asset_check

from workshop.resources import Warehouse


@asset
def raw_orders(warehouse: Warehouse) -> pd.DataFrame:
    return warehouse.read_csv("orders")


@asset
def cleaned_orders(raw_orders: pd.DataFrame) -> pd.DataFrame:
    return raw_orders.dropna(subset=["customer_id", "product_id"]).drop_duplicates(
        subset=["order_id"]
    )

# TODO(exercise-3): add a Dagster asset check on cleaned_orders that fails if
# any row has quantity <= 0 — see docs/exercises.md
@asset_check(asset=cleaned_orders)
def cleaned_orders_quality_check(cleaned_orders: pd.DataFrame) -> AssetCheckResult:
    invalid_rows = cleaned_orders[cleaned_orders["quantity"] <= 0]
    if not invalid_rows.empty:
        return AssetCheckResult(
            passed=False,
            description=f"Found {len(invalid_rows)} row(s) with quantity <= 0",
        )
    return AssetCheckResult(passed=True, description="All rows have valid quantity > 0")


@asset
def daily_revenue(cleaned_orders: pd.DataFrame, warehouse: Warehouse) -> pd.DataFrame:
    products = warehouse.read_csv("products")
    merged = cleaned_orders.merge(products, on="product_id")
    merged["revenue"] = merged["quantity"] * merged["price"]
    daily = merged.groupby("order_date", as_index=False)["revenue"].sum()
    warehouse.write_csv("daily_revenue", daily)
    return daily

# TODO(exercise-1): add a top_products asset downstream of cleaned_orders
# that ranks products by total quantity sold — see docs/exercises.md
@asset
def top_products(cleaned_orders: pd.DataFrame) -> pd.DataFrame:
    return (
        cleaned_orders
        .groupby("product_id")["quantity"]
        .sum()
        .nlargest(5)
        .reset_index(name="total_quantity")
    )
