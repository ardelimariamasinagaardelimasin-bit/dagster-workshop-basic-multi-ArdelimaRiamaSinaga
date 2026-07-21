import pandas as pd
from dagster import materialize

from workshop.assets import cleaned_orders, daily_revenue, raw_orders
from workshop.resources import Warehouse


def test_daily_revenue_pipeline_dedupes_and_aggregates(tmp_path):
    pd.DataFrame(
        {
            "order_id": [1, 2, 2],
            "customer_id": [10, 11, 11],
            "product_id": [100, 101, 101],
            "quantity": [2, 1, 1],
            "order_date": ["2026-01-01", "2026-01-01", "2026-01-01"],
        }
    ).to_csv(tmp_path / "orders.csv", index=False)

    pd.DataFrame(
        {
            "product_id": [100, 101],
            "name": ["Widget", "Gadget"],
            "category": ["tools", "tools"],
            "price": [9.99, 4.99],
        }
    ).to_csv(tmp_path / "products.csv", index=False)

    result = materialize(
        [raw_orders, cleaned_orders, daily_revenue],
        resources={"warehouse": Warehouse(data_dir=str(tmp_path))},
    )

    assert result.success
    output = pd.read_csv(tmp_path / "daily_revenue.csv")
    assert len(output) == 1
    assert output.loc[0, "order_date"] == "2026-01-01"
    assert output.loc[0, "revenue"] == 2 * 9.99 + 1 * 4.99
