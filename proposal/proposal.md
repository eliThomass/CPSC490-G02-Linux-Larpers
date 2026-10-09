# Project Proposal — Distributed Signal Capture for Multi-Node Analysis

**Department of Computer Science**
**CPSC 490 Undergraduate Seminar in Computer Science — Proposal for Capstone Project**

**Group 02 — Linux Larpers** · Sponsor: RTX-4  
Authors: Thomas, Eli (eliThomass), Perry, Ryan (Perryboi8), Cerasuolo, Jasmine (jcerasuolo5), Huynh, Chris (chroyy), Soo, Jonathan (soo-nexus)  
Date: 2026-10-04

> **This file is the proposal document, not a README.** Its section numbers,
> titles, and guidance are copied from the course Word template, so it
> converts cleanly for Canvas submission. Write continuous academic prose —
> no task lists, no emoji, no repo jargon.
>
> Each section below opens with the template's own guidance in a quote block.
> **Delete the quote blocks and every 〈bracket〉 before submitting.**
>
> **Getting this into the Word template for Canvas.** The template numbers
> its headings **automatically** (a multilevel list: top-level sections at
> level 1, *Related Work* and *Problem Statements* at level 2). The numbers
> typed below exist so the repo copy is readable and checkable — so when you
> move the text into Word, do not end up with both sets.
>
> The reliable route, and the one most teams should use: **open the course
> template and paste your prose section by section**, leaving Word's own
> numbering to do the numbering. Ten minutes, no surprises.
>
> If you prefer to convert, `pandoc` can do it (install with
> `winget install pandoc`):
>
>     pandoc proposal/proposal.md -o proposal.docx --reference-doc="CPSC 490 Project Proposal Template Fall 2026.docx"
>
> Then in Word: delete the typed `0.` / `1.` / `1.1` prefixes (Word re-adds
> them from the list), and set *Related Work* and *Problem Statements* to the
> template's level-2 heading so they number as 1.1 and 1.2. Check figure
> placement, then submit.
>
> Either way, keep this Markdown copy current — it is what peer review and CI
> can actually read. If your team writes in Word instead, commit the `.docx`
> here as well.

---

## 0. Abstract

The Internet of Things (IoT) connects physical devices to computing systems, allowing them to exchange data and communicate through networks. Recording devices and network-connected cameras are commonly found in everyday environments, and their presence keeps growing, from home security cameras to Flock cameras. Devices such as Ring cameras, Meta glasses, body cameras, and spy cameras can record people without them knowing, which makes it harder for people to know where their privacy may be affected. These devices emit signals that may be observed and may provide information about their activity and location. By observing and understanding these signals, individuals can better understand how everyday IoT devices communicate and become more aware of the devices operating around them.

The problem this project addresses is the difficulty of identifying and understanding nearby network-connected devices in real time. There are existing tools that can detect network devices already, but the information provided by these tools does not give the user a good understanding of what devices are present and where they are located. Our project, Distributed Signal Capture for Multi-Node Analysis, proposes a system that helps people understand where their privacy may be affected by showing them which recording and network-connected devices are around them and approximately where those devices are. In this project, each IoT device in range is treated as a node. As a user enters an area, the system captures the signals of every device within range and sends the signal metadata to a backend for analysis, such as device fingerprinting, which tells devices apart based on their observable traits. The software is meant to run on a laptop or on a smaller device such as a Raspberry Pi.

This system will be able to map device presence in real time and pick out a small set of known devices: Meta glasses, Ring cameras, body cameras, and spy cameras. Although there are already tools available such as Kismet that provide network monitoring, our project will also investigate whether a device's signal metadata can show if it is actively recording nearby. The info this project provides will be shown through a user-friendly dashboard that shows detected devices and their approximate location, so the processed information is easier for the user to understand. Building this is non-trivial because it combines wireless protocol fundamentals (Wi-Fi, Bluetooth), device fingerprinting, and multi-node data analysis in one system. This will allow users to be more aware of the network-connected devices operating around them.

-〈Goals and outcomes: fill in once §2 Goals and Objectives is written. Summarize the 2–3 goals and what will exist at the end of the project.〉The statement *below* will need to be **lined up with §2** once it is complete!

By the end of this project, we will have software that runs on a laptop or a Raspberry Pi and can capture signals from different devices within range. Backend services will collect and analyze the signal metadata from each node to fingerprint and identify the devices, and a frontend dashboard will reveal detected devices and their approximate locations in real time. The frontend will also show whether a device is actively recording, if that proves possible. This semester (Fall 2026) focuses on the proposal and planning phase of the project, including a working prototype. The full implementation will come next semester in CPSC 491. In the future, this project could evolve into a more complete signal analysis platform that can detect even more types of monitoring devices.

The rest of this proposal covers the background, related work, and problem statement (§1), our goals and objectives (§2), the proposed approaches (§3), the required environment, resources, and planned activities (§4), the expected outcomes and timeline (§5–§6), and our AI usage and references (§7–§8).


## 1. Introduction

  The Internet of Things (IoT) connects physical devices to computing systems through which they can exchange data. In this project, the devices of interest include network-connected cameras and wearable recording devices, such as Ring cameras, Meta glasses, and body cameras. Being able to understand the presence of such devices involves both signal capture and data analysis. This will include observing signals emitted by devices within range and interpreting those observations to be able to develop a useful picture of the surrounding environment. This projects main goal is **privacy awareness**, helping individuals map which devices are present and what their observable activity may reveal.

  Our project, *Distributed Signal Capture for Multi-Node Analysis*, aims to map device presence in real time by capturing signals from devices within range as a user enters an area. Our software is intended to operate on either a labtop or a smaller computing platform, such as Raspberry Pi. Backend services will collect signal metadata from each node for analysis, including device fingerprinting to distinguish devices based on their observable traits. A frontend dashboard will present detected devices amd their approximate locations, giving users a spatial view of device presence.

  Our project combines distributed signal collection, metadata analysis, and real-time visualization within a single system. We also intend to investigate whether observable metadata can indicate if a device is actively recording. We intend to have a accessible user-friendly dashboard that translates signal metadata into understandable information about nearby devices in real-time.

  This problem matters because recording devices now capture people who never agreed to be recorded and often cannot tell that they are being recorded. Doorbell cameras record sidewalks and neighbors' doorsteps, smart glasses can record with only a small indicator light to signal it, and body cameras record everyone their wearer interacts with. The people most affected are bystanders rather than device owners. They include guests in short-term rentals, where hidden cameras have been reported; participants in meetings, classes, or interviews where a wearable device may be recording; and residents of shared spaces such as apartments and dormitories. For these people the harm is not only being recorded, but that footage may be stored, uploaded, or shared without their knowledge. At present they have no practical way to check what is recording around them, and the tools that do exist assume technical expertise most of them do not have.

  What makes our project different than others which are similar is that ours focuses on the bystander. Wireless monitoring tools such as Kismet [1] report and track the networks and devices in range, but they assume a technical user will inspect the data. Our system narrows the scope down to recording devices, allowing for more accurate fingerprinting and location tracking. This is combined with a user interface that someone non-technical can read and understand. Additionally, we will investigate whether the signal metadata can show that a device is actively recording, so users don't just know if a camera is nearby, but if it's live and capturing their actions.



### 1.1 Related Work

| Existing approach | What it does | Pros | Cons | Why ours differs |
|---|---|---|---|---|
| Kismet [1] | An open-source wireless monitoring tool & sniffer. It can capture packets for a multitude of wireless specifications including Wi-Fi, Bluetooth, BTLE, and more. Essentially it passively captures packets from different sources and logs info such as packets, devices, location, and other runtime data to a SQLite-based DB. It also includes MAC lookups for different manufacturers. Uses GPS to determine location through a running average of positions where the device was seen. | In-depth and trusted software which has been around for a long time. It has lots of features other than detection, such as alerting for intrusion detection. It includes remote capture programs which can run on small devices, which could be used to track rooms all the time, increasing security. | It is designed for security professionals and network admins, so the data it does log can be hard for a non-technical user to understand. Does not include recording detection or classify devices by type. | Our program will differ from Kismet by using a simplified approach. We will only be looking for surveillance devices. This makes the log data easier to read and sort, and also allows us to search for specific activities such as recording, which Kismet doesn't focus on. Our project will also focus on a more user-friendly dashboard that anyone could read, rather than the packet capture user interface Kismet has. Lastly, Kismet uses GPS to track where a device was last seen, not necessarily where the device actually is. Our project focuses on estimating how close the device is to the user. |
| Lumos [2] | A research system that lets a person walking into an unfamiliar place, like an Airbnb, find and identify hidden Wi-Fi IoT devices using their own device. It also utilizes augmented reality (AR) to show where these devices might be. It is meant to combat hidden devices used to spy on guests, for example hidden cameras. To do this, it has three different modules. The first is the fingerprinting module, which predicts the device type. The second is channel sensing, which learns each device's transmission pattern to decide which Wi-Fi channel to listen on. The third is localization, which is used to log the device location by having the user walk around the room.  | This project is very similar to ours, which is a pro as we can take inspiration from it, especially for how to fingerprint device types. It also has a solid location module, and combined with AR gives the user a great understanding of where hidden IoT devices might be. | The software is Wi-Fi only, so devices that are wired or Bluetooth wouldn't be scanned. Furthermore, MAC address randomization [3] could stop the program from correctly identifying the type of device. Additionally, it can only identify devices similar to ones in its training data. | Unlike Lumos, our project assumes that the user has access to the router (at least for testing). This allows for our project to more accurately identify devices and whether they may be recording, although it comes with the caveat that you have to actually have access to the router. Additionally, our project will be searching not only for Wi-Fi devices, but for Bluetooth ones as well, since many spy cameras, such as Meta glasses, don't need to connect to Wi-Fi. |
| SnoopDog [4] | A framework that detects whether hidden Wi-Fi sensors such as cameras, microphones, motion sensors, etc. are actively monitoring the user, not just present. It can identify and locate where this device is. To determine whether a device is watching you, SnoopDog compares a trusted sensor on your phone with the Wi-Fi traffic of all nearby devices. By doing this, it can determine whether the user's movement changes the Wi-Fi traffic of nearby devices (which works well for cameras). If a camera is recording, the user moving will cause a spike in its traffic, and this can be used to both determine it's recording and determine its approximate location. | Analyzing other devices for spikes in traffic is a great idea for camera detection, and the paper reports a detection rate of 95.2%. The location detection capability is also great, since it can use the network traffic to determine which part of the room the camera is watching. This gives the user a great approximate location of the camera, although not exact. | This framework is great, although just like Lumos, it is Wi-Fi only, so it can't detect devices connected through Bluetooth. Additionally, an attacker could use MAC randomization, broadcast delay, or simply add fake cover traffic to avoid detection. This project is not passive either; the user has to move around and do active trials the software gives to determine device locations. | As stated previously, our project plans to not only scan Wi-Fi, but also search for Bluetooth devices, specifically Meta glasses. Our project plans to be more passive than this one too, so device info can be found by walking into a room. Our project also plans to have access to the router so we can more easily identify devices. |
| flock-you [5] | This is an open-source project which utilizes an ESP32 microcontroller to passively detect Flock cameras nearby. It uses Wi-Fi detection on a 2.4 GHz band to watch data frames for MAC addresses whose OUI matches Flock-related prefixes. It uses Flock cameras' wildcard probe requests to identify them. It also uses Bluetooth to identify Flock cameras in case Wi-Fi detection fails. While driving, this device will play beep sounds to inform the driver of nearby cameras. There are also different beep sounds depending on the confidence level of the device, which is a great idea and something our project could build from. A Flask dashboard shows detections live. For location detection, the software doesn't estimate the camera's location, but rather where the detector was when it heard the camera. This essentially provides the user a list of where these cameras may be for future drives. | The software has many great features, especially the audio feedback from the microcontroller. This makes it especially useful for driving, when you can't look at a dashboard. Our project could build on this idea by using sounds to inform the user of the number of devices nearby. This project also uses confidence tiers, which is another great form of feedback for the user. Along with this, utilizing Wi-Fi and Bluetooth gives the program more chances to find a nearby camera. | The program is built specifically for Flock cameras, so other recording devices aren't located or shown. Additionally, the software doesn't have location detection of the cameras, just whether they may be nearby. The software also doesn't detect whether the Flock camera is actively capturing or not. | Our project differs in that we aren't just detecting Flock cameras; we will be detecting many types of spy cameras and monitoring devices. Our project also plans to map the location of these devices and whether they may be recording, unlike this project. This project is less generalized than ours, which makes it great for Flock cameras, but we plan to extend this capability to give the user more insight on what may be recording them. |

Each of these projects contributes to part of what our project will do. To start with Kismet, its trusted status and in-depth software will be great for us to reference. The problem is that it is designed for professionals and network admins, so we will take that and interpret the data in a way non-technical users can understand. Lumos and SnoopDog are both similar to our project, and much can be learned from them. The fingerprinting ability of Lumos can prove useful for us in identifying device types, and the network traffic sensing which SnoopDog provides will be useful for detecting if a camera is actively recording. However, both projects focus on Wi-Fi only, so we plan to expand this to Bluetooth. SnoopDog also requires the user to move around and do active trials, while we plan to be more passive in our detection. Finally, the flock-you project is great since it utilizes both Wi-Fi and Bluetooth and gives the user great feedback with its sounds and confidence ratings. It only scans for Flock cameras, however, so we can plan on expanding beyond Flock cameras. Our project will take inspiration from all these projects by scanning both Wi-Fi and Bluetooth for many types of spy cameras and monitoring devices, estimating device distances, and detecting whether they may be recording. All this info will be displayed on a user-friendly dashboard that anyone could read.

### 1.2 Problem Statements

> Briefly state the problem to solve in this project.

〈Your problem statement(s), **concise** — a few sentences each, no
background (that was §1) and no solution (that is §3). Number them P1, P2, …
so later sections can refer back.〉

**Every problem here must connect to the goals and objectives in §2, and
every goal in §2 must trace back to a problem here.** A goal with no problem
behind it is scope you invented; a problem with no goal is a problem you are
not actually solving. Check both directions before you submit — this mapping
is what the final project report is graded against.

| Problem | Addressed by |
|---|---|
| P1 〈one line〉 | 〈Goal 1 (#n)〉 |
| P2 〈one line〉 | 〈Goal 2 (#n)〉 |

## 2. Goals and Objectives

> Describe goals and objectives. Goals are general statements of what you are
> trying to accomplish with the project or problems to solve. Objectives are
> specific, measurable statements of what you want to complete to reach the
> project goals. Most projects have 2-3 goals.
>
> List the objectives for each goal. To write objectives, look at the goal
> statement and list what you need to complete using action words like use
> case names in order to meet the goal.
>
> Note that the goals and objectives in a proposal will be an important
> metric to evaluate whether or not you successfully finished your project
> when you turn in your final project report.

Each **goal** is tracked as an **Epic** issue and each **objective** as a
**User Story** issue in the team repository (see the setup guide's *Epics and user stories* section).
**Every epic and user story in the repository is linked from this section** —
CI gate G8 fails if one exists that this section does not link. That is what
keeps the goals in this document and the work on the board from drifting
apart.

Write each objective the way the guidance above asks — **an action word plus
the measure that says it is done**, not a role-play sentence:

- **Goal 1: 〈e.g. Secure account management〉** (Epic #〈n〉)
  - Objective 1.1: 〈Implement member registration and login with hashed
    credentials, session expiry, and rejection of malformed input.〉 (#〈n〉)
  - Objective 1.2: 〈Demonstrate the login round-trip in a runnable prototype
    at the Week-8 in-class check.〉 (#〈n〉)
- **Goal 2: 〈your second goal〉** (Epic #〈n〉)
  - Objective 2.1: 〈Action word + what you will complete + how it will be
    measured〉 (#〈n〉)

〈Replace the brackets with your own 2–3 goals and their objectives, and put
the **real issue numbers** in as you file them — gate G8 checks that every
epic and story in your repository is linked from this section. A fully worked
version of this, with live issues and a populated board, is in the course
example repository.〉

## 3. Proposed Approaches

> Describe your proposed approach to solve the problem, specifying how you
> will achieve the stated goals. List some possible strategies.

〈Your approach — **clear and concise**. State the strategy you chose, the
alternatives you considered, and the reasoning that decided between them.
Think of this as the argument, not the manual: a reader should finish this
section understanding *what* you will do and *why that* rather than the
alternatives.〉

**Keep the details out of this section.** Tooling, platforms, frameworks,
DBMS choices, environment setup, diagrams, and the work breakdown all belong
in §4 (Required Environment, Resources, and Planned Activities). If a
sentence here names a version number, a library, or a configuration, it
probably belongs in §4 — leave a pointer instead ("the implementation stack
is detailed in §4").

〈A few paragraphs, or a short list of candidate strategies with one line of
trade-off each. If it runs past a page, you are writing §4.〉

## 4. Required Environment, Resources, and Planned Activities

> Review the required and available resources and environment to complete
> your project. For example, server, platform, software tools, operating
> systems, DBMS, or any required skills.
>
> Describe the expected activities to achieve the stated goals, e.g.,
> software development process.

〈Your environment, resources, and planned activities.〉

**Diagrams belong in this section.** Include at minimum a high-level
architecture diagram and a system (context) diagram; add the ER/EER model and
a data-flow diagram where they help the reader understand what you are
building and what it depends on. Draw them with any graphical tool
(Lucidchart, draw.io, Miro, Mermaid, ERDPlus, Figma), keep the authoritative
copies in `docs/design/` with both editable source and exported image, and
reference them here.

〈Number every figure, caption it, and point at it from the prose — "Figure 1
shows the three deployment tiers and the trust boundary between them." A
figure the text never mentions is decoration. See `docs/design/DIAGRAMS.md`
for tools, conventions, and the rule that every box and arrow must be
verified against reality.〉

### Specification and design documents

**Every specification and design document the team writes is listed here**
with the objective it serves. This section is the index of the project's
technical detail: §3 holds the argument, §4 holds the documents that make it
buildable. CI gate G9 fails if a document exists in `docs/specs/` or
`docs/design/` that this section does not link.

| Document | Kind | Covers | Issues |
|---|---|---|---|
| 〈docs/specs/account-management.md〉 | specification | 〈account management requirements〉 | 〈#n, #n〉 |
| 〈docs/design/architecture.md〉 | design | 〈system architecture + data model〉 | 〈#n〉 |

〈The scaffold ships `docs/specs/example-spec.md` and
`docs/design/example-design.md` as worked examples — read them, then delete
them once you have your own, and list yours here.〉

〈Replace these rows with your own. Each document names its epic and stories
in its own first lines too (gate G2), so the trail runs both ways.〉

### Planned activities — the work items

The goals and objectives live in §2 as epics and user stories. **This section
links every *other* work item: features, enhancements, bugs, tasks, and
sub-tasks** — the concrete activities that deliver those objectives. CI gate
G8 fails if such an issue exists that this section does not link.

| Issue | Type | Activity | Parent | Owner | Sprint |
|---|---|---|---|---|---|
| 〈#n〉 | 〈task〉 | 〈stand up the prototype login endpoint〉 | 〈#story〉 | 〈owner〉 | 〈Sprint 1〉 |
| 〈#n〉 | 〈feature/enhancement/bug/task/sub-task〉 | 〈…〉 | 〈#story〉 | 〈…〉 | 〈…〉 |

〈Replace these rows with your own, and keep the table current as you file new
issues — with §2 it gives a reader every planned activity in one place, each
traceable to the objective it serves.〉

## 5. Project Outcomes

> Describe the outcomes or deliverables, e.g., final project report, user
> manuals, source code, data or database files, etc.
>
> Note: the deliverables always include the team GitHub repository, which
> must already contain prototype v0 (a thin end-to-end proof-of-concept,
> however small, running when this proposal is submitted). Briefly describe
> what your v0 demonstrates and how to run it.

〈**One or two paragraphs** explaining the project outcome overall — what will
exist when the project is finished, and what it will let someone do. Keep it
prose, not a checklist; name the deliverables inside the paragraphs, and say
briefly what prototype v0 demonstrates today and how to run it.〉

## 6. Project Timeline

> Identifies tasks (project objectives) to be performed, milestones to be
> met, and the estimated number of hours for each task.

〈**This is the plan for CPSC 491 next semester — the implementation timeline,
not this semester's proposal work.** Identify the tasks (your objectives from
§2), the milestones, and the estimated hours for each, in the order they will
be built. State the assumptions it rests on (sponsor availability, data
access, hardware).〉

| Task (objective) | Milestone | Owner | Est. hours | Spring phase |
|---|---|---|---|---|
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |

〈Do **not** put this fall's four proposal sprints here — those live on the
project board and in `docs/sprint-reviews/`. This section answers "how does
the system actually get built next semester?"〉

## 7. AI Usage

> Per the course AI policy (see the syllabus, Use of AI Tools), disclose the
> AI tools used in preparing this proposal and the prototype: which tools,
> for what tasks (e.g., code generation, test writing, debugging,
> diagramming), and approximately what fraction of each artifact was
> AI-assisted.
>
> Reminder: the prose of this proposal must be your own writing. You remain
> fully responsible for the correctness of all AI-assisted work, including
> the prototype code.

〈Your disclosure. Naming the tool is not disclosure — name what it drafted,
what fraction of each artifact was AI-assisted, and how you verified it.〉

## 8. References

> [1] Burges, C. J. C. Tutorial on Support Vector Machines for Pattern
> Recognition. Kluwer Academic Publishers, 1998.
> [2] Chen, P., Fan, R., and Lin, C. A study on SMO-type decomposition
> methods for support vector machines. IEEE Transactions on Neural Networks,
> 2006.
> [3] For Wikipedia, specify the URL here
> [4] For a web source, specify the URL here plus date accessed

[1] Kismet Wireless, "Kismet." Accessed: Oct. 9, 2026. [Online]. Available: https://www.kismetwireless.net/

[2] R. A. Sharma, E. Soltanaghaei, A. Rowe, and V. Sekar, "Lumos: Identifying and localizing diverse hidden IoT devices in an unfamiliar environment," in *Proc. 31st USENIX Security Symp. (USENIX Security 22)*, Boston, MA, USA, Aug. 2022, pp. 1095–1112.

[3] M. Vanhoef, C. Matte, M. Cunche, L. S. Cardoso, and F. Piessens, "Why MAC address randomization is not enough: An analysis of Wi-Fi network discovery mechanisms," in *Proc. 11th ACM Asia Conf. Comput. Commun. Secur. (ASIA CCS '16)*, Xi'an, China, May 2016, pp. 413–424, doi: 10.1145/2897845.2897883.

[4] A. D. Singh, L. Garcia, J. Noor, and M. Srivastava, "I always feel like somebody's sensing me! A framework to detect, identify, and localize clandestine wireless sensors," in *Proc. 30th USENIX Security Symp. (USENIX Security 21)*, Aug. 2021, pp. 1829–1846.

[5] Colonel Panic, "flock-you: Flock cam detection," GitHub repository. Accessed: Oct. 9, 2026. [Online]. Available: https://github.com/colonelpanichacks/flock-you


