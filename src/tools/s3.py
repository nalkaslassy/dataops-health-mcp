# TODO (Phase 1): implement find_untagged_s3_buckets
# Returns S3 buckets that are missing required tags (e.g., "team", "env", "project").
# Mock mode: return a static list of example untagged buckets.
# Live mode: call s3_client.list_buckets() then s3_client.get_bucket_tagging() per bucket.


def find_untagged_s3_buckets() -> dict:
    raise NotImplementedError("find_untagged_s3_buckets is not implemented yet.")
