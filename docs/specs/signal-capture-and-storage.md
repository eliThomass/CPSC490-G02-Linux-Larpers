# Specification — Signal capture and storage

> Epic: #47 · Stories: #16, #45, #46, #48, #49
> Owner: Eli Thomas (@eliThomass) · Sprint: 4 · Status: draft · Task: #119
> Design: [`../design/system-design.md`](../design/system-design.md)

Goal 1 is the pipeline every other goal depends on: ESP32 capture nodes
listen for nearby Wi-Fi and Bluetooth signals, turn each capture into one
common observation record, and upload it to a backend that stores it and
returns it on request.

## Scope

**In scope.**

- Passive capture of Wi-Fi metadata (#16) and Bluetooth advertisements (#45)
  on ESP32 capture nodes.
- One common observation format for both protocols, with explicit units and
  missing-field behavior (#46).
- Storing observations in PostgreSQL and retrieving them by time range and
  device identifier, including after a backend restart (#48).
- Repeated collection at an interval during a test session, with scan
  failures reported without stopping collection (#49).

**Out of scope.**

- Deciding what a device is, how close it is, or whether it is recording.
  That is Goal 2, in [`device-identification.md`](device-identification.md).
- Showing observations to the user. That is Goal 3, in
  [`dashboard.md`](dashboard.md).
- Transmitting to, connecting to, or decrypting the traffic of observed
  devices. The nodes only listen to what devices already broadcast.
- Testing against the school's Flock cameras or analyzing private company
  data, per the sponsors (#70).
- Correlating observations of the same device across several nodes. This is
  not designed yet.

**Where it stands (Sprint 4).** The observation format (#46) is defined in
`prototype/backend/schemas.py` and `models.py` and tested with complete and
partial records for each protocol (#109). `POST /observations` and
`GET /observations` store and retrieve observations (#112, #113); the restart
check (#114) is in review as PR #127. The ESP32 firmware is a skeleton that
builds (#92); Wi-Fi capture (#16), Bluetooth capture (#45), and repeated
collection (#49) have not started because the boards have not arrived.

## Functional requirements

Each requirement is the story's acceptance criterion, quoted as written.

| ID | Requirement | Story | Status |
|---|---|---|---|
| FR-1 | A scan returns nearby access points with SSID, BSSID, signal percentage, channel when available, and scan timestamp. | #16 | not started |
| FR-2 | Results are accessible through a local API as JSON. | #16 | not started |
| FR-3 | Repeating a scan updates the results and timestamp. | #16 | not started |
| FR-4 | Scan failures produce understandable responses. | #16 | not started |
| FR-5 | When a known test device emits discoverable Bluetooth advertisements, the collector records observations with timestamps, signal strength, and advertised identifiers when available. | #45 | not started |
| FR-6 | When fields are unavailable, the collector marks them as unavailable without crashing. | #45 | not started |
| FR-7 | The schema defines capture-source ID, protocol, timestamp, available identifiers, signal measurements and their units, and missing-field behavior. | #46 | met (`schemas.py`, `models.py`) |
| FR-8 | When Wi-Fi or Bluetooth observations are collected, their records conform to the documented schema. | #46 | waits on FR-1, FR-5 |
| FR-9 | Validation covers a complete record and a record with unavailable optional fields for each protocol. | #46 | met (#109) |
| FR-10 | Signal percentage and RSSI are distinguished rather than treated as interchangeable measurements. | #46 | met (`rssi_dbm`, `signal_percent`) |
| FR-11 | When an observation is collected, the backend shall persist it in the observation format from #46. | #48 | met (#112) |
| FR-12 | When a client requests a time range, the backend shall return only observations inside that range. | #48 | met (#113) |
| FR-13 | When a client requests a device identifier, the backend shall return only that device's observations, or an empty result if none match. | #48 | met (#113) |
| FR-14 | After the backend restarts, a previously saved test capture is still retrievable. | #48 | in review (PR #127) |
| FR-15 | When a test session is started, the collector shall scan at a configurable interval until it is stopped. | #49 | not started |
| FR-16 | Each scan's observations carry their own timestamp, later than the previous scan's. | #49 | not started |
| FR-17 | When a scan fails, the collector shall report the failure and continue with the next interval. | #49 | not started |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Capture is passive: a node only receives signals that devices already broadcast and never transmits to an observed device. | The sponsors ruled out invasive methods (#70), and passive capture works without control of the local network (`system-context.md` §3). |
| NFR-2 | An observed address is stored as evidence that a device was present, never as its permanent identity. | Devices randomize MAC and Bluetooth addresses [proposal ref. 5], so an address can change between captures (#45). |
| NFR-3 | Every signal measurement names its unit. RSSI is stored in dBm and signal percentage as 0–100, and neither is converted from the other. | Converting would invent precision the hardware did not report (#46). |
| NFR-4 | A field the capture did not provide is stored as unavailable (`null`, or `{}` for metadata), never guessed. | Goal 2 must be able to tell "not broadcast" from "zero" (#45, #46). |
| NFR-5 | Capture times carry a time zone, and the backend records its own receipt time separately. | Nodes and the server may disagree on time; both times are needed to measure delay for #58. |
| NFR-6 | No captures from the school's Flock cameras, and no analysis of private company data. | Sponsor instruction (#70): "DONT TEST OUT SCHOOL FLOCK CAMERAS". |
| NFR-7 | Upload from node to backend leaves room inside the dashboard's 2-second target. | #58 requires display within 2 seconds of capture; how that budget is split is an open question below. |

## Acceptance criteria (epic level)

The epic's success measure (#47), as written:

- [ ] Demonstrate repeated Wi-Fi and Bluetooth collection, a shared
      observation format, persistent retrieval, and ingestion from two
      capture sources.

The stories' remaining acceptance criteria, as written:

- [ ] The prototype runs and compiles on a labtop following its README.md
      (#16)
- [ ] A Teammate successfully runs the prototype (#16)
- [ ] Documentation identifies this as access point discovery and does not
      claim individual IoT device detection. (#16)
- [ ] A teammate reproduces the capture using documented hardware, device
      state, and setup instructions. (#45)
- [ ] Documentation distinguishes advertisement discovery from confirmed
      device identity and records identifier changes observed during
      testing. (#45)
- [ ] A teammate runs a test session from the README and confirms the
      above. (#49)

And for the epic as a whole:

- [ ] FR-1 … FR-17 each have a test, or for hardware behavior a documented
      check a teammate can repeat.
- [ ] `python .github/scripts/check_repo.py` is green and the prototype's
      tests pass in CI.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| #16 asks for "a local backend", results through "a local API", and a prototype that runs "on a laptop", and its deliverables are still placeholders. In the architecture, the ESP32 uploads observations to the FastAPI server. Is #16's local API the FastAPI backend, and should the story's wording be updated to match? (`data-flow.md` §6 raises the same mismatch.) | Hardware (Eli, Ryan, Jonathan) | before #16 starts |
| FR-1 asks for "signal percentage", but the ESP32 Arduino Wi-Fi scan reports RSSI in dBm, and NFR-3 forbids converting one into the other. Is percentage still required, and from what source? | Hardware | before #16 starts |
| An access-point scan (#16) sees access points, and #45 sees Bluetooth advertisers. Many selected devices, such as Ring cameras, likely join an existing Wi-Fi network as clients, which an access-point scan does not see. Does Goal 1 also need to capture Wi-Fi client frames? Goal 2's packet-rate analysis (#55) depends on the answer. | Hardware, with Goal 2 owners | before #16 and #51 start |
| What protocol do nodes use to send observations to the backend? (`architecture.md` §5) | Hardware and Backend | before FR-8 can be checked |
| Who creates `Scanner` and `ScanSession` rows? `POST /observations` rejects unknown IDs, and no endpoint creates them yet. #49 needs a way to start a test session. | Backend | before #49 starts |
| How is an observation matched to a `DetectedDevice` (process 4.0 in `data-flow.md`)? Today `device_id` is set only if the client sends it. | Backend | before #51 starts |
| Where is a scan failure reported? `data-flow.md` §5 decided failures are "not stored or shown", but FR-4 and FR-17 require them to be reported. | Hardware and Backend | before #49 starts |
| How are observations of one device from several nodes combined? (`architecture.md` §5) | Backend | before a second node is added |
| #51 removes bystander identifiers from the dataset. Does the live system also need a retention or removal rule for bystander observations it stores during normal use? | team, with sponsors | before the first capture outside a test room |
