import os
import pytest

os.environ["DATAOPS_MODE"] = "mock"

from src.tools.glue import find_glue_failures


def test_glue_failures_returns_dict():
    result = find_glue_failures()
    assert isinstance(result, dict)


def test_glue_failures_has_required_fields():
    result = find_glue_failures()
    assert "lookback_hours" in result
    assert "failures" in result
    assert "total_failures" in result
    assert "mode" in result


def test_glue_failures_has_at_least_one_failure():
    result = find_glue_failures()
    assert len(result["failures"]) >= 1


def test_glue_failures_mode_is_mock():
    result = find_glue_failures()
    assert result["mode"] == "mock"


def test_glue_failure_fields():
    result = find_glue_failures()
    failure = result["failures"][0]
    assert "job_name" in failure
    assert "run_id" in failure
    assert "started_at" in failure
    assert "failed_at" in failure
    assert "error_message" in failure
    assert "duration_minutes" in failure


def test_glue_total_failures_matches_list():
    result = find_glue_failures()
    assert result["total_failures"] == len(result["failures"])
