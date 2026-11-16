# Setting a disk latency threshold

## Prompt
- Microsoft says SQL Server disk latency should consistently stay below 10–15 ms.
- The team proposes a vSphere VM disk latency alert at 15 ms, averaged over 5 minutes.

Which statements are correct?

- A. Alert on the VM at 15 ms: it is the value Microsoft gives for SQL Server.
- B. Microsoft's 10–15 ms describes the latency that SQL Server itself measures for its IO.
- C. The VM-layer threshold should sit below the Windows-layer threshold.
- D. The VM-layer alert sits above 15 ms: the virtualization layer adds latency of its own to what Windows sees.
- E. Read latency and write latency may need different thresholds.
- F. In vCenter, a 5-minute window holds 300 latency samples, one per second.
- G. "Consistently below 10–15 ms" must be turned into a time window before it can drive an alert.
- H. A threshold set on 5-minute averages can be applied unchanged to 20-second peak values.
- I. A threshold set too low turns red often without any user complaint.
- J. With tolerance differing by application, a disk latency alert at the VM layer serves no purpose.

## Likely wrong answer
- A: "Microsoft says 15 ms, so alert on the VM at 15 ms."

## Expected key points
- Answer: B, C, E, G, I.
- A is wrong: an application-layer value used directly as a VM-layer alert is too high; each lower layer needs a lower value.
- B is correct: the guidance is for SQL Server's own view of its IO, the top of the stack.
- C is correct: each layer above adds processing and queueing, so the threshold falls at each lower layer: VM < Guest OS < application.
- D is wrong: the VM layer sits below Windows and SQL Server, so it sees less latency than they do, not more; its threshold is lower.
- E is correct: read and write latency have different patterns, and often only one of them has a problem.
- F is wrong: vSphere samples every 20 seconds, so a 5-minute window holds 15 samples (150 in esxtop at 2 seconds).
- G is correct: "consistently" has to be translated into a time window (how long the value stays in the band) and a sample interval before a threshold is complete.
- H is wrong: a threshold holds only for the interval it was set on; 20-second peaks read higher than 5-minute averages, so their threshold must be higher.
- I is correct: too low gives frequent red without complaints; too high misses real problems.
- J is wrong: the layer rule sets a VM-layer threshold below the Guest OS and application ones; no universal value fits, but each context gets its own.

## Notes
- Tests: judgement and interpretation (heuristic, "it depends").
- A 5-minute window holds 15 samples of 20 seconds (thresholds, Time window rule); option F follows it.
- E keeps the knowledge base's hedge (may need): read and write often differ, not always.
- Changed in the 2026-11-15 audit: D and J reworded without "because" (both still false). Proposed K (VM-level value hides the worst disk) and L (15-times bound) not added: both facts are already tested by two questions.

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
