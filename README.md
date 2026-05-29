# dataops-health-mcp

Local-first MCP server for DataOps health monitoring on AWS.

Ask Claude questions like:
- *"What are my top AWS costs this month?"*
- *"Which Glue jobs failed in the last 24 hours?"*
- *"Generate a full DataOps health report."*

---

## Current Status: Phase 1 complete — all 5 tools mocked

> **Note:** Real AWS mode is not yet implemented. All tools run on mock data. Live mode coming in Phase 2.

| Tool | Mock | Live AWS |
|---|---|---|
| `get_cost_summary` | Done | TODO |
| `find_glue_failures` | Done | TODO |
| `find_sfn_failures` | Done | TODO |
| `find_untagged_s3_buckets` | Done | TODO |
| `generate_dataops_health_report` | Done | TODO |

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

## Coming Next (Phase 2 — Live AWS mode)

1. `get_cost_summary` — real Cost Explorer API calls
2. `find_glue_failures` — real Glue job run history
3. `find_sfn_failures` — real Step Functions execution history
4. `find_untagged_s3_buckets` — real S3 tag audit
5. `generate_dataops_health_report` — automatically live once all tools above are done
