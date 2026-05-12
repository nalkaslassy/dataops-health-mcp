"""
DataOps Health MCP Server — Phase 1
Entry point for the FastMCP server.

Run locally:
    python -m src.server

Connect from Claude Desktop by adding this server to your claude_desktop_config.json.
"""

from fastmcp import FastMCP
from src.tools.cost import get_cost_summary

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
    Currently runs in mock mode — no real AWS calls are made.
    """
    return get_cost_summary()


# TODO: register find_glue_failures when tools/glue.py is implemented
# @mcp.tool()
# def find_glue_failures_tool() -> dict:
#     from src.tools.glue import find_glue_failures
#     return find_glue_failures()

# TODO: register find_sfn_failures when tools/stepfunctions.py is implemented
# @mcp.tool()
# def find_sfn_failures_tool() -> dict:
#     from src.tools.stepfunctions import find_sfn_failures
#     return find_sfn_failures()

# TODO: register find_untagged_s3_buckets when tools/s3.py is implemented
# @mcp.tool()
# def find_untagged_s3_buckets_tool() -> dict:
#     from src.tools.s3 import find_untagged_s3_buckets
#     return find_untagged_s3_buckets()

# TODO: register generate_dataops_health_report last (depends on all tools above)
# @mcp.tool()
# def generate_dataops_health_report_tool() -> dict:
#     from src.tools.health_report import generate_dataops_health_report
#     return generate_dataops_health_report()


if __name__ == "__main__":
    mcp.run()
