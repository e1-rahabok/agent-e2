---
id: vendor-neutral-general-001
title: "Hyperscaler cost of 1,000 VMs"
scope: vendor-neutral
area: general
input: text
tests: judgment
knowledge:
  - vsphere/system/concepts/capacity-model
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Cost and Price > Q1 VM Cost"
format: multiple-choice
level: l400
answer: [C]
trap: [A,B]
status: draft
---

## Prompt
Roughly how much would you pay to buy 1,000 VMs from hyperscalers? The VMs average 4 vCPU, 16 GB RAM, 0.5 TB disk, up to 10 Gb network.

Included:
- Support (not on-site).
- Self-service portal to manage the 1,000 VMs.
- Observability.
- Sufficient IP addresses.

Not included:
- Guest OS.
- Security software.

You pay 1 year in advance, for 24/7 use. Roughly, what is the average cost among the top 3 hyperscalers?

A. US$ 1 million per year.
B. US$ 1.5 million per year.
C. US$ 2 million per year.
D. US$ 2.5 million per year.

## Likely wrong answer
A or B (compute list price only, ignoring disk, network, support and management).

## Expected key points
- Answer: C (US$ 2 million per year).
- About US$ 2,000 per VM per year.

## Notes
- The key has no explanation for A, B and D, and no pricing date or source. Tracked in docs/todo.md.
- Prices change. Re-check against current hyperscaler pricing before each evaluation run.
- No knowledge file covers cloud pricing yet; `knowledge` points to the closest file.
