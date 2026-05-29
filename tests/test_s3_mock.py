import os
import pytest

os.environ["DATAOPS_MODE"] = "mock"

from src.tools.s3 import find_untagged_s3_buckets


def test_s3_untagged_returns_dict():
    result = find_untagged_s3_buckets()
    assert isinstance(result, dict)


def test_s3_untagged_has_required_fields():
    result = find_untagged_s3_buckets()
    assert "required_tags" in result
    assert "buckets" in result
    assert "total_untagged" in result
    assert "mode" in result


def test_s3_untagged_has_at_least_one_bucket():
    result = find_untagged_s3_buckets()
    assert len(result["buckets"]) >= 1


def test_s3_untagged_mode_is_mock():
    result = find_untagged_s3_buckets()
    assert result["mode"] == "mock"


def test_s3_bucket_fields():
    result = find_untagged_s3_buckets()
    bucket = result["buckets"][0]
    assert "bucket_name" in bucket
    assert "missing_tags" in bucket
    assert "existing_tags" in bucket


def test_s3_total_untagged_matches_list():
    result = find_untagged_s3_buckets()
    assert result["total_untagged"] == len(result["buckets"])


def test_s3_missing_tags_is_list():
    result = find_untagged_s3_buckets()
    for bucket in result["buckets"]:
        assert isinstance(bucket["missing_tags"], list)
        assert len(bucket["missing_tags"]) >= 1
