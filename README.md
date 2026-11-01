# Isvara-2 — vSphere Knowledge Base for AI

This repository contains deep, structured vSphere knowledge designed to power a high-quality RAG AI assistant.

The primary goal is **mastery and real understanding**, not just a dictionary of metrics.

---

## Core Philosophy

Performance counters are a **byproduct** of understanding how vSphere actually works.

Half of true expertise comes from knowing the underlying architecture and resource management mechanisms. Only then do the counters become meaningful.

This repository is organized accordingly:

1. **Architecture** — How the system really works
2. **Resource Management** — The rules and mechanisms
3. **Counters** — Separated by perspective (Host vs VM)
4. **Interpretation** — How experienced admins actually use the information

---

## Repository Structure

```text
knowledge/
├── _templates/
├── vsphere/
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
│   ├── troubleshooting/          # Cross-cutting flows
│   ├── glossary/
│   └── README.md
├── nsx/                         # Future
└── vsan/                        # Future
```

---

## Why this structure?

A veteran vSphere administrator does not think in isolated counter names.  
They think in terms of:

- How the CPU scheduler works
- What Ready Time really means
- How shares, reservations and limits interact
- Why the same counter name means different things on a Host vs a VM

The folder structure reflects that mental model so both humans and the AI can build genuine understanding.

---

## Current Focus

**CPU** is the model area.  
Other resource areas (memory, storage, network) will follow the same pattern.

---

## How to contribute

- Put deep architectural explanations in `architecture/`
- Put mechanisms (shares, limits, scheduling behavior, etc.) in `resource-management/`
- Put individual counters in `counters/host/` or `counters/vm/` — never mix perspectives
- Put real-world diagnostic patterns in `interpretation/`
