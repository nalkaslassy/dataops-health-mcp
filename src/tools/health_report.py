from datetime import datetime, timezone

from src.aws.clients import is_mock
from src.schemas.outputs import HealthReportOutput
from src.tools.cost import get_cost_summary
from src.tools.glue import find_glue_failures
from src.tools.stepfunctions import find_sfn_failures
from src.tools.s3 import find_untagged_s3_buckets


def generate_dataops_health_report() -> dict:
    """
    Generates a full DataOps health report combining AWS cost summary,
    Glue job failures, Step Functions failures, and untagged S3 buckets.
    """
    output = HealthReportOutput(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        cost_summary=get_cost_summary(),
        glue_failures=find_glue_failures(),
        sfn_failures=find_sfn_failures(),
        untagged_buckets=find_untagged_s3_buckets(),
        mode="mock" if is_mock() else "live",
    )
    return output.model_dump()
