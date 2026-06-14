# dataops-health-mcp

Local MCP server that connects Claude to your AWS account for DataOps health monitoring.

Ask Claude questions like:
- *"What are my top AWS costs this month?"*
- *"Which Glue jobs failed in the last 24 hours?"*
- *"Are any of my S3 buckets missing tags?"*
- *"Give me a full DataOps health report."*

---

## Tools

| Tool | What it does |
|---|---|
| `get_cost_summary` | AWS spend by service vs. last month |
| `find_glue_failures` | Failed Glue job runs in the last 24 hours |
| `find_sfn_failures` | Failed Step Functions executions in the last 24 hours |
| `find_untagged_s3_buckets` | S3 buckets missing required tags (team, env, project) |
| `generate_dataops_health_report` | All four tools combined into one summary |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/nalkaslassy/dataops-health-mcp.git
cd dataops-health-mcp
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure your environment

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and set:

```
DATAOPS_MODE=live     # use "mock" for fake data, "live" for real AWS
AWS_REGION=us-east-1  # change to your AWS region if different
```

---

## AWS Credentials Setup

### Step 1 — Install the AWS CLI

Download from: https://aws.amazon.com/cli/

Verify it's installed:
```bash
aws --version
```

### Step 2 — Configure your credentials

```bash
aws configure
```

You'll be prompted for:
```
AWS Access Key ID:     <your access key>
AWS Secret Access Key: <your secret key>
Default region name:   us-east-1
Default output format: json
```

To get your access key, go to the AWS Console → IAM → Users → your user → Security credentials → Create access key.

### Step 3 — Verify it's working

```bash
aws sts get-caller-identity
```

You should see your account ID and user name. If you get an error, your credentials are not set up correctly.

### Step 4 — Attach required IAM policies

Your AWS user needs the following policies. Go to AWS Console → IAM → Users → your user → Add permissions → Attach policies directly:

| Policy | Required for |
|---|---|
| `AWSBillingReadOnlyAccess` | `get_cost_summary` |
| `AWSGlueConsoleFullAccess` | `find_glue_failures` |
| `AWSStepFunctionsReadOnlyAccess` | `find_sfn_failures` |
| `AmazonS3ReadOnlyAccess` | `find_untagged_s3_buckets` |

Or attach them via CLI (replace `your-username` with your IAM username):

```bash
aws iam attach-user-policy --user-name your-username --policy-arn arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess
aws iam attach-user-policy --user-name your-username --policy-arn arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess
aws iam attach-user-policy --user-name your-username --policy-arn arn:aws:iam::aws:policy/AWSStepFunctionsReadOnlyAccess
aws iam attach-user-policy --user-name your-username --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

---

## Connect to Claude Desktop

### Step 1 — Find your Claude Desktop config file

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

### Step 2 — Add the MCP server

Open the config file and add this (replace the path with where you cloned the repo):

```json
{
  "mcpServers": {
    "dataops-health-mcp": {
      "command": "C:/path/to/dataops-health-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "src.server"],
      "cwd": "C:/path/to/dataops-health-mcp",
      "env": {
        "DATAOPS_MODE": "live",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

For macOS/Linux:
```json
{
  "mcpServers": {
    "dataops-health-mcp": {
      "command": "/path/to/dataops-health-mcp/.venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/dataops-health-mcp",
      "env": {
        "DATAOPS_MODE": "live",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

### Step 3 — Restart Claude Desktop

Fully quit and reopen Claude Desktop. The tools will appear automatically.

### Step 4 — Test it

Try asking Claude:
- *"What are my AWS costs this month?"*
- *"Give me a full DataOps health report."*

---

## Run Tests

```bash
pytest tests/ -v
```

All 34 tests should pass. Tests run in mock mode and do not require AWS credentials.

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
```
