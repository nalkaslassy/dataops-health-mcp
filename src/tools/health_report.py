from datetime import datetime, timezone

from src.aws.clients import is_mock
from src.schemas.outputs import HealthReportOutput
from src.tools.cost import get_cost_summary
from src.tools.glue import find_glue_failures
from src.tools.stepfunctions import find_sfn_failures
from src.tools.s3 import find_untagged_s3_buckets


def generate_dataops_health_report() -> dict:
    """
    Calls all four health tools and returns a combined report.

    Mock mode: delegates to each tool in mock mode and bundles results.
    Live mode: TODO — same composition, but each tool hits real AWS APIs.
    """
    if not is_mock():
        raise NotImplementedError("Live AWS mode is not implemented yet. Set DATAOPS_MODE=mock.")

    output = HealthReportOutput(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        cost_summary=get_cost_summary(),
        glue_failures=find_glue_failures(),
        sfn_failures=find_sfn_failures(),
        untagged_buckets=find_untagged_s3_buckets(),
        mode="mock",
    )
    return output.model_dump()
