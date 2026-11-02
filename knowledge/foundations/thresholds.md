---
id: foundations/thresholds
type: concept
scope: vendor-neutral
resources: [cpu, memory, storage, network]
related: [foundations/metrics-as-accounting, vsphere/foundations/visibility-layers]
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Interpretation Challenge
corrections: []
review_notes: []
status: draft
---

# Thresholds and interpretation

## Definition
- What counts as a good value depends on context. There is no universal threshold.
- Tolerance varies by:
  - application,
  - use case of the same application,
  - end user, even for the same use case.

## Consequence
- Out-of-the-box universal thresholds are unreliable.
- Threshold too low → frequent red, without actual complaints.
- Threshold too high → actual problems missed.

## Layer rule
- A threshold given at one layer of the stack does not apply unchanged at a lower layer.
- Each layer above adds processing latency and queueing.
- So the threshold must be lower at each lower layer.
```text
threshold(VM layer) < threshold(Guest OS layer) < threshold(application layer)
```

## Time window rule
- "Consistently above X" must be translated into a time window.
- IO is measured per second. A 5-minute window = 300 samples.
- Observed: a 5-minute window on disk latency produces many alerts but few user complaints.

## Worked example: SQL Server disk latency
- Microsoft guidance for SQL Server: disk latency should consistently stay within 10–15 ms.
- That value is at the SQL Server layer.
- At the Windows layer the value must be lower.
- At the vSphere VM layer the value must be lower still.
- Read and write latency may need different thresholds.
- Reference: https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/troubleshoot-sql-io-performance

## Traps
- Using an application-layer threshold (e.g. 15 ms) directly as a VM-layer alert → too high.
- Treating "consistently" as a 5-minute average → many alerts, few complaints.
