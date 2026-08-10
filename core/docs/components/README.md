# Component Documentation — `core/docs/components/`

This directory holds **one subfolder per Android IVI software component** registered
with Autodev. Each subfolder contains structured documentation that BugAnalyst reads
automatically before querying SharePoint, giving it precise local context for root
cause analysis.

---

## Directory Structure

```
core/docs/components/
├── README.md                          ← this file
├── dtv-service/
│   ├── component-info.md              ← component identity, architecture, interfaces, logging
│   └── component-flow.md              ← ASCII layer diagram + interface annotations
├── media-input-service/
│   ├── component-info.md
│   └── component-flow.md
├── audio-hal/
│   ├── component-info.md
│   └── component-flow.md
└── ...
```

Each folder name is the component name in **kebab-case lowercase**
(e.g. "DTV Service" → `dtv-service`, "Audio HAL" → `audio-hal`).

---

## How to Add a New Component

**Open Copilot Chat → select the `ComponentSetup` agent → type `start`.**

The agent will interview you in 5 phases:

| Phase | What it collects |
|-------|-----------------|
| 1 — Basics | Component name, IVI domain, JIRA tag, owner, safety relevance |
| 2 — Flow | Layer-by-layer breakdown (e.g. HMI → DTV Service → DTV HAL → Kernel) with source path, logcat tag, and description per layer |
| 3 — Interfaces | Interface type, name, and description for every adjacent layer boundary |
| 4 — Operations | Gerrit URL, Android target version, SharePoint folder, error handling, known issues |
| 5 — Approval | Summary table → confirmation → file generation |

No terminal commands or scripts needed. Everything happens in chat.

---

## How Agents Use These Files

### BugAnalyst
Before querying SharePoint, BugAnalyst checks this directory for a folder matching
the JIRA ticket's component tag. If found, it reads both files first:

1. `component-info.md` — provides architecture context, logcat tags, error handling
   strategy, and known issues that directly inform root cause hypotheses.
2. `component-flow.md` — provides the layer diagram and interface map to identify
   which layer boundary a bug most likely occurred at.

If SharePoint returns additional documents, they supplement (not replace) the local
component docs.

### FixGenerator
Uses `component-info.md` to confirm the correct source paths, language, and
interface contracts before writing a fix plan.

---

## Supported IVI Domains

| Domain | Examples |
|--------|---------|
| DTV | Digital TV tuner, DTV service, DTV HAL |
| MIS | Media Input Service, media session management |
| Audio | Audio HAL, AudioFlinger interaction, CarAudioService |
| Navigation | Navigation service, GNSS HAL |
| Climate | Climate control service, HVAC VHAL properties |
| VHAL | VehicleHAL, CarPropertyManager, CAN gateway |
| Diagnosis | OBD-II bridge, diagnostic manager, UDS service |
| Phone & BT | Bluetooth telephony, HFP, BLE services |
| Display | SurfaceFlinger, Presentation, secondary display |
| System | Watchdog, init, boot, CarService |
| Other | Specify during ComponentSetup |

---

## Updating an Existing Component

Either:
- **Edit manually** — open `core/docs/components/<slug>/component-info.md` and update.
- **Re-run ComponentSetup** — the agent will warn about the existing folder and ask
  for confirmation before overwriting.

---

## File Naming Convention

| File | Contents |
|------|---------|
| `component-info.md` | Structured info sheet: identity, purpose, architecture, interfaces, error handling, testing, known issues, related documents |
| `component-flow.md` | ASCII layer diagram with interface annotations, logcat tag table, and full-stack capture command |
