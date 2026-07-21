from dagster import Definitions

from definitions import defs


def test_defs_registers_expected_assets_jobs_and_schedules():
    assert isinstance(defs, Definitions)

    asset_keys = {ak.to_user_string() for ak in defs.get_asset_graph().get_all_asset_keys()}
    assert {"raw_orders", "cleaned_orders", "daily_revenue"} <= asset_keys

    job = defs.get_job_def("all_assets_job")
    assert job.name == "all_assets_job"

    schedule = defs.get_schedule_def("daily_refresh")
    assert schedule.cron_schedule == "0 6 * * *"
