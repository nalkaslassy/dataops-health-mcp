from datetime import datetime, timedelta, timezone

from src.aws.clients import is_mock, get_sfn_client
from src.mock.mock_data import MOCK_SFN_FAILURES_DATA
from src.schemas.outputs import SfnFailuresOutput


def find_sfn_failures(lookback_hours: int = 24) -> dict:
    """
    Returns failed AWS Step Functions executions in the last 24 hours.
    Shows state machine name, execution name, error type, and failure cause.
    Currently runs in mock mode — no real AWS calls are made.
    """
    if not is_mock():
        return _get_live_sfn_failures(lookback_hours)

    data = {**MOCK_SFN_FAILURES_DATA, "mode": "mock"}
    output = SfnFailuresOutput(**data)
    return output.model_dump()


def _get_live_sfn_failures(lookback_hours: int) -> dict:
    client = get_sfn_client()

    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

    state_machines = client.list_state_machines()["stateMachines"]

    failures = []
    for sm in state_machines:
        executions = client.list_executions(
            stateMachineArn=sm["stateMachineArn"],
            statusFilter="FAILED",
        )["executions"]

        for execution in executions:
            if execution["startDate"] < cutoff:
                continue

            detail = client.describe_execution(executionArn=execution["executionArn"])

            failures.append({
                "state_machine_name": sm["name"],
                "execution_name": execution["name"],
                "execution_arn": execution["executionArn"],
                "started_at": execution["startDate"].isoformat(),
                "failed_at": execution.get("stopDate", execution["startDate"]).isoformat(),
                "error": detail.get("error", "Unknown"),
                "cause": detail.get("cause", "No cause available."),
            })

    data = {
        "lookback_hours": lookback_hours,
        "failures": failures,
        "total_failures": len(failures),
        "mode": "live",
    }

    output = SfnFailuresOutput(**data)
    return output.model_dump()
