"""
DataOps Health MCP Server
Entry point for the FastMCP server.

Run locally:
    python -m src.server

Connect from Claude Desktop by adding this server to your claude_desktop_config.json.
"""

from fastmcp import FastMCP
from src.tools.cost import get_cost_summary
from src.tools.glue import find_glue_failures
from src.tools.stepfunctions import find_sfn_failures
from src.tools.s3 import find_untagged_s3_buckets
from src.tools.health_report import generate_dataops_health_report

mcp = FastMCP(
    name="dataops-health-mcp",
    instructions=(
        "You are a DataOps health assistant. "
        "Use the available tools to summarize AWS costs, find pipeline failures, "
        "and identify infrastructure hygiene issues."
    ),
)

# --- Registered tools ---

@mcp.tool()
def get_cost_summary_tool() -> dict:
    """
    Returns an AWS cost summary for the current billing period.
    Shows top services by spend, cost vs. prior period, and notable increases.
    """
    return get_cost_summary()


@mcp.tool()
def find_glue_failures_tool() -> dict:
    """
    Returns failed AWS Glue job runs in the last 24 hours.
    Shows job name, run ID, error message, and how long the job ran before failing.
    """
    return find_glue_failures()


@mcp.tool()
def find_sfn_failures_tool() -> dict:
    """
    Returns failed AWS Step Functions executions in the last 24 hours.
    Shows state machine name, execution name, error type, and failure cause.
    """
    return find_sfn_failures()


@mcp.tool()
def find_untagged_s3_buckets_tool() -> dict:
    """
    Returns S3 buckets missing required tags (team, env, project).
    Shows bucket name, which tags are missing, and which tags exist.
    """
    return find_untagged_s3_buckets()


@mcp.tool()
def generate_dataops_health_report_tool() -> dict:
    """
    Generates a full DataOps health report combining cost summary, Glue failures,
    Step Functions failures, and untagged S3 buckets into a single summary.
    """
    return generate_dataops_health_report()


if __name__ == "__main__":
    mcp.run()
