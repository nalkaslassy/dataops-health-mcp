from src.aws.clients import is_mock
from src.mock.mock_data import MOCK_COST_DATA
from src.schemas.outputs import CostSummaryOutput


def get_cost_summary() -> dict:
    """
    Returns a cost summary for the current billing period.

    Mock mode: returns static example data from mock/mock_data.py.
    Live mode: TODO — call AWS Cost Explorer API via aws/clients.py.
    """
    if not is_mock():
        # TODO (Phase 1 live mode): call Cost Explorer here.
        # client = get_cost_explorer_client()
        # raw = client.get_cost_and_usage(...)
        # return _parse_cost_explorer_response(raw)
        raise NotImplementedError("Live AWS mode is not implemented yet. Set DATAOPS_MODE=mock.")

    data = {**MOCK_COST_DATA, "mode": "mock"}
    output = CostSummaryOutput(**data)
    return output.model_dump()
