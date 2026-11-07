# Sprint 2 review — Oct 13 – Oct 26

> Written at the Sprint 2 boundary by Eli Thomas (@eliThomass, team leader).
> Numbers come from `scripts/sprint_report.py`, the issue tracker, and merged
> pull requests as they stood at the boundary.

## Progress this sprint — the substance

**Proposal moved:**

| Section | What changed | Where |
|---|---|---|
| §2 Goals and Objectives | Removed Goal 0 per the HW5 feedback | PR #66 (#22) |
| §0, §1 | Proofread for HW5 | PR #65 (#39) |
| §0, §1 | Removed the Flock camera data-retrieval content, per the sponsor | PR #71 (#68) |
| §0, §1 | Named the ESP32 as the capture hardware | PR #83 (#81) |
| §5, §6 | Wrote Project Outcomes and Project Timeline | PR #88 (#24) |
| §4 | Proposed AWS Lightsail hosting and SSH-tunnel development | PR #87 (#86), merged into the #23 branch |
| `docs/design/diagrams/architecture.drawio.png` | High-level architecture diagram | PR #85 (#84) |
| `docs/design/NodeAnalysisERdiagram.png` | ER diagram: six PostgreSQL entities | PR #89 (#82) |
| `docs/design/data-flow.md` | Level 0 and Level 1 data flow diagrams and design doc | PR #90 (#77) |
| `README.md` | Team roles and role descriptions | PR #74 (#69) |
| Repository | Synced `develop` with `main` and switched to the Gitflow workflow | PR #76 (#75) |
| Repository | Removed the leftover `README.old.md` | PR #78 (#73) |

§3 Proposed Approaches and the rest of §4 (#23) are drafted on
`feature/23-approach-environment` but not merged. The explanations behind
each approach and each environment choice are still being written.

**Prototype moved:** no prototype code was merged this sprint. The team
chose the stack at the 2026-10-20 meeting (#79): ESP32 (C/C++), FastAPI,
PostgreSQL, Angular. The scaffold was split into one task per component
(#92–#95). The FastAPI scaffold (#95, PR #96) runs locally and passes its
tests in CI (`test_health`), and was approved on Oct 27, after the
boundary. The Wi-Fi and Bluetooth prototype stories did not start because
the team is waiting on the ESP32 boards.

## Velocity

| | Story points | Issues |
|---|---|---|
| Planned (in the Sprint 2 milestone at the boundary) | 13 | 20 |
| Completed | 8 | 14 |

From `scripts/sprint_report.py --sprint 2`:

| Sprint | Window | Committed | Added mid | Completed | Open/carried | Closed late | Done % |
|---|---|---|---|---|---|---|---|
| Sprint 2 | Oct 13 – Oct 26 | 1 | 12 | 8 | 5 | 0 | 62% |

12 of the 13 points were added after the sprint began, and 9 points sit on
sub-issues whose parent story is also pointed (counted once, at the
parent). The seven prototype stories moved to Sprint 3 are not counted
here.

## Completed (merged PRs)

| Story | Owner | Points | PR |
|---|---|---|---|
| #77 Draw the Level 0 and Level 1 data flow diagrams | @eliThomass | 2 | #90 |
| #81 Update §0 and §1 to name the ESP32 | @eliThomass | 1 | #83 |
| #73 Remove leftover README.old.md | @eliThomass | 1 | #78 |
| #69 Decide team roles and record them in README.md | @eliThomass | 1 | #74 |
| #22 Define goals and objectives in §2 (Sprint 1 issue) | @eliThomass | 2 | #66 |
| #39 Proofread §0 and §1 for HW5 (Sprint 1 issue) | @eliThomass | 1 | #65 |
| #82 Include the ER diagram | @Perryboi8 | — | #89 |
| #68 Remove Flock camera content from the proposal | @Perryboi8 | 1 | #71 |
| #24 Write §5 and §6 | @jcerasuolo5 | 1 | #88 |
| #75 Sync develop with main and switch to Gitflow | @jcerasuolo5 | — | #76 |
| #84 Draw the high-level architecture diagram | @soo-nexus | 2 | #85 |
| #86 Propose AWS Lightsail hosting in §4 | @soo-nexus | 1 | #87 |

Closed without a PR: meetings #70 (sponsor, Oct 15), #72 (Discord call),
#79 (Oct 20), and #80 (Oct 22). #91 was closed as not planned and split into
#92–#95.

## Carried over — and why

| Story | Owner | Why not finished | Decision |
|---|---|---|---|
| #16 Wi-Fi discovery (3 sp), #17, #18 | unassigned | Waiting on the ESP32 boards | Moved to Sprint 3 |
| #45 Bluetooth discovery (3 sp) | unassigned | Waiting on the ESP32 boards | Moved to Sprint 3 |
| #46 Standardize metadata (2 sp) | unassigned | Depends on #16 and #45 | Moved to Sprint 3 |
| #48 Store and retrieve observations (2 sp) | unassigned | Depends on #46 | Moved to Sprint 3 |
| #49 Repeated signal collection (2 sp) | unassigned | Depends on #48 | Moved to Sprint 3 |
| #23 Write §3 and §4 | @Perryboi8 | Explanations for each approach and environment choice still being written | Carry to Sprint 3 |
| #95 Scaffold the FastAPI backend | @eliThomass | PR #96 approved after the boundary | Carry to Sprint 3; merge #96 |
| #92, #93, #94 Scaffold ESP32, PostgreSQL, Angular | unassigned | Filed Oct 26, at the end of the sprint | Carry to Sprint 3 |
| #67 Secure a dedicated project room | 4 assignees | Room not secured yet | Carry to Sprint 3 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | about 4 (11 PRs) |
| Harness rules added (rows in the harness log) | 0 |

Iterations to green counts CI runs on each PR's branch until the first green
run, so it overcounts when one push triggers both a push and a pull-request
run. We are still discovering
requirements during the work: most of this sprint's issues were filed after
it started.

## Prototype increment

None merged. At the boundary, the FastAPI scaffold (PR #96) serves `/` and
`/health` and passes `test_health` and `test_root` locally and in CI. It is
demonstrated by following `prototype/README.md` from a clean clone and
opening `http://127.0.0.1:8000/health`.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Instructor, HW5: remove Goal 0 | Removed Goal 0 from §2 | #22 / PR #66 |
| Sponsor, Oct 15 (#70): "take out the flock camera sections where you intend to retrieve data from flock cameras" | Removed the Flock content | #68 / PR #71 |
| Sponsor, Oct 15 (#70): "fill in any template information such as the filler brackets <> and the ai page" | §5 and §6 written; §3 and §4 in progress; §7 AI Usage not started | #24 / PR #88, #23, #25 |
| Sponsor, Oct 15 (#70): "Decide Individual Roles by end of next week 10/20" | Roles recorded in README.md on Oct 22 | #69 / PR #74 |
| Sponsor, Oct 15 (#70): "Angular (Tracy and Cara are familiar)" | Adopted Angular for the dashboard | #79 |
| Sponsor, Oct 15 (#70): "Gonna need to show a skeleton of the project" | Filed one scaffold task per component; FastAPI scaffold in review | #92–#95 / PR #96 |
| Sponsor, Oct 15 (#70): a dedicated project room, as long as it is secure | Not secured yet | #67 |
| Instructor, Oct 26 review: give the reason behind each choice in §4 | In progress | #23 |

## Contribution snapshot

| Member | Meetings attended (of 4) | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @eliThomass | 3 | 6 | 9 | 6 |
| @Perryboi8 | 3 | 2 | 4 | 6 |
| @jcerasuolo5 | 2 | 2 | 2 | 1 |
| @soo-nexus | 2 | 2 | 2 | 0 |
| @chroyy | 3 | 0 | 0 | 0 |

Meetings are #70, #72, #79, and #80. Merged PRs are those authored and
merged Oct 13–26. Issues closed are completed Sprint 2 issues the member is
assigned to, including meeting issues. Reviews given are on PRs merged
Oct 13–26.

## What we change next sprint

- Commit about 8 points, the one-sprint average from `scripts/sprint_report.py`.
- Point user stories, not their sub-tasks, so points are not double-counted.
- File and point issues at sprint planning rather than mid-sprint.
- Assign an owner to every carried-over story and scaffold task (#16–#18,
  #45, #46, #48, #49, #92–#94).
