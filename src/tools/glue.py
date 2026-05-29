from src.aws.clients import is_mock
from src.mock.mock_data import MOCK_GLUE_FAILURES_DATA
from src.schemas.outputs import GlueFailuresOutput


def find_glue_failures() -> dict:
    """
    Returns failed Glue job runs within a lookback window.

    Mock mode: returns static failure examples from mock/mock_data.py.
    Live mode: TODO — call glue_client.get_job_runs() and filter by JobRunState == "FAILED".
    """
    if not is_mock():
        # TODO (Phase 1 live mode): call Glue API here.
        # client = get_glue_client()
        # raw = client.get_job_runs(JobName=job_name)
        # return _parse_glue_failures(raw)
        raise NotImplementedError("Live AWS mode is not implemented yet. Set DATAOPS_MODE=mock.")

    data = {**MOCK_GLUE_FAILURES_DATA, "mode": "mock"}
    output = GlueFailuresOutput(**data)
    return output.model_dump()
