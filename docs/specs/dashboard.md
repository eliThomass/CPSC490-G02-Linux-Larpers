# Specification — Dashboard

> Epic: #56 · Stories: #57, #58, #59, #60, #61
> Owner: Eli Thomas (@eliThomass) · Sprint: 4 · Status: draft · Task: #119
> Design: [`../design/system-design.md`](../design/system-design.md)

Goal 3 is the part of the system the user actually sees: an Angular
dashboard that shows which devices are nearby, what they probably are, how
close they are, and when they were last seen, updating on its own as new
observations arrive.

## Scope

**In scope.**

- Listing detected devices with identification (when available), protocol,
  signal strength, and last-seen time (#57).
- Updating without a manual refresh, within 2 seconds of capture (#58).
- Showing identification confidence and proximity, and labeling unknown
  devices, unavailable estimates, and stale observations (#59).
- Filtering by protocol, device classification, and last-seen time, and
  showing one device's observation history (#60).
- A usability evaluation with participants outside the team (#61).

**Out of scope.**

- A raw packet or log view like Kismet's. The users are non-technical
  (proposal §1, §3).
- Configuring capture nodes or starting test sessions from the dashboard.
  No story asks for it.
- User accounts and sign-in. No story asks for them; see the open questions.

**Where it stands (Sprint 4).** The Angular starter is scaffolded in
`prototype/dashboard/` and builds and tests (#94, PR #124). It does not call
the backend yet. The backend offers `GET /observations`, filtered by
`start`, `end`, and `device_id`; it has no device list, protocol filter, or
analysis results yet.

## Functional requirements

Each requirement is the story's acceptance criterion, quoted as written.

| ID | Requirement | Story |
|---|---|---|
| FR-1 | For each detected device, the dashboard shows identification (when available), protocol, signal strength, and last-seen time. | #57 |
| FR-2 | When the backend returns no observations, the dashboard shall say so instead of showing an empty table. | #57 |
| FR-3 | When the backend receives a new observation, the dashboard shall show it without a manual page refresh. | #58 |
| FR-4 | When a new observation is captured, the dashboard shall display it within 2 seconds. | #58 |
| FR-5 | Each identified device shows the confidence value from Objective 2.3. | #59 |
| FR-6 | Each device shows the proximity/location estimate from Objective 2.4, or "unavailable". | #59 |
| FR-7 | Unknown devices, unavailable estimates, and stale observations each have a visible label; the staleness cutoff is documented. | #59 |
| FR-8 | The user can filter by protocol, device classification, and last-seen time, and combine filters. | #60 |
| FR-9 | Selecting a device shows its observation history. | #60 |
| FR-10 | When no device matches the filters, the dashboard shall say so. | #60 |

## Verification requirements

Also acceptance criteria quoted as written; they describe how the dashboard
is checked rather than what it does.

| ID | Requirement | Story |
|---|---|---|
| VR-1 | For a known test dataset, every displayed value matches the backend's response. | #57 |
| VR-2 | The delay from capture to dashboard display is measured and recorded. | #58 |
| VR-3 | Participants outside the team attempt three tasks: identify a detected device, find when it was last observed, and explain what the display tells them. | #61 |
| VR-4 | Task results and observed problems are written up. | #61 |
| VR-5 | Each problem found is either fixed or filed as its own issue. | #61 |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Each observation appears within 2 seconds of capture (FR-4). | The sponsors want real-time data that is "demoable (not like a 10 minute delay)" (#101). |
| NFR-2 | A user without a wireless background can read every screen. | The epic's success measure names this user (#56), and the proposal is written for non-technical users (§1). |
| NFR-3 | Uncertainty is always visible: a confidence value, "unknown", "unavailable", or "stale" is shown rather than hidden. | A clean screen that hides uncertainty would overstate what the system knows (FR-5 to FR-7). |
| NFR-4 | The dashboard is built in Angular. | The sponsors are familiar with Angular and can support it (#70). |
| NFR-5 | The dashboard reads data only through the backend API, never from the database directly. | The architecture puts the backend between the dashboard and PostgreSQL (`architecture.md` §3). |

## Acceptance criteria (epic level)

The epic's success measure (#56), as written:

- [ ] A user without a wireless background can find a detected device, when
      it was last seen, and its approximate location on the dashboard, and
      new observations appear within the team's real-time target.

And for the epic as a whole:

- [ ] FR-1 … FR-10 each have a test that fails if the behavior is removed.
- [ ] VR-1 … VR-5 are met, with the measured delay recorded in
      `prototype/README.md` and the evaluation in
      `docs/design/usability-evaluation.md`.
- [ ] `python .github/scripts/check_repo.py` is green and the prototype's
      tests pass in CI.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Does the dashboard poll the backend or receive pushed updates (for example over a WebSocket)? Proposal §4 leaves this undecided, and it decides whether FR-4 can be met. | Frontend (Jasmine, Chris) and Backend | before #58 starts |
| The dashboard needs a device list with last-seen times, a protocol filter, and analysis results (confidence, proximity). None of these endpoints exist yet. Who builds them, and in which story? | Backend | before #57 and #59 start |
| What is the staleness cutoff (FR-7)? | Frontend | before #59 starts |
| FR-4 measures from capture time on the ESP32 to display in the browser. How are the node's and browser's clocks compared when measuring VR-2? | Frontend and Hardware | before VR-2 is measured |
| The epic's success measure asks for "approximate location", but #54 may produce only a distance from one scanner. Is a distance enough, or does the dashboard need a position? | team, with sponsors | before #59 starts |
| The classification filter (FR-8) depends on #53, which is a CPSC 491 item. Does #60 ship the protocol and last-seen filters first? | Frontend | before #60 starts |
| Who are the usability participants, how many, and how are they recruited (VR-3)? | Frontend | before #61 starts |
| The dashboard shows addresses of nearby devices, including bystanders'. Does it need sign-in, or is it only ever run locally? | team, with sponsors | before the dashboard runs off a developer's laptop |
