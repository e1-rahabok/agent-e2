# Storage adapter Highest latency

## Prompt
- In the vSphere Client, the Storage adapter chart of an ESXi host offers Read latency and Write latency for each adapter (vmhba), and one Highest latency line for the host.
- The host has four adapters. The storage team wants one line to watch.

Which statements about Highest latency and the adapter chart are correct?

- A. Highest latency averages each adapter's read and write latency first, then reports the worst adapter.
- B. Beside Highest latency, the adapter chart offers a Commands aborted counter for each adapter.
- C. Highest latency is the average over all adapters of the host, so one slow adapter barely moves it.
- D. Highest latency is of no use for alerting on any of the four adapters of the host.
- E. To find the slowest adapter, take the highest read or write latency among the adapters.
- F. Use Highest latency as the one alert line, as it covers the reads and writes of all four adapters.
- G. In a 1 Day history, each point of Highest latency is the last value of its interval, not the mean.
- H. Highest latency also includes the time requests wait in the Guest OS queues of the VMs on that adapter.

## Answers
A, E, G

## Explanation
- A is correct: Highest latency takes the worst adapter or path, but averages read and write per adapter first.
- B is wrong: there is no commands-aborted counter at adapter level; aborts are counted per path (commandsAborted, beside Bus Resets) and per device.
- C is wrong: it takes the worst adapter, not the mean of the adapters.
- D is wrong: the over-correction. Highest latency follows the worst adapter after averaging; when the slowest adapter's average of read and write rises, it rises, so it can raise an alert for an adapter slow on both.
- E is correct: the useful value is the highest read or write latency among the adapters or paths.
- F is wrong: the misconception (Highest latency = the worst read or write) turned into an action. The per-adapter average of read and write comes first, so the value is not the worst single direction: an adapter with slow reads and fast writes averages to a value below its read latency, so an alert on Highest latency alone misses it; watch read and write latency per adapter.
- G is correct: Highest latency (storageAdapter.maxTotalLatency) is rolled up as Latest, collected from statistics level 3: each history point is the value at the end of its interval (the last 20-second value of a 5-minute point), not representative of it.
- H is wrong: the time a request waits in the Guest OS queues is outside ESXi latency; adapter latency starts in the host.
- Misconception: F: Highest latency is taken as the worst read or write latency of any adapter, so it looks like a complete alert line. Or the overshoot, D: it is useless for alerting.

## Notes
- Theory half of the pair with 0072 (practical; design.md, section 3.9). Different situation from 0072.
- storageAdapter.maxTotalLatency: rollup latest, level 3, in the vSphere Web Services API 9.1 reference (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/storage_adapter_counters.html).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B8 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: D (the not-B of the old key) replaced by an over-correction; F is now the wrong action of using Highest latency as the only alert line (the 10 ms alert moved to 0072, which reads it on the CSV); G now rests on adapter-and-path (Latest, level 3, from the API 9.1 reference). Key changed from A, D, E, G to A, E, G.
- Audit 2026-11-15: H added (Guest OS queue time, the theory side of 0072 D); G shortened (it was the longest option and correct), D reworded and F made a full statement. Key unchanged.
- Re-review 2026-11-16: B (Highest latency = worst read or write) was the negation of A, so one decided the other; B now tests the adapter chart's missing aborts counter (adapter-and-path, Scope), and the misconception is carried by F. Key unchanged.

## Metadata
```yaml
id: "0406"
title: "Storage adapter Highest latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/host/adapter-and-path
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/technology/storage/concepts/esxi-storage-io-path
knowledge_main: vsphere/technology/storage/metrics/host/adapter-and-path
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B8"
misconception: [F]
misconception_type: [average-hides-worst]
pair: "0072"
status: draft
```
