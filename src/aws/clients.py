import os
import boto3


def get_mode() -> str:
    return os.getenv("DATAOPS_MODE", "mock").lower()


def get_region() -> str:
    return os.getenv("AWS_REGION", "us-east-1")


def is_mock() -> bool:
    return get_mode() == "mock"


def get_cost_explorer_client():
    return boto3.client("ce", region_name="us-east-1")


def get_glue_client():
    return boto3.client("glue", region_name="us-east-1")


def get_sfn_client():
    return boto3.client("stepfunctions", region_name="us-east-1")


def get_s3_client():
    return boto3.client("s3", region_name="us-east-1")
