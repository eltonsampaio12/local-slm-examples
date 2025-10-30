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

## Run the Flask API server

```bash
python flask_server.py
```

Send a request:
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

## Optional: Use LocalLLM directly (Python)
```python
from local_llm import LocalLLM

llm = LocalLLM()
prompt = "Your prompt here"
text = llm.generate(prompt)
print(text)
```

# local-llm-examples
