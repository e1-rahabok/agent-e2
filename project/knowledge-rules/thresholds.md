# Thresholds

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

- A threshold has more parts than a number:

```text
threshold = (metric, object, instance reading, sample interval, time window) -> band values and source
```

- Sample interval: the same workload reads higher at 2 seconds (esxtop) than at 20 seconds, and higher at 20 seconds than at 5 minutes. A band set on 20-second peaks cannot be applied to a 5-minute chart. Example: VM Compressed + Swapped (5-minute samples) has a lower band than VM Memory Contention (20-second peaks) although it is the less serious signal.
- Instance reading: for a metric with instances (per vCPU, per disk), the worst instance is always at least the object value. The worst vCPU of a 64-vCPU VM can be far above the VM's normalized Ready. A band must say which reading it applies to, as "Peak CPU Ready among any vCPU" does.
- One place per number (2026-11-10). A number Agent E2 or a system decides with lives only in `knowledge/catalog/thresholds-*.yaml`; no knowledge file, table or image repeats it. A knowledge file holds the mechanism and the reasons, and numbers that no machine decides with: vendor values written as misconceptions ("the vendor says X; read Y"), reading rules ("Latency near 0 with Ready above 15% means a limit"), worked examples.
  - Admission: a row exists only for a use case: KPI levels, KAI or KSI, alert symptom, capacity model input or decision.
  - A KPI metric qualifies only if it maps to green, yellow, orange, red and a worse colour means slower work for the consumer. Banding alone is not enough: CPU Usage can be banded, but high usage is consumption, not slowness.
  - Sections are named by use, and the section name is the use: no `kind` or `use` field on the rows. The Harness labels every value with its use (KPI, Alert, Capacity decision, Capacity rule), because one metric has a different threshold per use. Lint rejects any other section.
  - `knowledge/catalog/thresholds-performance.yaml` (no SLA and no SLI: performance is managed by the KPI only, 2026-11-11):
    - `kpi`: KPI colour levels, one line per object and metric, yellow, orange, red for 5m, 20s and 2s (9 values), entered by hand, null until entered, with `group`, `kb` and `excluded_when_green`. The 4x rule is a guide for choosing a 20-second value from a 5-minute one (a spike rarely lasts 300 seconds), not a formula: it never fills a cell. No class of service.
  - `knowledge/catalog/thresholds-capacity.yaml`: `models` (capacity and risk model inputs with grey for wastage, green, yellow, orange, red), `decisions` (close for business), `rules` (planning and sizing).
  - `knowledge/catalog/thresholds-alerts.yaml`: `alerts`, one row per alert and criticality (`criticality`: red or orange, no yellow; `pillar`: performance or capacity). Alerts are set apart from the KPI: different purpose, set separately.
  - Ids are unique across the three files. The Harness loads them into its catalog at start-up and shows a file's rows whenever the file is in the context (classic facts, agentic `read_file`).
  - Still to move (a `quote` marks a row whose number is also in prose; lint checks the copy until it goes): alert values in the alert files; decision tree steps (can-cluster-take-more-vms, host-cpu-capacity-headroom); class of service planning; monster VM sizes.
- No invented thresholds: a threshold goes in only with a source. Row field `source`: `knowledge-base`, or a vendor document with its version (`vsphere-9.1-docs`, `performance-best-practices-9.1`, `microsoft`), because vendor values can go stale and the newer official document wins.
- The rule for the model is in `observability/thresholds` (Interval rule, Instance rule). The catalog has `interval` and `instance` fields, filled only where a source states them.
