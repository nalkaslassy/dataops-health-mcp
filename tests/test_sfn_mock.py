import os
import pytest

os.environ["DATAOPS_MODE"] = "mock"

from src.tools.stepfunctions import find_sfn_failures


def test_sfn_failures_returns_dict():
    result = find_sfn_failures()
    assert isinstance(result, dict)


def test_sfn_failures_has_required_fields():
    result = find_sfn_failures()
    assert "lookback_hours" in result
    assert "failures" in result
    assert "total_failures" in result
    assert "mode" in result


def test_sfn_failures_has_at_least_one_failure():
    result = find_sfn_failures()
    assert len(result["failures"]) >= 1


def test_sfn_failures_mode_is_mock():
    result = find_sfn_failures()
    assert result["mode"] == "mock"


def test_sfn_failure_fields():
    result = find_sfn_failures()
    failure = result["failures"][0]
    assert "state_machine_name" in failure
    assert "execution_name" in failure
    assert "execution_arn" in failure
    assert "started_at" in failure
    assert "failed_at" in failure
    assert "error" in failure
    assert "cause" in failure


def test_sfn_total_failures_matches_list():
    result = find_sfn_failures()
    assert result["total_failures"] == len(result["failures"])
