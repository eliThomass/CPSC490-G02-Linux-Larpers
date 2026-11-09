# Design — High-level architecture

> Epic: #47, #50, #56 · Stories: #16, #48, #57
> Task: #84 · Owner: Jonathan Soo · Sprint: 2 · Status: draft

This document answers one question: what are the major pieces of the
system, and how do they connect? The data model is in the ER diagram
(#82) and the step-by-step movement of data is in the data flow diagram
(#77); neither is repeated here. See [`DIAGRAMS.md`](DIAGRAMS.md) for the
conventions this diagram follows.

## 1. Architecture

![High-level architecture: ESP32 capture nodes pick up Wi-Fi and Bluetooth
signals from nearby recording devices and send observations to a FastAPI
backend, which reads and writes PostgreSQL on the same server; the dashboard
requests observations from the API and shows nearby devices to the
user](diagrams/architecture.drawio.png)

*Figure 1 — High-level architecture. The dashed outline is everything the
team builds; the solid box is the proposed server. Labels in brackets give
the technology, and TBD marks what is not decided yet. Editable source:
[`diagrams/architecture.drawio.svg`](diagrams/architecture.drawio.svg).*

## 2. Components

| Component | Responsibility | Technology | Status |
|---|---|---|---|
| Recording devices | Emit Wi-Fi and Bluetooth signals (Meta glasses, Ring, body cameras) | — | external, not built by us |
| ESP32 capture node (×N) | Scans Wi-Fi and Bluetooth and sends observations to the backend | C/C++ firmware on ESP32 | decided (#79) |
| Backend API | Ingests, stores and serves observations | FastAPI | decided (#79) |
| Database | Holds observations and devices | PostgreSQL | decided (#79) |
| Dashboard | Shows nearby devices to the user | framework TBD (Angular suggested) | open (#79) |
| User | A person entering the space | — | external |

## 3. Connections

| From | To | What flows | How |
|---|---|---|---|
| Recording devices | ESP32 capture node | Wi-Fi and BLE signals | passive capture |
| ESP32 capture node | Backend API | Observations | protocol TBD |
| Backend API | Database | Reads and writes observations | SQL |
| Dashboard | Backend API | Requests observations | HTTP(S), JSON |
| Dashboard | User | Nearby devices | on screen |

## 4. Deployment

The Backend API and the Database run together on one server, so the API
reaches PostgreSQL directly. The proposed host is **AWS Lightsail**, pending
sponsor approval; proposal §4 carries the suggestion. During development,
teammates reach the server from their own machines through **SSH tunnels**.

## 5. What is NOT designed yet

- The protocol between the capture nodes and the API.
- How observations from several nodes are correlated with each other.
- The dashboard framework.
- The final host, until the sponsors approve one.
