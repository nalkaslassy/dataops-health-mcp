# dataops-health-mcp

Local MCP server that connects Claude to your AWS account for DataOps health monitoring.

Ask Claude questions like:
- *"What are my top AWS costs this month?"*
- *"Which Glue jobs failed in the last 24 hours?"*
- *"Are any of my S3 buckets missing tags?"*
- *"Give me a full DataOps health report."*

---

## Current Status: Phase 2 complete — all 5 tools live

| Tool | Mock | Live AWS |
|---|---|---|
| `get_cost_summary` | Done | Done |
| `find_glue_failures` | Done | Done |
| `find_sfn_failures` | Done | Done |
| `find_untagged_s3_buckets` | Done | Done |
| `generate_dataops_health_report` | Done | Done |

---

## How it works

This is an MCP server — a plugin for Claude Desktop. Instead of copying and pasting AWS data into Claude, Claude calls this server directly and gets the data itself.

Set `DATAOPS_MODE=mock` to use fake data (no AWS credentials needed).  
Set `DATAOPS_MODE=live` to use your real AWS account.

---

## Install

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux
```

---

## Run Tests

```bash
pytest tests/ -v
```

---

## Connect to Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dataops-health-mcp": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:/Users/your-username/path/to/dataops-health-mcp",
      "env": { "DATAOPS_MODE": "live" }
    }
  }
}
```

---

## AWS Permissions Required

Your AWS user needs the following policies:

| Policy | Used by |
|---|---|
| `AWSBillingReadOnlyAccess` | `get_cost_summary` |
| `AWSGlueConsoleFullAccess` | `find_glue_failures` |
| `AWSStepFunctionsReadOnlyAccess` | `find_sfn_failures` |
| `AmazonS3ReadOnlyAccess` | `find_untagged_s3_buckets` |

---

## Project Structure

```
src/
  server.py               # MCP entry point — tool registration
  tools/
    cost.py               # get_cost_summary
    glue.py               # find_glue_failures
    stepfunctions.py      # find_sfn_failures
    s3.py                 # find_untagged_s3_buckets
    health_report.py      # generate_dataops_health_report (calls all 4 above)
  mock/
    mock_data.py          # Fake AWS data for mock mode
  schemas/
    outputs.py            # Pydantic models for tool return values
  aws/
    clients.py            # boto3 client factory + mock/live mode switch
tests/
  test_cost_mock.py
  test_glue_mock.py
  test_sfn_mock.py
  test_s3_mock.py
  test_health_report_mock.py
examples/
  sample_prompts.md
```

---

## Coming Next (Phase 3)

- Connect to Claude Desktop and test end-to-end
- Add tagging support — tag S3 buckets directly from Claude
- Slack/email alerting for critical failures
