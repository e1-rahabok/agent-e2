# Isvara-2 — vSphere Knowledge Base for AI

This repository contains **structured, high-quality vSphere knowledge** intended to power a Retrieval-Augmented Generation (RAG) AI assistant.

The goal is simple: when an admin asks a question, the AI should retrieve accurate, grounded information from this knowledge base instead of guessing.

---

## Design Philosophy

This repository is written for **veteran vSphere administrators** first.

We use normal vSphere language:

- Managed Objects / Object Types
- Properties
- Performance Counters
- Alarms
- Logs
- Faults
- Advanced Settings
- Troubleshooting flows

At the same time, the folder structure is deliberately organized so that a RAG system can retrieve information accurately. This dual purpose is intentional and documented.

---

## Repository Structure

```text
knowledge/
├── _templates/                  # Templates (copy these)
├── vsphere/                     # All vSphere knowledge lives here
│   ├── object-types/            # VirtualMachine, HostSystem, Datastore, etc.
│   ├── properties/              # Important properties of managed objects
│   ├── performance-counters/    # Real performance counters
│   ├── alarms/                  # Alarm definitions and behaviour
│   ├── logs/                    # Important log messages & signatures
│   ├── faults/                  # Faults and error codes
│   ├── advanced-settings/       # Advanced options / settings
│   ├── troubleshooting/         # Decision trees and flows
│   ├── glossary/                # Precise term definitions
│   └── README.md
├── nsx/                         # Future
└── vsan/                        # Future

evaluation/
└── vsphere-golden-questions.md  # Questions used to test the AI
```

---

## Why this structure? (RAG explanation)

A RAG system works by breaking knowledge into searchable pieces (chunks) and retrieving only the most relevant ones for each question.

By separating knowledge into clear vSphere-native categories, we get two benefits:

1. **Admins feel at home** — the folders match how we already think about vSphere.
2. **The AI retrieves better** — it can be guided to look in the right category (e.g. “only search Performance Counters + Alarms”).

This is why we keep a clean separation even though a human could just put everything in one big folder.

---

## How to add knowledge

1. Go to `knowledge/_templates/`
2. Copy the appropriate template
3. Fill it with accurate information
4. Save it in the correct folder under `knowledge/vsphere/`
5. Use clear filenames (example: `host-not-responding.md`, `cpu.usage.average.md`)

---

## Priority order for content

1. Troubleshooting flows (highest practical value)
2. Faults and important log signatures
3. Key Properties and Performance Counters
4. Alarms
5. Advanced Settings
6. Object Types and Glossary

---

## Current Status

Focus is currently on **vSphere** only.  
NSX and vSAN will follow the exact same structure later.
