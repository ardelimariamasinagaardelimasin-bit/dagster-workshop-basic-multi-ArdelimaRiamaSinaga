# dagster-workshop-basic

A single-container introduction to [Dagster](https://dagster.io): assets, jobs,
schedules, and resources, using a small generated retail dataset (customers,
products, orders).

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)

## Quickstart

```bash
docker compose up --build
```

Then open http://localhost:3000. On first boot the container generates a fake
retail dataset into `data/` (50 customers, 20 products, 500 orders over the
last 30 days).

In the UI, select all three assets and click "Materialize all" to run the
pipeline end to end.

## What just happened

```
seed_data.py --> data/customers.csv, data/products.csv, data/orders.csv
                        |
                        v
                  raw_orders (asset)
                        |
                        v
                 cleaned_orders (asset)   <- dedupes by order_id, drops nulls
                        |
                        v
                 daily_revenue (asset)    <- joins products, aggregates by day
                        |
                        v
                data/daily_revenue.csv
```

A `Warehouse` **resource** (`workshop/resources.py`) wraps the `data/`
directory so assets don't hard-code file paths. A **schedule**
(`daily_refresh`) re-runs the whole chain every day at 06:00 — you won't see
it fire in a short workshop session, but you can trigger it manually from the
UI's Schedules tab, or just materialize assets directly.

## Exercises

See [docs/exercises.md](docs/exercises.md) for three hands-on TODOs, in
increasing difficulty. Each one has a `# TODO(exercise-N)` comment marking
where to add your code.

## How this maps to the production pipeline

This workshop scaffold is adapted from a real Dagster + Docker production
system that runs 20+ independent pipeline containers pulling manufacturing
data into a central database. This single-container version keeps the same
core Dagster concepts (`@asset`, `define_asset_job`, `ScheduleDefinition`,
resources) but drops the multi-container / gRPC / shared-Postgres
architecture for simplicity. See `dagster-workshop-multi` for that version.
