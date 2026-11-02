# Evaluation

This folder contains **golden evaluation cases** used to measure and improve the quality of the AI system.

## Purpose

Golden cases serve two critical roles:

1. **Measurement** — They let us objectively test whether changes to the knowledge base, chunking, retrieval, or prompts actually improve answers.
2. **Teaching signal** — High-quality examples help shape the style, depth, and reasoning pattern we want from the AI.

We deliberately support more than clean text questions. Real vSphere admins often submit screenshots, diagrams, log fragments, or files and simply say “Explain the problem and why I have it.”

## Case Types

| Type | Description |
|------|-------------|
| `text` | Classic question → expected answer |
| `screenshot` | Image + short prompt (e.g. “What’s wrong?”) |
| `diagram` | Architecture or flow diagram + question |
| `log` | Log excerpt or error dump + question |
| `mixed` | Combination of the above |

## File Format

Each golden case is a Markdown file. See the template in `_templates/golden-case.md`.

Recommended naming:

```text
evaluation/
├── vsphere/
│   ├── cpu/
│   ├── memory/
│   ├── storage/
│   ├── network/
│   └── general/
└── _templates/
    └── golden-case.md
```
