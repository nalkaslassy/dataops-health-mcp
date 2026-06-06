from datetime import date, timedelta

from src.aws.clients import is_mock, get_cost_explorer_client
from src.mock.mock_data import MOCK_COST_DATA
from src.schemas.outputs import CostSummaryOutput


def get_cost_summary() -> dict:
    """
    Returns a cost summary for the current billing period.

    Mock mode: returns static example data from mock/mock_data.py.
    Live mode: calls AWS Cost Explorer and returns real spend by service.
    """
    if not is_mock():
        return _get_live_cost_summary()

    data = {**MOCK_COST_DATA, "mode": "mock"}
    output = CostSummaryOutput(**data)
    return output.model_dump()


def _get_live_cost_summary() -> dict:
    client = get_cost_explorer_client()

    today = date.today()
    first_of_month = today.replace(day=1)
    last_month_start = (first_of_month - timedelta(days=1)).replace(day=1)
    last_month_end = first_of_month

    current = client.get_cost_and_usage(
        TimePeriod={"Start": str(first_of_month), "End": str(today)},
        Granularity="MONTHLY",
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        Metrics=["UnblendedCost"],
    )

    previous = client.get_cost_and_usage(
        TimePeriod={"Start": str(last_month_start), "End": str(last_month_end)},
        Granularity="MONTHLY",
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        Metrics=["UnblendedCost"],
    )

    current_by_service = _extract_costs(current)
    previous_by_service = _extract_costs(previous)

    services = []
    for service, current_cost in current_by_service.items():
        if current_cost < 0.01:
            continue
        previous_cost = previous_by_service.get(service, 0)
        if previous_cost > 0:
            percent_change = round((current_cost - previous_cost) / previous_cost * 100, 1)
        else:
            percent_change = 0.0
        services.append({
            "service": service,
            "current_cost": round(current_cost, 2),
            "previous_cost": round(previous_cost, 2),
            "percent_change": percent_change,
        })

    services.sort(key=lambda x: x["current_cost"], reverse=True)

    total_current = round(sum(s["current_cost"] for s in services), 2)
    total_previous = round(sum(s["previous_cost"] for s in services), 2)
    if total_previous > 0:
        total_percent_change = round((total_current - total_previous) / total_previous * 100, 1)
    else:
        total_percent_change = 0.0

    notable_increases = [
        {"service": s["service"], "reason": f"Up {s['percent_change']}% vs last month."}
        for s in services
        if s["percent_change"] >= 20
    ]

    data = {
        "period": {"start": str(first_of_month), "end": str(today)},
        "services": services,
        "total_current": total_current,
        "total_previous": total_previous,
        "total_percent_change": total_percent_change,
        "notable_increases": notable_increases,
        "mode": "live",
    }

    output = CostSummaryOutput(**data)
    return output.model_dump()


def _extract_costs(response: dict) -> dict:
    costs = {}
    for group in response["ResultsByTime"][0]["Groups"]:
        service = group["Keys"][0]
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        costs[service] = amount
    return costs
