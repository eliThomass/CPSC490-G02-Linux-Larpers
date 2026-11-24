# Specification — Device identification and signal analysis

> Epic: #50 · Stories: #51, #52, #53, #54, #55
> Owner: Eli Thomas (@eliThomass) · Sprint: 4 · Status: draft · Task: #119
> Design: [`../design/system-design.md`](../design/system-design.md)

Goal 2 turns stored observations into answers about a small set of selected
recording devices: which device it is, roughly where it is, and whether its
signals show that it is recording. Every answer is measured against labeled
captures the team collects itself.

## Scope

**In scope.**

- A labeled dataset of repeated captures of the approved devices: Meta
  glasses, Ring cameras, body cameras, and spy cameras, provided by the
  advisors and RTX (proposal §4) (#51).
- Candidate fingerprints: the observable characteristics that distinguish
  the selected devices, and which stay consistent across captures (#52).
- Classifying observations as one of the selected devices, with a
  confidence value, or as "unknown" (#53).
- Estimating proximity or location from signal measurements and reporting
  the error against known test positions (#54).
- Investigating whether signal metadata shows that a device is recording
  (#55).

**Out of scope.**

- Identifying devices outside the selected set. They are reported as
  "unknown" rather than given the closest class (proposal §3).
- Looking up a manufacturer from a MAC address, which address randomization
  defeats, and general-purpose classifiers such as Lumos's (proposal §3).
- Locating devices by having the user walk around the room, as Lumos and
  SnoopDog do (proposal §3).
- Promising that recording detection works. #55 is an investigation, and a
  negative result backed by captures counts as done.
- Flock cameras and private company data (#70).

**Where it stands (Sprint 4).** Not started. All five stories moved from
Sprint 3 with no tasks filed under them. The dataset (#51) needs the ESP32
boards and the test devices; #52–#55 depend on the dataset. The
`DeviceModel` and `AnalysisResult` tables from the ER diagram (#82) are not
in `prototype/backend/models.py` yet.

## Functional requirements

Each requirement is the story's acceptance criterion, quoted as written.

| ID | Requirement | Story |
|---|---|---|
| FR-1 | When an observation matches a selected device, the backend shall return the device class and a confidence value. | #53 |
| FR-2 | When an observation matches no selected device, the backend shall return "unknown" instead of the closest class. | #53 |
| FR-3 | When signal measurements for a device are available, the backend shall return a proximity or location estimate; otherwise it shall mark the estimate unavailable. | #54 |

## Dataset and evaluation requirements

These are also acceptance criteria quoted as written. They describe the
evidence each story must produce rather than system behavior.

| ID | Requirement | Story | Deliverable |
|---|---|---|---|
| DR-1 | The dataset has repeated captures for every device in the approved set. | #51 | `docs/specs/device-dataset.md` |
| DR-2 | Every capture is labeled with device model, capture date, and test conditions (distance, environment, device state). | #51 | same |
| DR-3 | Captures use the observation format from #46. | #51 | same |
| DR-4 | The capture procedure is documented well enough that a teammate can add a capture the same way. | #51 | same |
| DR-5 | Identifiers from non-test (bystander) devices are removed or excluded before the dataset is committed. | #51 | same |
| DR-6 | Each candidate characteristic is listed with the devices it distinguishes. | #52 | `docs/design/device-fingerprints.md` |
| DR-7 | Each characteristic is marked consistent, variable, or unavailable across repeated captures, with the captures used as evidence. | #52 | same |
| DR-8 | Characteristics that change between captures (e.g. randomized MAC addresses) are documented as unreliable. | #52 | same |
| DR-9 | Accuracy is measured on captures not used to build the fingerprints and reported per device class. | #53 | `docs/design/device-fingerprints.md` |
| DR-10 | Misclassifications from the evaluation are listed with their likely cause. | #53 | same |
| DR-11 | Estimates are compared against measured test positions, and distance error is reported (average and worst case). | #54 | `docs/design/device-location.md` |
| DR-12 | The test setup (positions, capture hardware, environment) is documented so the test can be repeated. | #54 | same |
| DR-13 | For each tested device, captures are taken while recording and while idle under the same conditions. | #55 | `docs/design/recording-detection.md` |
| DR-14 | Differences between the two states are reported with the metric used (e.g. packet rate, frame size). | #55 | same |
| DR-15 | The report states whether recording-state detection is supported, with measured performance and limitations. | #55 | same |
| DR-16 | A negative result counts as done if it is backed by the captures. | #55 | same |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | When unsure, the system says "unknown" rather than guessing. | A wrong "this is a body camera" misleads a non-technical user more than "unknown" does (proposal §3, FR-2). |
| NFR-2 | Every identification and recording result carries a confidence value. | The dashboard must show uncertainty (#59). |
| NFR-3 | Accuracy is reported only on captures that were not used to build the fingerprints. | Testing on training captures would overstate accuracy (DR-9). |
| NFR-4 | Every experiment is documented well enough for a teammate to repeat it. | DR-4 and DR-12 require it, and results that cannot be repeated cannot be checked. |
| NFR-5 | Each stored analysis result records the algorithm version that produced it. | Results from different fingerprint versions must not be mixed. The ER diagram has `algorithm_version` on `AnalysisResult` for this. |
| NFR-6 | Bystander identifiers never reach the committed dataset. | Captures in shared spaces pick up people who did not agree to be recorded (DR-5). |
| NFR-7 | Test devices are captured in a secure room. | The sponsors want the room "secure" (#70), and the devices are provided by the advisors and RTX (proposal §4, #67). |

## Acceptance criteria (epic level)

The epic's success measure (#50), as written:

- [ ] The approved test devices are classified from captured metadata with
      measured per-device accuracy, unmatched devices are reported as
      unknown, location error is reported against known positions, and a
      documented finding states whether recording state can be detected.

And for the epic as a whole:

- [ ] FR-1 … FR-3 each have a test that fails if the behavior is removed.
- [ ] DR-1 … DR-16 are each met in the deliverable named in the table above.
- [ ] `python .github/scripts/check_repo.py` is green and the prototype's
      tests pass in CI.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Which exact models make up the "approved set", how many units of each will the advisors and RTX lend, and when? | team, with sponsors | before #51 starts |
| Does the sponsors' "analyzing any private company data" rule (#70) limit the dataset in any way? This was left open after the 2026-10-15 meeting. | team, with sponsors | before #51 starts |
| Where is the secure test room? (#67) | all five | before #51 starts |
| `ScanSession` has only `test_conditions`. The dataset needs the device model and the recording state for each session (`data-flow.md` §6). Add label fields, or a separate labels table? | Backend | before #51 starts |
| How many captures per device, and how are they split between building fingerprints and evaluating them (DR-9)? | Backend | before #53 starts |
| What confidence threshold turns a match into "unknown" (FR-2)? | Backend | before #53 is evaluated |
| No story sets an accuracy target, only that accuracy is measured. Do the sponsors expect one? | team, with sponsors | before #53 is evaluated |
| Proximity from one scanner gives a distance, not a position. Does #54 estimate distance from the reference scanner (as the ER diagram's `estimated_distance_m` suggests) or a position from several nodes? | Backend | before #54 starts |
| Metrics such as packet rate and frame size (DR-14) need captured Wi-Fi frames, not an access-point scan. This depends on the Goal 1 question about capturing Wi-Fi client frames (`signal-capture-and-storage.md`). | Hardware and Backend | before #55 starts |
| `AnalysisResult` covers a time window (`window_start`, `window_end`). How long is a window, and does analysis run as observations arrive or in batches? | Backend | before #53 starts |
