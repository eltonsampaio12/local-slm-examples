## Setup

### 1) Create and activate a virtual environment

macOS/Linux (zsh/bash):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

To deactivate later:
```bash
deactivate
```

### 2) Install project requirements
```bash
pip install -r requirements.txt
```

### 3) (Optional) Set Latimer API key for cloud service
If you want to use the Latimer API endpoint, you can set the environment variable in two ways:

**Option 1: Using a `.env` file (recommended)**
Create a `.env` file in the project root:
```bash
LATIMER_API_KEY=your-api-key-here
```

**Option 2: Set environment variable directly**

macOS/Linux:
```bash
export LATIMER_API_KEY="your-api-key-here"
```

Windows (PowerShell):
```powershell
$env:LATIMER_API_KEY="your-api-key-here"
```

## Run the Flask API server

```bash
python flask_server.py
```

## API Endpoints

### Local LLM: `/generate`

Send a request to the local LLM:
```bash
curl -X POST http://localhost:8000/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Say hello in one sentence."}'
```

Send a request with a system prompt:
```bash
curl -X POST http://localhost:8000/generate \
  -H 'Content-Type: application/json' \
  -d '{
        "system": "You are a concise assistant. Reply with one word.",
        "prompt": "Provide a positive greeting"
      }'
```

### Latimer API: `/generate/latimer`

Send a request to the Latimer API:
```bash
curl -X POST http://localhost:8000/generate/latimer \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Say hello in one sentence."}'
```

Send a request with a system prompt:
```bash
curl -X POST http://localhost:8000/generate/latimer \
  -H 'Content-Type: application/json' \
  -d '{
        "system": "You are a concise assistant. Reply with one word.",
        "prompt": "Provide a positive greeting"
      }'
```

### Swagger (OpenAPI) docs

After starting the server, open:

`http://localhost:8000/apidocs`

There you can explore and try both `/generate` and `/generate/latimer` endpoints interactively.

## Optional: Use LocalLLM directly (Python)
```python
from local_llm import LocalLLM

llm = LocalLLM()
prompt = "Your prompt here"
text = llm.generate(prompt)
print(text)
```

# local-llm-examples
