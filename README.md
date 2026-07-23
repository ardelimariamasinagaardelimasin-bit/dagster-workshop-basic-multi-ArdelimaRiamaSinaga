# dagster-workshop-basic

A single-container introduction to [Dagster](https://dagster.io): assets, jobs,
schedules, and resources, using a small generated retail dataset (customers,
products, orders).

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)

## How to Run

### Option A: Docker (recommended)

```bash
docker compose up --build
```

Then open http://localhost:3000. On first boot the container generates a fake
retail dataset into `data/` (50 customers, 20 products, 500 orders over the
last 30 days) — see `docker_entrypoint.py`.

In the UI, select all three assets (`raw_orders`, `cleaned_orders`,
`daily_revenue`) and click "Materialize all" to run the pipeline end to end.
You can also run the whole chain as a single job from the UI's Jobs tab by
launching `all_assets_job`, or trigger it on-demand from the Schedules tab
without waiting for the 06:00 cron fire.

Stop the container with `Ctrl+C`, or `docker compose down` to remove it.

### Option B: Local Python (no Docker)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
python seed_data.py           # only needed once, or whenever you want fresh fake data
dagster dev -f definitions.py
```

Then open http://localhost:3000 and materialize assets the same way as above.

## How to Verify the Run

A materialization is only "done" once you've confirmed it actually produced
correct output — checking the UI alone isn't enough since a run can succeed
with stale or empty data.

1. **Check run status in the UI.** After materializing, the Dagster UI shows
   each asset with a green "Materialized" state and a timestamp. Click into
   the run (Runs tab) to see the full step-by-step log; any failure shows up
   here as a red step with a stack trace.

2. **Inspect the output file.** `daily_revenue` writes its result to
   `data/daily_revenue.csv` via the `Warehouse` resource. After a successful
   run:

   ```bash
   cat data/daily_revenue.csv        # macOS/Linux
   type data\daily_revenue.csv       # Windows
   ```

   You should see one row per `order_date` with a non-empty `revenue` column,
   covering the last 30 days that `seed_data.py` generated.

3. **Check container/process logs.** With Docker, `docker compose logs -f`
   streams the same step logs shown in the UI — useful if the UI itself is
   unreachable. Locally, the `dagster dev` process prints them directly to
   the terminal it's running in.

4. **Run the test suite.** The tests don't require the UI or Docker and check
   the pipeline logic in isolation (asset transformations, resource I/O, and
   that `Definitions` wires up the expected assets/job/schedule):

   ```bash
   pip install -r requirements.txt   # if not already installed
   pytest
   ```

   All tests passing confirms the code is correct even before you materialize
   anything by hand; materializing in the UI then confirms the wiring and
   environment (Docker, ports, volumes) also work end to end.

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
