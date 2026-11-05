# Product requirements: the assistant (1.0 and after)

What the shipped system must do for its users. Not indexed.
Inputs: the author's demo video of vCommunity Ask (2026-11-04, 56 s, no audio), the solution design, and the benchmark results.
Related: `solution-design.md` (system design), `design-kb-test-site.md` (test site and benchmark), `harness/README.md` (tools).

## 1. What the demo shows

| Area | Seen in the demo |
|---|---|
| Ask page | Chat. Starter questions. Sources filter (All sources). Enter to send, Shift+Enter for a new line. Streaming answer with a progress line ("Found 16 sources, asking qwen3.8:27b-mlx…"). Stop button. Recent chats, delete chat. Dark mode. |
| Answer | Every fact cited as [n]. Source chips above the answer. Footer: model, time, tokens per second (6.8 s, 81.5 tokens/s), Copy answer. Follow-up questions use 3 earlier turns. |
| Source details | One card per source: title, section, file id, draft badge, snippet, image thumbnails, Open (local viewer), View on GitHub. Linked files listed separately with the link type (linked · same name, linked · internal derive). |
| Knowledge sources | Source plug-in `markdown-repo`: Git repo or mounted folder, include `knowledge/**/*.md`, version = commit SHA, last synced, re-sync every 24 h, 198 documents and 1,095 chunks, Sync now, Re-index all. |
| Settings | Local Ollama URL, chat model (qwen3.8:27b-mlx), embedding model (nomic-embed-text), show thinking, keep model loaded. Chunks to retrieve 8, context budget 24,000 characters, model context 16,384 tokens, temperature 0.2, chat history 3 turns, follow links on. System prompt editable, with reset to default. |
| Admin | API token for changes (kept in the browser). Swagger API docs. Link to observability dashboards. |

### Kept as requirements
- Answer only from the knowledge base. A citation for every fact. Source cards with file id, section and status.
- Linked files shown with their link type. This makes the `same_name` trap guard visible to the user.
- The index version (commit SHA) shown, and stored with every answer.
- Streaming, progress line, Stop.
- Model, time and speed shown per answer.
- A local model through Ollama. No internet needed to answer.

### Gaps against what the benchmark tests

- **Classic retrieval only: 8 chunks + linked files. No catalog facts, calculator, flow executor or answer verifier.**
  - Why it matters: The benchmark scores the harness. An app that rebuilds retrieval on its own is an untested system.
  - Requirement: The app calls `harness/` (library or local API) for retrieval, tools, prompt and verifier. One implementation, tested and shipped.
- **Embedding model nomic-embed-text; the benchmark uses qwen3-embedding-0.6b.**
  - Why it matters: Different embeddings retrieve different files, so the score does not transfer.
  - Requirement: Use the benchmarked embedding model, or benchmark the app's model before release.
- **System prompt and retrieval settings editable in the UI.**
  - Why it matters: An edited prompt is an untested prompt.
  - Requirement: Prompt and settings live in the repo with a version. Each answer stores prompt version, settings, model and index version. A UI edit marks answers as untested.
- **No rating or flag on answers.**
  - Why it matters: Weak answers cannot be fed back into the knowledge base.
  - Requirement: Rate and flag on every answer, with a cause tag (knowledge gap, wrong fact, retrieval miss, model error). Feeds the review queue in `design-kb-test-site.md`.
- **Every answer ends with "all sources are draft".**
  - Why it matters: Release content is all reviewed (D1).
  - Requirement: Answers never mention review status.
- **"View on GitHub" links.**
  - Why it matters: A dark site has no internet.
  - Requirement: The local viewer (Open) is the default. The GitHub link is optional and hidden when offline.
- **Repo sync from GitHub every 24 h.**
  - Why it matters: A dark site cannot pull.
  - Requirement: Also accept an offline bundle (signed archive of `knowledge/` + catalog + index), imported by an admin.

### Answer quality seen in the demo
- Question 1, "most important CPU metrics to monitor on an ESX host": the answer led with esxtop load average (1 or more = overloaded) and PCPU 80% / 90%.
  - The answer was faithful to its source: section "Host CPU monitoring" in [vsphere/foundations/overhead](https://github.com/e1-rahabok/isvara-2/blob/main/knowledge/vsphere/foundations/overhead.md), from Performance Best Practices 9.1.
  - The emphasis is wrong for this knowledge base. Host utilization does not show VM performance; contention across VMs does. Capacity is read from Core and Thread Utilization.
  - Causes: the section sits in the overhead file (a merge artifact), and no overview file answers "what do I monitor on an ESXi host". The top sources were power management and overhead files; the host utilization files (`core-utilization`, `utilization`, `host-consumption-metrics`) were not cited.
  - Fix: tracked in `todo.md`, section Product.
- Question 2, "CPU Ready ms vs %": correct and well cited. The user said they prefer ms. A calculator conversion would have helped (2,000 ms in a 20-second sample = 10% of one vCPU).

## 2. Ways to ask

| # | Mode | Input | What the system does | Release |
|---|---|---|---|---|
| 1 | Text | A typed question | Retrieve, use tools, answer with citations. | 1.0 |
| 2 | Screenshots | 1 or more images: vCenter charts, esxtop, VCF Operations dashboards | Recognize the screen type. Read metric names, values, units, time range and interval. Show what was read for confirmation. Answer from the knowledge base. | 1.1 (knowledge structure prepared in 1.0) |
| 3 | Data files | esxtop batch CSV, vCenter chart export CSV, VCF Operations export, pasted text | Parse with code, not with the model: peak, 95th percentile, time of peak, per object. Feed the exact values to the answer. | 1.2 |
| 4 | Guided troubleshooting | A symptom ("VM is slow") | Run the matching flow one step at a time. Ask for the next value. Show the step ("Step 2 of 6") and the branch taken. | 1.0 (flow tool exists) |
| 5 | Live instance | Connection to VCF Operations | Read metrics for a named object and apply the flows to live values. | After 1.0 |

- Clarifying questions are part of every mode. The system asks when the object (VM, host, cluster), the time window or the product version is unclear, because the same metric name means different things on different objects.

### Screenshot mode requirements
- Several images in one question, compared with each other (before and after, VM and host, two time ranges).
- Recognize the screen against the screenshot library: each library image has alt text and metadata (`image_type`, `metric`, `object`, `product`). Matching tells the system which chart and which counters it is looking at.
- Read the chart interval and rollup (real-time 20 s, 1 Day 5 min, ...). A 1-day chart hides 20-second peaks; say so. See `vsphere/foundations/vcenter-statistics`.
- Show the values it read before reasoning: "I read Ready 12.3% at 10:05 on VM app01. Correct?" A misread number spoils the whole answer.
- Answers can return library images ("this is what the healthy pattern looks like").
- Screenshots hold host names and IP addresses. Keep them local. Set a retention period. Never send them outside the customer site.
- Needs a vision-capable model that passes the screenshot track of the benchmark, or a separate local vision step that turns the image into text.

### Data file mode requirements
- esxtop batch output (`esxtop -b`) is a large CSV with one column per counter per world. Parse by column name with the esxtop field catalog (`knowledge/catalog/esxtop-fields.yaml`).
- Compute statistics in code. The model receives a short table, not the raw file.
- More exact than screenshots and possible on a dark site. Recommended over screenshots when the user can export.

## 3. Answer UX
- Order: direct answer first, then the mechanism and the reason, then what to check next. This matches the top of the 0-3 rubric.
- Name the object for every metric (VM CPU Ready, not CPU Ready). State units and the time interval.
- Thresholds: only with their source (book, vSphere docs, Microsoft). When the book and the docs differ, show both and say which applies.
- Exact values (unit, rollup, statistics level, conversions) come from the catalog and the calculator, and are shown as such.
- Unsure is an answer: "The knowledge base does not settle this. Here is what it does say." Better than a guess.
- Troubleshooting answers show the flow as steps, with the user's values filled in.
- Diagrams: return the author's diagrams from the library when they answer the question.

## 4. Non-functional requirements

| Area | Requirement |
|---|---|
| Dark site | No call outside the customer network to answer, index or update. Offline bundle for updates. |
| Model | Open weights with a commercial licence, vision, at least 32K context, runs on one customer GPU VM (one GPU, at most 96 GB). Chosen by the benchmark (`benchmark/models.md`). |
| Reproducibility | Every answer stores: question, answer, cited ids, tool trace, index version, prompt version, model, settings. |
| Accuracy | Release gate: Stable correct at or above the target in `benchmark/test-design.md`, section 1, on the shipped configuration. |
| Speed | Demo baseline: 6.8 s for a full answer at 81.5 tokens/s (classic mode, local Mac). Agentic mode makes several model calls; measure before setting a target. |
| Users and access | Single user for the demo. Enterprise: SSO, roles (user, admin), audit log. Admin API token not stored in the browser in production. |
| Privacy | Questions, screenshots and files stay on site. Retention configurable. |
| Concurrency | Several users: vLLM instead of Ollama. |
| Knowledge sources | The isvara knowledge base is the authoritative source. Customer runbooks can be added as extra sources later, ranked below it, and labelled in citations. |

## 5. Decisions (author, 2026-11-04)
- D1: no draft status in the product. Release content is final and curated: every file is reviewed before release. `status: draft` is a review-tracking field for the author only; answers never mention it.
- D2: screenshot upload is version 1.1. Prepare the knowledge and folder structure for it now, so no redesign later.
- D3: data file upload is version 1.2. Export formats are hard to infer, and VCF Operations output can mislead; each format needs its own documented reading first.
- The demo app is a sample, not the target. Learn from it; do not treat it as complete.

## 6. After 1.0: live VCF Operations
- Goal: the compound system applies its knowledge to a live instance.
- Read-only service account on VCF Operations. The assistant never changes configuration.
- Tools: find an object by name; read metrics for a time window (20-second peak where available); read properties (vCPU, memory, reservations, limits, host, cluster).
- The flow executor fills each step from live data instead of asking the user, and shows the values with their timestamps.
- Citations cover both: knowledge file ids and live metric names with time range.
- Data stays on site. Calls are logged.
- Needs the VCF Operations 9.1 metric reference in the catalog first (`todo.md`, Catalog and tools follow-up).
