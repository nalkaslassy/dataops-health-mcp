# TODO (Phase 1): implement find_sfn_failures
# Returns failed Step Functions executions within a lookback window.
# Mock mode: return static failure examples.
# Live mode: call sfn_client.list_executions(statusFilter="FAILED") per state machine.


def find_sfn_failures() -> dict:
    raise NotImplementedError("find_sfn_failures is not implemented yet.")
