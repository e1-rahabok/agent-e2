# Isvara-2 Knowledge Base

Structured knowledge base for VMware Cloud Foundation / vSphere / NSX / vSAN AI agent.

This repository holds clean, structured domain knowledge that will be used by a Retrieval-Augmented Generation (RAG) system. The goal is high-quality, grounded answers with minimal hallucination.

## Design Principles

- **Same structure for every component** (vSphere, NSX, vSAN, Aria, etc.)
- Only the *content* changes between components
- Templates live in `knowledge/_templates/`
- Real content lives under `knowledge/<component>/`
- Evaluation questions live in `evaluation/`

## Current Focus

**vSphere** first.

## Directory Overview

```text
knowledge/
├── _templates/               # Reusable templates (do not put real content here)
├── vsphere/                 # Start filling content here
│   ├── troubleshooting/
│   ├── errors/
│   ├── config-parameters/
│   ├── metrics/
│   ├── glossary/
│   └── README.md
├── nsx/                     # Future
├── vsan/                    # Future
└── ...
evaluation/
└── vsphere-golden-questions.md
metadata/
└── schema.md
```

## How to contribute content

1. Copy the relevant template from `knowledge/_templates/`
2. Fill it with accurate vSphere knowledge
3. Place the completed file in the correct folder under `knowledge/vsphere/`
4. Keep filenames descriptive and consistent (e.g. `esxi-host-not-responding.md`)

## Priority order for vSphere content

1. Troubleshooting flows (highest impact)
2. Error / event / log catalog
3. Configuration parameter reference
4. Key metrics
5. Glossary of precise terms
