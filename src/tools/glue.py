from datetime import datetime, timedelta, timezone

from src.aws.clients import is_mock, get_glue_client
from src.mock.mock_data import MOCK_GLUE_FAILURES_DATA
from src.schemas.outputs import GlueFailuresOutput


def find_glue_failures(lookback_hours: int = 24) -> dict:
    """
    Returns failed AWS Glue job runs in the last 24 hours.
    Shows job name, run ID, error message, and how long the job ran before failing.
    Currently runs in mock mode — no real AWS calls are made.
    """
    if not is_mock():
        return _get_live_glue_failures(lookback_hours)

    data = {**MOCK_GLUE_FAILURES_DATA, "mode": "mock"}
    output = GlueFailuresOutput(**data)
    return output.model_dump()


def _get_live_glue_failures(lookback_hours: int) -> dict:
    client = get_glue_client()

    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

    job_names = client.list_jobs()["JobNames"]

    failures = []
    for job_name in job_names:
        runs = client.get_job_runs(JobName=job_name)["JobRuns"]
        for run in runs:
            if run["JobRunState"] == "FAILED" and run["StartedOn"] >= cutoff:
                failures.append({
                    "job_name": job_name,
                    "run_id": run["Id"],
                    "started_at": run["StartedOn"].isoformat(),
                    "failed_at": run.get("CompletedOn", run["StartedOn"]).isoformat(),
                    "error_message": run.get("ErrorMessage", "No error message available."),
                    "duration_minutes": round(run.get("ExecutionTime", 0) / 60),
                })

    data = {
        "lookback_hours": lookback_hours,
        "failures": failures,
        "total_failures": len(failures),
        "mode": "live",
    }

    output = GlueFailuresOutput(**data)
    return output.model_dump()
