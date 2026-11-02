# Isvara-2 — vSphere Knowledge Base for AI

This repository contains deep, structured vSphere knowledge designed to power a high-quality RAG AI assistant.

The primary goal is **mastery and real understanding**, not just a dictionary of metrics.

---

## Core Philosophy

Performance counters are a **byproduct** of understanding how vSphere actually works.

True expertise requires internalizing:
- The nature of metrics themselves
- The difference between the VM (virtual motherboard) and the Guest OS
- Resource management mechanisms
- Architectural realities of each resource area

Only then do the individual counters become meaningful.

---

## Repository Structure

```text
knowledge/
├── raw-input/                      # Original source materials (Word, drawio, PPT, PDF)
├── _templates/
├── vsphere/
│   ├── foundations/                 # Cross-cutting deep knowledge
│   │   ├── metrics-philosophy/      # What metrics really are, nuances, industry problems
│   │   ├── vm-vs-guest-os/          # Virtual motherboard vs Guest OS
│   │   ├── overhead-and-buffers/    # Overhead concepts and different types of buffers
│   │   └── observability-principles/
│   ├── cpu/
│   │   ├── architecture/
│   │   ├── resource-management/
│   │   ├── counters/
│   │   │   ├── host/
│   │   │   └── vm/
│   │   └── interpretation/
│   ├── memory/
│   ├── storage/
│   ├── network/
│   ├── troubleshooting/
│   ├── glossary/
│   └── README.md
├── nsx/                            # Future
└── vsan/                           # Future
```

---

## Layer Responsibilities

| Layer | Purpose |
|-------|--------|
| `foundations/` | Deep, cross-cutting mental models. How to *think* about metrics and virtualization. |
| `cpu/`, `memory/`, etc. | Resource-specific architecture, mechanisms, counters, and interpretation. |
| `counters/host/` vs `counters/vm/` | Never mix perspectives. Same counter name can mean different things. |
| `raw-input/` | Original source documents (your book, diagrams, decks). |

---

## Current Focus

1. Build out `foundations/` from Chapter 1 of the metrics book.
2. Then deepen the CPU area as the first full resource example.
