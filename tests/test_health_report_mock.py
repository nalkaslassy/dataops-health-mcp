import os

os.environ["DATAOPS_MODE"] = "mock"

from src.tools.health_report import generate_dataops_health_report


def test_health_report_returns_dict():
    result = generate_dataops_health_report()
    assert isinstance(result, dict)


def test_health_report_has_required_fields():
    result = generate_dataops_health_report()
    assert "generated_at" in result
    assert "cost_summary" in result
    assert "glue_failures" in result
    assert "sfn_failures" in result
    assert "untagged_buckets" in result
    assert "mode" in result


def test_health_report_mode_is_mock():
    result = generate_dataops_health_report()
    assert result["mode"] == "mock"


def test_health_report_generated_at_is_string():
    result = generate_dataops_health_report()
    assert isinstance(result["generated_at"], str)
    assert "T" in result["generated_at"]


def test_health_report_cost_summary_has_services():
    result = generate_dataops_health_report()
    assert "services" in result["cost_summary"]
    assert len(result["cost_summary"]["services"]) >= 1


def test_health_report_glue_failures_has_failures():
    result = generate_dataops_health_report()
    assert "failures" in result["glue_failures"]
    assert len(result["glue_failures"]["failures"]) >= 1


def test_health_report_sfn_failures_has_failures():
    result = generate_dataops_health_report()
    assert "failures" in result["sfn_failures"]
    assert len(result["sfn_failures"]["failures"]) >= 1


def test_health_report_untagged_buckets_has_buckets():
    result = generate_dataops_health_report()
    assert "buckets" in result["untagged_buckets"]
    assert len(result["untagged_buckets"]["buckets"]) >= 1


def test_health_report_subsections_mode_is_mock():
    result = generate_dataops_health_report()
    assert result["cost_summary"]["mode"] == "mock"
    assert result["glue_failures"]["mode"] == "mock"
    assert result["sfn_failures"]["mode"] == "mock"
    assert result["untagged_buckets"]["mode"] == "mock"
