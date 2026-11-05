# Prototype

Proof-of-concept code for Distributed Signal Capture for Multi-Node Analysis.

| Folder | Component |
|---|---|
| `backend/` | FastAPI backend |

## Backend (FastAPI)

Requires Python 3.12 or newer.

### Setup

With uv:

```bash
cd prototype/backend
uv sync
```

With pip:

```bash
cd prototype/backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
uv run fastapi dev main.py       # uv
fastapi dev main.py              # pip (with .venv active)
```

Then open <http://127.0.0.1:8000/health>. It should return `{"status":"ok"}`.

### Test

```bash
uv run pytest                    # uv
pip install pytest && pytest     # pip (with .venv active)
```

### Add a dependency

Use uv, then regenerate `requirements.txt` so pip users get it too:

```bash
uv add <package>
uv export --format requirements-txt --no-hashes --no-dev --no-emit-project -o requirements.txt
```
