# dataops-health-mcp

Local-first MCP server for DataOps health monitoring on AWS.

Ask Claude questions like:
- *"What are my top AWS costs this month?"*
- *"Which Glue jobs failed in the last 24 hours?"*
- *"Generate a full DataOps health report."*

---

## Current Status: Phase 1 — Template + one mock tool

> **Warning:** Real AWS mode is NOT implemented yet. Everything runs on mock data.

| Tool | Status |
|---|---|
| `get_cost_summary` | Mock working |
| `find_glue_failures` | Not yet implemented |
| `find_sfn_failures` | Not yet implemented |
| `find_untagged_s3_buckets` | Not yet implemented |
| `generate_dataops_health_report` | Not yet implemented |

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

## Run in Mock Mode

```bash
python -m src.server
```

No AWS credentials needed — mock mode uses example data only.

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
      "cwd": "/absolute/path/to/dataops-health-mcp",
      "env": { "DATAOPS_MODE": "mock" }
    }
  }
}
```

Then try: *"Give me a cost summary for this billing period."*

---

## Project Structure

```
src/
  server.py               # MCP entry point — tool registration lives here
  tools/
    cost.py               # get_cost_summary (mock done, live TODO)
    glue.py               # find_glue_failures (TODO)
    stepfunctions.py      # find_sfn_failures (TODO)
    s3.py                 # find_untagged_s3_buckets (TODO)
    health_report.py      # generate_dataops_health_report (TODO, last)
  mock/
    mock_data.py          # Realistic fake AWS data for development
  schemas/
    outputs.py            # Pydantic models for tool return values
  aws/
    clients.py            # boto3 client factory stub (live mode TODO)
tests/
  test_cost_mock.py       # pytest tests for get_cost_summary
examples/
  sample_prompts.md       # Example prompts to try in Claude Desktop
```

---

## Coming Next

1. `find_glue_failures` — Glue job run history
2. `find_sfn_failures` — Step Functions execution history
3. `find_untagged_s3_buckets` — S3 tag audit
4. `generate_dataops_health_report` — combined report from all tools
5. Live AWS mode — real boto3 calls behind `DATAOPS_MODE=live`
