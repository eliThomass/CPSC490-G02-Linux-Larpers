# Prototype

Proof-of-concept code for Distributed Signal Capture for Multi-Node Analysis.

| Folder | Component |
|---|---|
| `backend/` | FastAPI backend |
| `database/` | PostgreSQL database |
| `dashboard/` | Angular dashboard |

## Database (PostgreSQL)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/). Open it once before running the commands below.

Create your `.env` from the example. Before the first start, replace `change-me` with your own password in both places it appears:

```bash
cd prototype
cp .env.example .env             # Windows: copy .env.example .env
```

Start the database:

```bash
cd prototype/database
docker compose up -d
```

Stop it with `docker compose down`. The data is kept; `docker compose down -v` deletes it.

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

With the database running, open <http://127.0.0.1:8000/health/db>. It should return `{"database":"ok"}`. The backend creates its tables on first connect.

To try the API, open <http://127.0.0.1:8000/docs>. `POST /observations` stores one observation; its `scanner_id` and `session_id` must already exist in the `scanners` and `scan_sessions` tables. `GET /observations` returns stored observations, optionally filtered by `start` and `end` (time zone required, e.g. `2026-11-09T12:00:00Z`) and `device_id`.

### Check that data survives a restart

With the database and backend running:

1. Connect the backend to the database once so it creates the tables. This should return `{"database":"ok"}`:

   ```bash
   curl http://127.0.0.1:8000/health/db
   ```

2. Add a scanner and a scan session:

   ```bash
   cd prototype/database
   docker compose exec db psql -U signal -d signal_capture -c "INSERT INTO scanners (scanner_id, name, hardware_model, firmware_version) VALUES ('11111111-1111-1111-1111-111111111111', 'node-1', 'ESP32', '0.1.0') ON CONFLICT DO NOTHING; INSERT INTO scan_sessions (session_id, name, started_at) VALUES ('22222222-2222-2222-2222-222222222222', 'restart-check', now()) ON CONFLICT DO NOTHING;"
   ```

3. Store an observation and note its `observation_id`:

   ```bash
   curl -X POST http://127.0.0.1:8000/observations -H "Content-Type: application/json" -d '{"scanner_id": "11111111-1111-1111-1111-111111111111", "session_id": "22222222-2222-2222-2222-222222222222", "captured_at": "2026-11-09T12:00:00Z", "protocol": "wifi"}'
   ```

4. Stop the backend with Ctrl+C and start it again.
5. Run `curl http://127.0.0.1:8000/observations`. The list should include the same `observation_id`.

On Windows, steps 3 and 5 can be done from <http://127.0.0.1:8000/docs> instead.

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

## Dashboard (Angular)

Requires [Node.js](https://nodejs.org/) 22.22.3+, 24.15.0+, or 26+ (24 LTS recommended) and the Angular CLI:

```bash
npm install -g @angular/cli
```

### Setup

```bash
cd prototype/dashboard
npm install
```

### Run

```bash
ng serve
```

Then open <http://localhost:4200>. It should show the Angular starter page.

### Build and test

```bash
ng build
ng test --watch=false
```
