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
