# Exercises

Each exercise has a `# TODO(exercise-N)` comment in the source marking where
to add your code. Work through them in order.

## ① Add a `top_products` asset

**File:** `workshop/assets.py`

Add a new `@asset` named `top_products` that depends on `cleaned_orders`,
groups by `product_id`, sums `quantity`, and returns the top 5 products by
total quantity sold. Add it to the `assets=[...]` list in `definitions.py` so
it shows up in the UI.

Hint: `cleaned_orders.groupby("product_id")["quantity"].sum().nlargest(5)`.

## ② Add a second schedule

**File:** `workshop/schedules.py`

Add a second `ScheduleDefinition` (e.g. `hourly_refresh`) that runs
`all_assets_job` every hour instead of once a day. Add it to the
`schedules=[...]` list in `definitions.py`.

Hint: cron syntax for "every hour" is `"0 * * * *"`.

## ③ Add a data-quality asset check

**File:** `workshop/assets.py`

Add an `@asset_check` on `cleaned_orders` that fails if any row has
`quantity <= 0`. Register it in `definitions.py` via the `asset_checks=[...]`
argument to `Definitions`.

Hint: see the [Dagster asset checks docs](https://docs.dagster.io/concepts/assets/asset-checks)
for the `@asset_check` decorator signature.
