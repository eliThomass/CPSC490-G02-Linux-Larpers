# Sprint 3 review — Oct 27 – Nov 9

> Written at the Sprint 3 boundary by Eli Thomas (@eliThomass, team leader).
> Numbers come from `scripts/sprint_report.py`, the issue tracker, and merged
> pull requests as they stood at the end of Nov 9 (Pacific time).

## Progress this sprint — the substance

**Proposal moved:**

| Section | What changed | Where |
|---|---|---|
| §3 Proposed Approaches | Wrote the section | PR #106 (#104) |
| §4 Required Environment | Wrote the environment, resources, and work items; replaced the work-items table with paragraphs | PR #120 (#105) |
| `docs/design/system-context.md` | System context diagram and doc | PR #98 (#97) |
| `docs/design/system-context.md`, diagrams | Removed AWS Lightsail from the context doc and the architecture and context diagrams | PR #116 (#102) |
| `docs/design/architecture.md` | Added the architecture doc; showed the self-hosted server in the architecture diagram | PR #121 (#118) |

The specification and design documents are not written yet. The instructor's
Sprint 3 guidance (one spec per epic, six-part design documents) is filed as
#119 for Sprint 4. Each teammate's development operating system is still
missing from §4 (#117).

**Prototype moved:** at the start of the sprint `prototype/` held only the
FastAPI starter, still in review. By the boundary all four components from
the architecture diagram had a scaffold on `develop`, and the backend stores
and retrieves observations in PostgreSQL:

- FastAPI backend, `/` and `/health` (PR #96, #95)
- PostgreSQL 17 in Docker Compose, `/health/db` (PR #115, #93 and #110)
- Observation model and ORM tables from the ER diagram (PR #122 and PR #125, #108)
- `POST /observations` validates and stores one observation (PR #122, #112)
- `GET /observations` filters by time range and device (PR #123, #113)
- Angular dashboard starter (PR #124, #94)
- ESP32 firmware skeleton built with PlatformIO (PR #129, #92)

No Wi-Fi or Bluetooth capture exists yet. The ESP32 firmware builds, but it
has not run on a board because the team is still waiting on the hardware.

## Velocity

| | Story points | Issues |
|---|---|---|
| Planned (in the Sprint 3 milestone at the boundary) | 28 | 33 |
| Completed | 1 | 14 |

From `scripts/sprint_report.py --sprint 3`:

| Sprint | Window | Committed | Added mid | Completed | Open/carried | Closed late | Done % |
|---|---|---|---|---|---|---|---|
| Sprint 3 | Oct 27 – Nov 09 | 26 | 2 | 1 | 26 | 1 | 4% |

The low point total is real, and it has two causes. Points sit on the user
stories, and no story closed: #48 is one task short (#114, in review as PR
#127), #46 is one task short (#109, in review as PR #126), and the Wi-Fi and
Bluetooth stories (#16, #45, #49) wait on the boards. The five Goal 2
stories (#51–#55, 18 points) sat in Sprint 3 without any tasks filed under
them. They were not started and move to Sprint 4.

The script counts #92 as closed late because it closed at 07:30 UTC on Nov
10, which was 11:30 PM on Nov 9 Pacific time.

## Completed (merged PRs)

| Story | Owner | Points | PR |
|---|---|---|---|
| #104 Write §3 Proposed Approaches | @eliThomass | — | #106 |
| #105 Write §4 Required Environment | @eliThomass | — | #120 |
| #99 Write the Sprint 2 review | @eliThomass | — | #100 |
| #93, #110 Set up the PostgreSQL database | @eliThomass | — | #115 |
| #112 Store an observation through the API | @eliThomass | — | #122 |
| #113 Retrieve observations by time range and device | @eliThomass | — | #123 |
| #95 Scaffold the FastAPI backend (Sprint 2 issue) | @eliThomass | — | #96 |
| #108 Define the Observation model | @Perryboi8 | — | #125 |
| #97 Draw the system context diagram | @jcerasuolo5 | — | #98 |
| #102 Remove AWS Lightsail from the design docs | @jcerasuolo5 | — | #116 |
| #94 Scaffold the Angular dashboard | @jcerasuolo5 | — | #124 |
| #118 Show the self-hosted server in the architecture docs | @soo-nexus | 1 | #121 |
| #92 Scaffold the ESP32 firmware project | @soo-nexus | 1 | #129 |

PR #120 shows as closed rather than merged: its merge commit (`fc5df09`)
landed on `develop` on Nov 8, but GitHub did not mark the PR merged. Closed
without a PR: the sponsor meeting #101 (Oct 27).

## Carried over — and why

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #48 Store and retrieve observations (2 sp), #111, #114 | @eliThomass | #112 and #113 merged; #114 in review (PR #127) | Stays in Sprint 3; nearly complete once PR #127 merges |
| #46 Standardize metadata (1 sp), #107, #109 | @Perryboi8 (#107, #109) | #108 merged; #109 has changes requested (PR #126) | Stays in Sprint 3; nearly complete once PR #126 merges |
| #16 Wi-Fi discovery (3 sp), #17, #18 | unassigned | Waiting on the ESP32 boards | Moved to Sprint 4 |
| #45 Bluetooth discovery (2 sp) | unassigned | Waiting on the ESP32 boards | Moved to Sprint 4 |
| #49 Repeated signal collection (1 sp) | unassigned | Depends on #16 and #45 | Moved to Sprint 4 |
| #51 Labeled dataset (3 sp) | @chroyy | Not started | Moved to Sprint 4 |
| #52–#55 Goal 2 stories (15 sp) | unassigned | Not started; no tasks filed | Moved to Sprint 4 |
| #25 Finalize §7 AI Usage and §8 References | unassigned | Not started | Moved to Sprint 4 |
| #67 Secure a dedicated project room | all five | Room not secured; still in the Sprint 2 milestone | Stays open and in progress |

The epics #47 and #50 are also in the Sprint 3 milestone. They span the
whole project, so they stay open.

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | about 5 (13 PRs) |
| Harness rules added (rows in the harness log) | 0 |

Iterations to green counts CI runs on each PR's branch until the first green
run. It overcounts when one push triggers more than one run, and
`feature/84-architecture-diagram` was reused for PR #85 in Sprint 2. Most
prototype tasks (#107–#114) were filed on Nov 3, a week into the sprint, so
we are still discovering work during the sprint rather than at planning.

## Prototype increment

At the boundary the prototype can store an observation and read it back
with filters. With PostgreSQL running in Docker:

- `POST /observations` returns `201` with the new `observation_id`, and
  `422` for an unknown scanner, session, or device.
- `GET /observations?start=…&end=…` returns only observations inside the
  range; `?device_id=…` returns only that device's observations, or `[]`.

This was demonstrated with `curl` against PostgreSQL 17 in Docker, and by 11
tests in CI (`test_main.py`, `test_observations.py`). The Angular dashboard
builds and serves its starter page (`ng build`, `ng test`, 2 passed), and
the ESP32 firmware builds with `pio run` (`[SUCCESS]`). Setup steps for each
component are in `prototype/README.md`.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Sponsor, Oct 27 (#101): "Real time data -> as long as it is demoable (not like a 10 minute delay)" | Not acted on yet; it applies once Wi-Fi and Bluetooth capture work (#16, #45) | #101 |
| Sponsor, Oct 27 (#101): "AWS Lightsail potentially (~$168 for 8 months) (put on item list if allowed by RTX)" | Moved to a self-hosted server; removed Lightsail from the design docs | #102 / PR #116, #118 / PR #121, #105 / PR #120 |
| Sponsor, Oct 27 (#101): "Presentation will be similar to a stand-up (where we are, what we plan to do next, blockers, etc.)" | The date is not confirmed, most likely the week of Nov 16; we will start preparing a stand-up slide | #101 |
| Sponsor, Oct 27 (#101): "Order list should be finalized by **Thursday before 5PM**" | The order list was finalized; we will ask the sponsor for an update on the items at the Nov 11 meeting | #101 |
| Instructor, Oct 26 review: give the reason behind each choice in §4 | §4 written with the reasons | #105 / PR #120 |
| Instructor, Sprint 3 email: "A table or chart of issue links therefore adds nothing to your page count. Write full paragraphs that explain the work, and end each paragraph with its issue references." | Replaced the §4 work-items table with paragraphs | #105 / PR #120 |
| Instructor, Sprint 3 email: "Story points go on the user story only, once." | Not fixed yet: tasks #92 and #118 still carry `sp: 1` | Sprint 4 |
| Instructor, Sprint 3 email: one specification per epic; six-part design documents | Filed for Sprint 4 | #119 |
| Sponsor, Oct 15 (#70): a dedicated project room | Not secured yet | #67 |
| Our Sprint 2 review: commit about 8 points | Not followed: 28 points planned | — |
| Our Sprint 2 review: assign an owner to every carried-over story | Done for #92–#94; #16, #45, #46, #49 still unassigned | — |

## Contribution snapshot

| Member | Meetings attended (of 1) | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @eliThomass | 1 | 8 | 8 | 5 |
| @Perryboi8 | 0 | 1 | 1 | 3 |
| @jcerasuolo5 | 0 | 3 | 3 | 2 |
| @soo-nexus | 1 | 2 | 3 | 4 |
| @chroyy | 0 | 0 | 0 | 3 |

The only meeting with an issue is #101. Merged PRs are those authored and
merged Oct 27 – Nov 9, counting PR #120. Issues closed are completed Sprint 3
issues the member is assigned to, including #101. Reviews given are on PRs
merged Oct 27 – Nov 9.

Four PRs were merged by their own author: #103, #115, and #122
(@eliThomass), and #121 (@soo-nexus). Each was approved by another teammate
first. @chroyy contributed through reviews (3 this sprint), and @Perryboi8
has a second PR in review (#126).

## What we change next sprint

- The reviewer merges, not the author.
- Move the `sp:` labels on #92 and #118 to their user stories.
- Assign owners to #16, #45, #46, #49, and #52–#55.
- Moved the carried-over stories to Sprint 4 and re-estimated all 13 Sprint 4
  stories from `sp: 1` to `sp: 5`, keeping 4 and 5 for the largest: four at
  1, four at 2, two at 3, two at 4 (#16, #55), and one at 5 (#53), for 31
  points. This is still far above the 1 point completed in Sprint 3.
