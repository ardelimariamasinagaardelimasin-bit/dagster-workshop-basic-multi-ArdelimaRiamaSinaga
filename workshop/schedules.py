from dagster import ScheduleDefinition

from workshop.jobs import all_assets_job

daily_refresh = ScheduleDefinition(
    name="daily_refresh",
    job=all_assets_job,
    cron_schedule="0 6 * * *",
)

# TODO(exercise-2): add a second ScheduleDefinition here (e.g. an hourly
# refresh) — see docs/exercises.md

hourly_refresh = ScheduleDefinition(
    name="hourly_refresh",
    job=all_assets_job,
    cron_schedule="0 * * * *",
)