from src.aws.clients import is_mock, get_s3_client
from src.mock.mock_data import MOCK_UNTAGGED_S3_DATA
from src.schemas.outputs import UntaggedS3Output

REQUIRED_TAGS = ["team", "env", "project"]


def find_untagged_s3_buckets() -> dict:
    """
    Returns S3 buckets missing required tags (team, env, project).
    Shows bucket name, which tags are missing, and which tags exist.
    """
    if not is_mock():
        return _get_live_untagged_buckets()

    data = {**MOCK_UNTAGGED_S3_DATA, "mode": "mock"}
    output = UntaggedS3Output(**data)
    return output.model_dump()


def _get_live_untagged_buckets() -> dict:
    client = get_s3_client()

    buckets = client.list_buckets()["Buckets"]

    untagged = []
    for bucket in buckets:
        name = bucket["Name"]

        try:
            response = client.get_bucket_tagging(Bucket=name)
            existing_tags = {t["Key"]: t["Value"] for t in response["TagSet"]}
        except client.exceptions.from_code("NoSuchTagSet"):
            existing_tags = {}

        missing_tags = [tag for tag in REQUIRED_TAGS if tag not in existing_tags]

        if missing_tags:
            untagged.append({
                "bucket_name": name,
                "missing_tags": missing_tags,
                "existing_tags": existing_tags,
            })

    data = {
        "required_tags": REQUIRED_TAGS,
        "buckets": untagged,
        "total_untagged": len(untagged),
        "mode": "live",
    }

    output = UntaggedS3Output(**data)
    return output.model_dump()
