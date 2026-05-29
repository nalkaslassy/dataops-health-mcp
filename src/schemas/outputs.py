from pydantic import BaseModel
from typing import Optional


class ServiceCost(BaseModel):
    service: str
    current_cost: float
    previous_cost: float
    percent_change: float


class NotableIncrease(BaseModel):
    service: str
    reason: str


class CostPeriod(BaseModel):
    start: str
    end: str


class CostSummaryOutput(BaseModel):
    period: CostPeriod
    services: list[ServiceCost]
    total_current: float
    total_previous: float
    total_percent_change: float
    notable_increases: list[NotableIncrease]
    mode: str  # "mock" or "live"


class GlueFailure(BaseModel):
    job_name: str
    run_id: str
    started_at: str
    failed_at: str
    error_message: str
    duration_minutes: int


class GlueFailuresOutput(BaseModel):
    lookback_hours: int
    failures: list[GlueFailure]
    total_failures: int
    mode: str  # "mock" or "live"


class SfnFailure(BaseModel):
    state_machine_name: str
    execution_name: str
    execution_arn: str
    started_at: str
    failed_at: str
    error: str
    cause: str


class SfnFailuresOutput(BaseModel):
    lookback_hours: int
    failures: list[SfnFailure]
    total_failures: int
    mode: str  # "mock" or "live"


class UntaggedBucket(BaseModel):
    bucket_name: str
    missing_tags: list[str]
    existing_tags: dict


class UntaggedS3Output(BaseModel):
    required_tags: list[str]
    buckets: list[UntaggedBucket]
    total_untagged: int
    mode: str  # "mock" or "live"


class HealthReportOutput(BaseModel):
    generated_at: str
    cost_summary: CostSummaryOutput
    glue_failures: GlueFailuresOutput
    sfn_failures: SfnFailuresOutput
    untagged_buckets: UntaggedS3Output
    mode: str  # "mock" or "live"
