import os
import pytest

# Ensure mock mode is active before importing the tool
os.environ["DATAOPS_MODE"] = "mock"

from src.tools.cost import get_cost_summary


def test_cost_summary_returns_dict():
    result = get_cost_summary()
    assert isinstance(result, dict)


def test_cost_summary_has_required_fields():
    result = get_cost_summary()
    assert "period" in result
    assert "services" in result
    assert "total_current" in result
    assert "total_previous" in result
    assert "total_percent_change" in result
    assert "notable_increases" in result
    assert "mode" in result


def test_cost_summary_has_at_least_one_service():
    result = get_cost_summary()
    assert len(result["services"]) >= 1


def test_cost_summary_mode_is_mock():
    result = get_cost_summary()
    assert result["mode"] == "mock"


def test_cost_summary_service_fields():
    result = get_cost_summary()
    service = result["services"][0]
    assert "service" in service
    assert "current_cost" in service
    assert "previous_cost" in service
    assert "percent_change" in service


def test_cost_summary_totals_are_positive():
    result = get_cost_summary()
    assert result["total_current"] > 0
    assert result["total_previous"] > 0
