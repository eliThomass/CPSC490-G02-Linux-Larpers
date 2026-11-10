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
