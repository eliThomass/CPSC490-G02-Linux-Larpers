# Prototype

Proof-of-concept code for Distributed Signal Capture for Multi-Node Analysis.

| Folder | Component |
|---|---|
| `backend/` | FastAPI backend |
| `database/` | PostgreSQL database |
| `dashboard/` | Angular dashboard |
| `esp32/` | ESP32 capture-node firmware |

## Database (PostgreSQL)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/). Open it once before running the commands below.

Create your `.env` from the example:

```bash
cp prototype/.env.example prototype/.env
```

On Windows PowerShell:

```powershell
Copy-Item prototype/.env.example prototype/.env
```

Edit `prototype/.env` and replace `change-me` in both `POSTGRES_PASSWORD` and
`DATABASE_URL` with the same password. Keep this file local; do not commit it.

Start the database:

```bash
docker compose -f prototype/database/compose.yaml up -d db
```

PostgreSQL is available on `localhost:5433`. To stop it while keeping its data:

```bash
docker compose -f prototype/database/compose.yaml down
```

Adding `-v` to this command also deletes the database volume and its data.

The Compose project keeps the original name `database`, so the existing
`database_pgdata` volume is reused with this single Compose file.

## Backend (FastAPI)

Requires Python 3.12 or newer.

To run the backend's database endpoints, complete the database setup above first.
To run only the tests with Docker, skip to [Test](#test).

### Setup

With uv:

```bash
cd prototype/backend
uv sync
```

With pip:

```bash
cd prototype/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, use these commands instead:

```powershell
cd prototype/backend
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Run

From `prototype/backend`, use the command matching your setup:

```bash
uv run fastapi dev main.py       # With uv
fastapi dev main.py              # With pip and .venv active
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


| File | Coverage | Cases |
|---|---|---|
| `backend/test_main.py` | Root and health endpoints | 2 |
| `backend/test_observations.py` | Observation API storage, validation, and filtering | 9 |
| `backend/test_observation_model.py` | Complete and partial Wi-Fi/Bluetooth records, and missing required fields | 8 |

All tests use in-memory SQLite where a database is needed. They do not require
`.env`, a running API server, or PostgreSQL, and they do not modify your saved
PostgreSQL data.

#### Option 1: Docker (no local Python setup)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/),
   open it, and wait for Docker to finish starting.
2. Open a terminal in the repository root. If your terminal is currently in
   `prototype/backend`, run `cd ../..` first.
3. Confirm Docker is running and Compose is installed:

   ```bash
   docker info
   docker compose version
   ```

4. Build the test image and run all backend tests:

   ```bash
   docker compose -f prototype/database/compose.yaml run --build --rm tests
   ```

5. Check the result. A successful run ends with `19 passed`. A failing test
   produces a failure summary and a nonzero exit code.

The first run downloads Python 3.12 and installs dependencies, so it takes
longer. Repeat step 4 whenever you change the code. `--build` includes the latest
files and reuses cached build steps where possible; `--rm` removes the test
container afterward.

To run only the 8 Observation model cases with individual results:

```bash
docker compose -f prototype/database/compose.yaml run --build --rm tests python -m pytest test_observation_model.py -v
```

Both services use `prototype/database/compose.yaml`. The test image is built from
`prototype/backend/Dockerfile.test`. The test service has a profile so starting
the database does not also run tests; running `tests` explicitly enables it.
The `.env` file is optional for Compose to load the test service, but you must
create it as described above before starting PostgreSQL.

#### Option 2: Local Python with uv

1. Install Python 3.12 or newer and uv.
2. From the repository root, enter the backend folder and install dependencies:

   ```bash
   cd prototype/backend
   uv sync
   ```

3. Run all tests:

   ```bash
   uv run pytest -q
   ```

4. To run only the Observation model cases:

   ```bash
   uv run pytest test_observation_model.py -v
   ```

#### Option 3: Local Python with pip

1. Complete the pip setup above, including activating `.venv`.
2. From `prototype/backend`, install pytest:

   ```bash
   python -m pip install pytest
   ```

3. Run all tests:

   ```bash
   python -m pytest -q
   ```

4. To run only the Observation model cases:

   ```bash
   python -m pytest test_observation_model.py -v
   ```

#### CI

The existing **Prototype build & tests** job automatically discovers all three
test files and runs them with pytest on Python 3.12. CI installs Python
dependencies directly; Docker is an additional way to run the suite locally.

### Add a dependency

From `prototype/backend`, use uv, then regenerate `requirements.txt` so pip and
Docker users get the updated dependencies too. Replace `<package>` with the
package name:

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

## ESP32 firmware (PlatformIO)

Requires [PlatformIO Core](https://docs.platformio.org/en/latest/core/installation/index.html):

```bash
brew install platformio              # macOS
python3 -m pip install platformio    # any OS
```

`platformio.ini` targets the generic `esp32dev` board. Change `board` once the team confirms which ESP32 was ordered.

### Build

```bash
cd prototype/esp32
pio run
```

The first build downloads the ESP32 toolchain. It should end with `SUCCESS`.

### Flash and monitor

Needs an ESP32 board connected over USB (waiting for the hardware order, #79):

```bash
cd prototype/esp32
pio run --target upload
pio device monitor -b 115200
```

The monitor should print `ESP32 capture node: skeleton`.
