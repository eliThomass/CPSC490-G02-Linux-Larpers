# Design — Data flow

> Epic: #47, #50, #56 · Stories: #16, #45, #46, #48, #49, #51, #52, #53, #54, #55, #57, #58, #59, #60, #61
> Owner: Eli Thomas (@eliThomass) · Sprint: 2 · Status: draft · Task: #77
> Related: ER diagram (#82), high-level architecture diagram (#84)

This document answers one question: **how does signal data move through the
system and get transformed, from a nearby device's radio signal to what the
user sees on the dashboard?** It uses Gane-Sarson notation: external
entities are rectangles, processes are rounded rectangles, data stores are
open-ended rectangles, and arrows are data flows labeled with the data that
moves.

![Level 0 and Level 1 data flow diagrams. Level 0: nearby IoT devices send
Wi-Fi frames and BLE advertisements, the project team sends known device
models and session labels, and the user sends filter requests to the Signal
Capture and Analysis System, which returns the dashboard view. Level 1: on
the ESP32, processes 1.0 Scan Wi-Fi and 2.0 Scan Bluetooth feed 3.0
Normalize into Observation, which uploads Observations over Wi-Fi to the
server. On the server, 4.0 Ingest and Store writes the six PostgreSQL stores;
5.0 Identify Device, 6.0 Estimate Proximity, and 7.0 Detect Recording State
read them and write AnalysisResult; 8.0 Present Dashboard reads the stores
and serves the user.](diagrams/dfd.png)

*Figure 1 — Level 0 (top) and Level 1 (bottom) DFDs. Processes 5.0–7.0 are
planned for Sprints 3–4; 7.0 is dashed because recording-state detection is
an open research question (#55). The system has one ESP32 scanner today;
more scanners can be added without changing the flows.*

Editable source: [`diagrams/dfd.html`](diagrams/dfd.html), a self-contained
page with both diagrams as inline SVG. Edit the SVG, open the page in a
browser, and re-export `diagrams/dfd.png` from it.

## 1. Level 0 — context

The whole system is one process. Four flows cross its boundary:

| From | To | Data |
|---|---|---|
| Nearby IoT Devices | System | Wi-Fi frames, BLE advertisements |
| Project Team | System | Known device models, session labels |
| User | System | Filter and inspect requests |
| System | User | Dashboard view and live updates |

The Level 1 diagram balances against this: the flows that cross its outer
edge are exactly these four.

## 2. Level 1 — boundaries

| Boundary | Runs | Processes |
|---|---|---|
| ESP32 (capture node) | firmware in C/C++ | 1.0, 2.0, 3.0 |
| Server | FastAPI, PostgreSQL, Angular | 4.0–8.0, stores D1–D6 |

The only flow between the two boundaries is **Observations (over Wi-Fi)**:
the ESP32 normalizes each capture itself and uploads finished Observations
to the FastAPI backend.

## 3. Level 1 — processes

| # | Process | What it does | Stories |
|---|---|---|---|
| 1.0 | Scan Wi-Fi | Captures Wi-Fi frames from devices in range | #16 |
| 2.0 | Scan Bluetooth | Captures BLE advertisements from devices in range | #45 |
| 3.0 | Normalize into Observation | Converts raw records into the common observation format (capture source, protocol, timestamp, identifiers, signal measurement and units) | #46 |
| 4.0 | Ingest & Store | Receives uploaded Observations, matches each one to an existing tracked device or creates one, and stores the team's device models and session labels | #48, #49 |
| 5.0 | Identify Device | Predicts a device's model and a confidence from its Observations, the known models, and labeled sessions | #51, #52, #53 |
| 6.0 | Estimate Proximity | Estimates distance from the scanner using signal strength (RSSI) | #54 |
| 7.0 | Detect Recording State | Investigates whether Observations show that a device is recording, using labeled sessions | #55 |
| 8.0 | Present Dashboard | Shows tracked devices, signal strength, last-seen time, and analysis results; handles user filtering and inspection | #57–#61 |

## 4. Level 1 — data stores

Every store is a PostgreSQL table and an entity in the ER diagram (#82).
The names match so the two diagrams can be read together.

| Store | Holds | Written by | Read by |
|---|---|---|---|
| D1 Observation | One captured signal: timestamps, protocol, observed address, RSSI, metadata | 4.0 | 5.0, 6.0, 7.0, 8.0 |
| D2 DetectedDevice | A device the backend tracks across Observations | 4.0 | 4.0, 8.0 |
| D3 ScanSession | One collection or testing period, with its test labels | 4.0 | 5.0, 7.0 |
| D4 Scanner | The ESP32 hardware that captured each Observation | 4.0 | 6.0 |
| D5 DeviceModel | Catalog of known manufacturers, models, and categories | 4.0 | 5.0 |
| D6 AnalysisResult | Predicted model, confidence, recording state, proximity | 5.0, 6.0, 7.0 | 8.0 |

An observed address is evidence, not a permanent device identity: Bluetooth
addresses can change between captures (#45), so 4.0 matching an Observation
to a DetectedDevice is a best guess, not a fact.

## 5. Decisions behind the diagram

| Decision | Chosen | Alternative |
|---|---|---|
| Capture hardware | One ESP32 (more may be added later) | Laptop Wi-Fi adapter |
| ESP32 to server transport | Wi-Fi upload to FastAPI | USB serial to a computer |
| Where normalization happens | On the ESP32, before upload | On the server, after upload |
| Scan failures | Not stored or shown | A separate failure store |
| Labeled training data | Optional label fields on ScanSession | A separate labels entity |

## 6. Open items

- **ScanSession label fields.** The DFD's "Labeled sessions" flows into 5.0
  and 7.0 need ScanSession to record the labeled device model and the
  recording state for a test session. The current ER diagram has
  `test_conditions` only.
- **Meaning of "node".** This diagram treats the ESP32 scanner as the node.
  Proposal §0 still says each IoT device in range is treated as a node.
- **Wi-Fi prototype stories.** #16 and #17 still describe scanning from a
  laptop's built-in Wi-Fi adapter rather than the ESP32.
