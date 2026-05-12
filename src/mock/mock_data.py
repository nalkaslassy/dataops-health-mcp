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
