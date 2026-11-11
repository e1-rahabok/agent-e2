# Flows: health checks, troubleshooting, decision trees

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

- Location: [placement.md](placement.md), placement rules.
- Vocabulary:
  - Framework: how IT operations are managed (SP5). `sp5-framework/concepts/overview`.
  - Model: how one pillar of one object is quantified into a number and a decision (capacity model, availability model, security model). Files in `vsphere/object-types/<object>/models/` and `sp5-framework/capacity/`.
  - KPI: a model of performance only (the P in KPI). Files in `vsphere/object-types/<object>/kpis/`, plus `guest-os/system/metrics/guest-os-performance`.
  - Health check: the what. Is the object healthy, at risk, or wasteful? Always on one object type (VM, host, cluster, datastore), never on a technology (CPU, memory) and never on one pillar (author, 2026-11-11). A parent's health includes its children's, unless a realm separates them: Guest OS slowness is not ESXi or VM health, because the hypervisor neither sees nor controls it. Its order of checks is below; the health grouping (present health, risk, efficiency) defines the verdicts, not the order (`sp5-framework/concepts/health-risk-efficiency`). Monitoring belongs here. Explained to the agent in `sp5-framework/concepts/health-check`.
  - Troubleshooting: the why, in the reactive process. It starts from a complaint, an alert, or a failed health check step. Two types only: down (availability) and slow (performance). A security breach gets a forensic investigation, not troubleshooting. Each type uses the same order of checks as its pillar in the health check.
  - Two processes: reactive (troubleshooting, forensic investigation) and proactive (the health check, daily, with weekly and monthly analysis). The health check is a superset of reactive, because nobody knows yet whether there is a problem. Proactive findings arrive as insight, typically anomaly detection read with business context.
  - Decision tree: answers one operational question (can this cluster take more VMs, should this VM be downsized) and ends in a choice to act, with its reason. Not a health check, even when a health check step reads its result. Not a decision record: a decision records what was done; a decision tree decides what to do.
  - Most operational questions are neither a health check nor troubleshooting. A flow for one is a decision tree; a question answered by reading, not by a branching order of checks, is a concept or metric file.
  - Not used: diagnosis (troubleshooting), what to monitor (health check), verification (health check).
- A health check step names the KPI or model, its band, and the flow to open when it fails: `→ <troubleshooting id>`.
- Order: is it up (availability: log, saturation, configuration, known bug), is it fast (performance: contention, consumption, configuration, known bug, log), is it secure (security: configuration, known bug, log), will it be enough (capacity: consumption, configuration, contention, inventory). Within each pillar the what comes before the why: establish the fact, then explain it; do not jump to a conclusion. Known bugs are checked per pillar, because a bug can cause an outage, slowness or a security loophole. Efficiency is part of capacity. Contention is part of performance. Every performance troubleshooting flow checks configuration.
- The health check reads VCF Operations KPIs and models. It does not fall back to vSphere alone: VCF always includes VCF Operations, and other health check tools are outside the scope of Agent E2.
- One flow per file. Template: `project/templates/health-check.md`, `troubleshooting.md` or `decision-tree.md`. Order: purpose (health check: nothing is wrong yet, so no symptom), symptom (troubleshooting) or question (decision tree), Mermaid flowchart, numbered steps (`## Checks, in order`), why this order, how to read the result, traps, metadata.
- The numbered steps are what the LLM follows. The Mermaid chart is a second, text-readable view; GitHub renders it for review.
- Each step states: the metric (exact name, matching the metric file title), the object, the threshold with its source, and the next step for each outcome.
  - Example: 1. Check VM CPU Ready (VirtualMachine). Above <threshold> (<source>) → step 2. Otherwise → step 4.
- Every metric or flow named in a step is linked in `internal_derive`, so retrieval brings in the files with the flow.
- Mermaid node text repeats the step number: `S1[1. VM CPU Ready above threshold?]`. Step numbers tie the chart to the text.
- Keep each flowchart to about 15 nodes. Split a larger flow into linked flow files.
- draw.io files are not read by the LLM: the XML is mostly layout and style, and compressed files are unreadable.
  - Keep the `.drawio` file and an exported `.png` in the `images/` folder next to the flow as the editable source.
  - Link the `.png` under the flowchart and tag it in `images` (`image_type: diagram`).
  - The Mermaid chart and numbered steps are the content the LLM uses.
