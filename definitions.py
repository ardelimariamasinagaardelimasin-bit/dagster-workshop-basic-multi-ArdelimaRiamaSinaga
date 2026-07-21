from dagster import Definitions

from workshop.assets import cleaned_orders, daily_revenue, raw_orders
from workshop.jobs import all_assets_job
from workshop.resources import Warehouse
from workshop.schedules import daily_refresh

defs = Definitions(
    assets=[raw_orders, cleaned_orders, daily_revenue],
    jobs=[all_assets_job],
    schedules=[daily_refresh],
    resources={"warehouse": Warehouse(data_dir="data")},
)
