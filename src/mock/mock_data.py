# Realistic-looking but clearly fake AWS cost data for mock/dev mode.
# Replace with real Cost Explorer API calls in aws/ when DATAOPS_MODE=live.

MOCK_COST_DATA = {
    "period": {
        "start": "2026-04-01",
        "end": "2026-04-30",
    },
    "services": [
        {
            "service": "AWS Glue",
            "current_cost": 312.47,
            "previous_cost": 241.83,
            "percent_change": 29.2,
        },
        {
            "service": "Amazon Athena",
            "current_cost": 87.15,
            "previous_cost": 91.40,
            "percent_change": -4.6,
        },
        {
            "service": "Amazon S3",
            "current_cost": 54.22,
            "previous_cost": 49.88,
            "percent_change": 8.7,
        },
        {
            "service": "AWS Step Functions",
            "current_cost": 18.64,
            "previous_cost": 17.90,
            "percent_change": 4.1,
        },
        {
            "service": "Amazon CloudWatch",
            "current_cost": 11.30,
            "previous_cost": 9.75,
            "percent_change": 15.9,
        },
        {
            "service": "Amazon EC2",
            "current_cost": 6.02,
            "previous_cost": 5.88,
            "percent_change": 2.4,
        },
    ],
    "total_current": 489.80,
    "total_previous": 416.64,
    "total_percent_change": 17.6,
    "notable_increases": [
        {
            "service": "AWS Glue",
            "reason": "Spike in DPU-hours — possible job retry loop or large backfill run.",
        },
        {
            "service": "Amazon CloudWatch",
            "reason": "Log ingestion increased ~16%. Check for new verbose log groups.",
        },
    ],
}

MOCK_GLUE_FAILURES_DATA = {
    "lookback_hours": 24,
    "failures": [
        {
            "job_name": "ingest_customer_events",
            "run_id": "jr_abc123",
            "started_at": "2026-05-19T02:15:00Z",
            "failed_at": "2026-05-19T02:47:00Z",
            "error_message": "An error occurred while calling o_279.AnalysisException: Path does not exist: s3://data-lake-prod/raw/customer_events/2026-05-19/",
            "duration_minutes": 32,
        },
        {
            "job_name": "transform_orders_daily",
            "run_id": "jr_def456",
            "started_at": "2026-05-19T03:00:00Z",
            "failed_at": "2026-05-19T03:12:00Z",
            "error_message": "ResourceNumberLimitExceededException: Maximum number of concurrent runs for job transform_orders_daily reached.",
            "duration_minutes": 12,
        },
        {
            "job_name": "load_product_catalog",
            "run_id": "jr_ghi789",
            "started_at": "2026-05-19T04:30:00Z",
            "failed_at": "2026-05-19T04:58:00Z",
            "error_message": "java.lang.OutOfMemoryError: GC overhead limit exceeded. Consider increasing the number of DPUs.",
            "duration_minutes": 28,
        },
    ],
    "total_failures": 3,
}

MOCK_SFN_FAILURES_DATA = {
    "lookback_hours": 24,
    "failures": [
        {
            "state_machine_name": "OrderProcessingPipeline",
            "execution_name": "exec_20260519_001",
            "execution_arn": "arn:aws:states:us-east-1:123456789012:execution:OrderProcessingPipeline:exec_20260519_001",
            "started_at": "2026-05-19T01:00:00Z",
            "failed_at": "2026-05-19T01:04:00Z",
            "error": "Lambda.ServiceException",
            "cause": "Lambda function timed out after 60 seconds in state ValidateOrder.",
        },
        {
            "state_machine_name": "CustomerSyncWorkflow",
            "execution_name": "exec_20260519_002",
            "execution_arn": "arn:aws:states:us-east-1:123456789012:execution:CustomerSyncWorkflow:exec_20260519_002",
            "started_at": "2026-05-19T05:30:00Z",
            "failed_at": "2026-05-19T05:31:00Z",
            "error": "States.TaskFailed",
            "cause": "DynamoDB ProvisionedThroughputExceededException in state WriteCustomerRecord.",
        },
    ],
    "total_failures": 2,
}

MOCK_UNTAGGED_S3_DATA = {
    "required_tags": ["team", "env", "project"],
    "buckets": [
        {
            "bucket_name": "data-lake-raw-uploads",
            "missing_tags": ["team", "project"],
            "existing_tags": {"env": "prod"},
        },
        {
            "bucket_name": "ml-model-artifacts-dev",
            "missing_tags": ["env"],
            "existing_tags": {"team": "ml", "project": "recommendations"},
        },
        {
            "bucket_name": "legacy-etl-scratch-2019",
            "missing_tags": ["team", "env", "project"],
            "existing_tags": {},
        },
    ],
    "total_untagged": 3,
}
