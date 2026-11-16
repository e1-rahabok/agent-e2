# Network units in the vSphere Client and esxtop

## Prompt
Which units do the Advanced performance chart of a VM in the vSphere Client and the esxtop network panel use for VM network throughput?

- A. Both show kilobytes per second.
- B. The vSphere Client shows kilobytes per second; esxtop shows megabits per second.
- C. The vSphere Client shows megabits per second; esxtop shows kilobytes per second.
- D. Both show megabits per second.

## Answers
B

## Explanation
- A is wrong: esxtop shows network throughput in megabits per second, not kilobytes.
- B is correct: the VM network counters of the Advanced chart are in kilobytes per second, even where the chart title says Mbps; esxtop shows megabits per second. Convert bits to bytes and mega to kilo before comparing.
- C is wrong: the units are swapped; the chart title's Mbps does not change the KBps counters.
- D is wrong: only esxtop is in megabits per second.
- Misconception: A: assuming both tools use the same unit, then comparing the numbers directly.

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Counts only after author approval.
- Changed in the 2026-11-15 audit: the stem names the VM's Advanced chart and the esxtop network panel; the two stacked Overview charts list megabits per second in the vSphere 9.1 documentation, which made D partly true under the broad wording.

## Metadata
```yaml
id: "0029"
title: "Network units in the vSphere Client and esxtop"
product: [vsphere]
technology: [network]
object: [vm]
tool: [vcenter, esxtop]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/tools/esxtop/network-units-vs-vsphere-client
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
knowledge_main: vsphere/tools/esxtop/network-units-vs-vsphere-client
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [A]
misconception_type: [tool-confusion, unit-and-normalization]
pair: "0412"
status: draft
```
