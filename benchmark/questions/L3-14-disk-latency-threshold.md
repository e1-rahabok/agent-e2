# Setting a disk latency threshold

## Prompt
- Microsoft says SQL Server disk latency should consistently stay below 10–15 ms.
- The team proposes a vSphere VM disk latency alert at 15 ms, averaged over 5 minutes.

Which statements are correct?

- A. The proposal is right: 15 ms over 5 minutes at the VM layer matches Microsoft's guidance for SQL Server.
- B. Microsoft's 10–15 ms applies at the SQL Server layer, not at the VM's virtual disk.
- C. The VM-layer value should be below the Windows-layer value, which should be below SQL Server's.
- D. The Windows layer can take the same 15 ms, since Windows sits directly below SQL Server.
- E. Read latency and write latency may need different thresholds.
- F. In vCenter, a 5-minute window holds 300 latency samples, one for each second.
- G. Reading "consistently" as a 5-minute average tends to raise many alerts but few user complaints.
- H. A threshold set on 5-minute averages can be reused unchanged on 20-second peak values.
- I. No single threshold fits every application: tolerance differs by application, use case and user.

## Likely wrong answer
- A: "Microsoft says 15 ms, so alert on the VM at 15 ms."

## Expected key points
- Answer: B, C, E, G, I.
- A is false: an application-layer value used directly as a VM-layer alert is too high.
- B is true: the guidance is for SQL Server's own view of its IO.
- C is true: each layer above adds processing and queueing, so the threshold is lower at each lower layer: VM < Guest OS < application.
- D is false: Windows is a lower layer than SQL Server, so its value must be lower.
- E is true: read and write latency have different patterns, and often only one has a problem.
- F is false: vSphere samples every 20 seconds, so a 5-minute window holds 15 samples (150 in esxtop at 2 seconds); an IO rate is a per-second value within each sample.
- G is true: observed with a 5-minute window on disk latency; "consistently" has to be translated into a time window.
- H is false: a threshold holds only for the interval it was set on; 20-second peaks read higher than 5-minute averages, so their threshold must be higher.
- I is true: too low gives frequent red without complaints, too high misses real problems; out-of-the-box universal thresholds are unreliable.

## Notes
- Tests: Judgment / interpretation (heuristic, "it depends").
- The old key said a 5-minute window is 300 samples; the knowledge base (Time window rule) says 15 samples of 20 seconds, and option F follows it.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0027"
title: "Setting a disk latency threshold"
product: [vsphere]
technology: [storage]
input: [text]
task: judge-setting
knowledge:
  - sp5-framework/observability/thresholds
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
object: [vm]
tool: [vcenter]
knowledge_main: sp5-framework/observability/thresholds
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Interpretation Challenge."
answer_type: deterministic
answer: [B, C, E, G, I]
misconception: [A]
level: 300                      # author 2026-11-05
misconception_type: [threshold-transplanted]
status: draft
```
