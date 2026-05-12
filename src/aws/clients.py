import os

# Reads DATAOPS_MODE from the environment.
# "mock" (default) — no AWS calls are made; tools return mock data.
# "live" — real boto3 clients are created using AWS_PROFILE / AWS_REGION.
#
# TODO (Phase 1 live mode): instantiate boto3 clients here:
#   import boto3
#   def get_cost_explorer_client():
#       return boto3.client("ce", region_name=get_region())
#   def get_glue_client():
#       return boto3.client("glue", region_name=get_region())
#   def get_sfn_client():
#       return boto3.client("stepfunctions", region_name=get_region())
#   def get_s3_client():
#       return boto3.client("s3", region_name=get_region())


def get_mode() -> str:
    return os.getenv("DATAOPS_MODE", "mock").lower()


def get_region() -> str:
    return os.getenv("AWS_REGION", "us-east-1")


def is_mock() -> bool:
    return get_mode() == "mock"
