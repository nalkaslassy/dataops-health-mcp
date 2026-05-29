from src.aws.clients import is_mock
from src.mock.mock_data import MOCK_SFN_FAILURES_DATA
from src.schemas.outputs import SfnFailuresOutput


def find_sfn_failures() -> dict:
    """
    Returns failed Step Functions executions within a lookback window.

    Mock mode: returns static failure examples from mock/mock_data.py.
    Live mode: TODO — call sfn_client.list_executions(statusFilter="FAILED") per state machine.
    """
    if not is_mock():
        # TODO (Phase 1 live mode): call Step Functions API here.
        # client = get_sfn_client()
        # raw = client.list_executions(stateMachineArn=arn, statusFilter="FAILED")
        # return _parse_sfn_failures(raw)
        raise NotImplementedError("Live AWS mode is not implemented yet. Set DATAOPS_MODE=mock.")

    data = {**MOCK_SFN_FAILURES_DATA, "mode": "mock"}
    output = SfnFailuresOutput(**data)
    return output.model_dump()
