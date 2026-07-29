from dagster import Definitions

from workshop.assets import cleaned_orders, cleaned_orders_quality_check, daily_revenue, raw_orders, top_products
from workshop.jobs import all_assets_job
from workshop.resources import Warehouse
from workshop.schedules import daily_refresh, hourly_refresh

defs = Definitions(
    assets=[
        raw_orders,
        cleaned_orders,
        daily_revenue,
        top_products,
    ],
    asset_checks=[
        cleaned_orders_quality_check,
    ],
    jobs=[all_assets_job],
    schedules=[
        daily_refresh,
        hourly_refresh,
    ],
    resources={"warehouse": Warehouse(data_dir="data")},
)
