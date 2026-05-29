from src.aws.clients import is_mock
from src.mock.mock_data import MOCK_UNTAGGED_S3_DATA
from src.schemas.outputs import UntaggedS3Output


def find_untagged_s3_buckets() -> dict:
    """
    Returns S3 buckets that are missing required tags (team, env, project).

    Mock mode: returns static untagged bucket examples from mock/mock_data.py.
    Live mode: TODO — call s3_client.list_buckets() then get_bucket_tagging() per bucket.
    """
    if not is_mock():
        # TODO (Phase 1 live mode): call S3 API here.
        # client = get_s3_client()
        # buckets = client.list_buckets()["Buckets"]
        # return _find_untagged(client, buckets, REQUIRED_TAGS)
        raise NotImplementedError("Live AWS mode is not implemented yet. Set DATAOPS_MODE=mock.")

    data = {**MOCK_UNTAGGED_S3_DATA, "mode": "mock"}
    output = UntaggedS3Output(**data)
    return output.model_dump()
