# Setting a disk latency threshold

## Prompt
- Microsoft says SQL Server disk latency should consistently stay below 10–15 ms.
- The team proposes a vSphere VM disk latency alert at 15 ms, averaged over 5 minutes.

Which statements are correct?

- A. Alert on the VM at 15 ms: it is the value Microsoft gives for SQL Server.
- B. Microsoft's 10–15 ms describes the latency that SQL Server itself measures for its IO.
- C. The VM-layer threshold should sit below the Windows-layer threshold.
- D. The VM-layer alert should sit above 15 ms, because the virtualization layer adds latency of its own.
- E. Read latency and write latency should each get their own threshold.
- F. In vCenter, a 5-minute window holds 300 latency samples, one per second.
- G. An alert on the 5-minute average of disk latency fires often while users report few problems.
- H. A threshold set on 5-minute averages can be applied unchanged to 20-second peak values.
- I. A threshold set too low turns red often without any user complaint.
- J. Because tolerance differs by application, a disk latency alert at the VM layer serves no purpose.

## Likely wrong answer
- A: "Microsoft says 15 ms, so alert on the VM at 15 ms."

## Expected key points
- Answer: B, C, E, G, I.
- A is false: an application-layer value used directly as a VM-layer alert is too high; each lower layer needs a lower value.
- B is true: the guidance is for SQL Server's own view of its IO, the top of the stack.
- C is true: each layer above adds processing and queueing, so the threshold falls at each lower layer: VM < Guest OS < application.
- D is false: the VM layer sits below Windows and SQL Server, so it sees less latency than they do, not more; its threshold is lower.
- E is true: read and write latency have different patterns, and often only one of them has a problem.
- F is false: vSphere samples every 20 seconds, so a 5-minute window holds 15 samples (150 in esxtop at 2 seconds).
- G is true: observed with a 5-minute window on disk latency; "consistently" has to be translated into a time window.
- H is false: a threshold holds only for the interval it was set on; 20-second peaks read higher than 5-minute averages, so their threshold must be higher.
- I is true: too low gives frequent red without complaints; too high misses real problems.
- J is false: the layer rule sets a VM-layer threshold below the Guest OS and application ones; no universal value fits, but each context gets its own.

## Notes
- Tests: Judgment / interpretation (heuristic, "it depends").
- The old key said a 5-minute window is 300 samples; the knowledge base (Time window rule) says 15 samples of 20 seconds, and option F follows it.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option; the negation pairs (old B, D) restated; over-correction J and wrong action D added (author approved, 2026-11-14). Key stays B, C, E, G, I.

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
