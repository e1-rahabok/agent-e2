# Setting a disk latency threshold

## Prompt
- Microsoft says SQL Server disk latency should consistently stay below 10–15 ms.

Should we set a vSphere VM disk latency alert at 15 ms averaged over 5 minutes?

## Likely wrong answer
"Yes, use 15 ms as the threshold."

## Expected key points
- The 10–15 ms guidance is at the **SQL layer**. Windows layer must be lower, and the VM layer lower still, to leave room for processing and queues higher in the stack.
- Read vs write may need different thresholds.
- "Consistently": IO is measured per second, so 5 minutes is 300 samples. A 5-minute window tends to give many alerts but few real complaints.
- No universal threshold: tolerance varies by application, use case and end user. Too low = noise, too high = missed problems.

## Notes
- Tests: Judgment / interpretation (heuristic, "it depends").

## Metadata
```yaml
id: vsphere-storage-002
title: "Setting a disk latency threshold"
product: [vsphere]
technology: [storage]
input: [text]
task: judge-setting
knowledge:
  - foundations/thresholds
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Interpretation Challenge."
answer_type: judged
level: 300                      # author 2026-11-05
status: draft
```
