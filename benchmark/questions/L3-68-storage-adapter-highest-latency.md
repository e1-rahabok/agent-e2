# Storage adapter Highest latency

## Prompt
- In the vSphere Client, the Storage adapter chart of an ESXi host offers Read latency and Write latency for each adapter (vmhba), and one Highest latency line for the host.
- The host has four adapters. The storage team wants one line to watch.

Which statements about Highest latency are correct?

- A. For each adapter, Highest latency first averages its read and write latency, then reports the worst adapter.
- B. Highest latency equals the single worst read or write latency of any adapter.
- C. Highest latency is the average over all adapters of the host, so one slow adapter barely moves it.
- D. Highest latency is useless for alerting on any adapter.
- E. To find the slowest adapter, take the highest read or write latency among the adapters.
- F. Use Highest latency as the one alert line for all four adapters.
- G. Where vCenter keeps a 1 Day history of Highest latency, each 5-minute point is the last 20-second value of the interval, not its average.

## Likely wrong answer
B: Highest latency is the worst read or write latency of any adapter. Or the overshoot, D: it is useless for alerting.

## Expected key points
- Answer: A, E, G.
- A true: Highest latency takes the worst adapter or path, but averages read and write per adapter first.
- B false: the per-adapter average of read and write comes first, so the value is not the worst single direction.
- C false: it takes the worst adapter, not the mean of the adapters.
- D false: the over-correction. Highest latency follows the worst adapter after averaging; an adapter slow on both reads and writes, or on its average, raises it.
- E true: the useful value is the highest read or write latency among the adapters or paths.
- F false: the wrong action. An adapter with slow reads and fast writes averages to a value below its read latency, so an alert on Highest latency alone misses it; watch read and write latency per adapter.
- G true: Highest latency (storageAdapter.maxTotalLatency) is rolled up as Latest, collected from statistics level 3: each history point is the value at the end of its interval, not representative of it.

## Notes
- Theory half of the pair with 0072 (practical; design.md, section 3.9). Different situation from 0072.
- storageAdapter.maxTotalLatency: rollup latest, level 3, in the vSphere Web Services API 9.1 reference (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/storage_adapter_counters.html).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B8 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: D (the not-B of the old key) replaced by an over-correction; F is now the wrong action of using Highest latency as the only alert line (the 10 ms alert moved to 0072, which reads it on the CSV); G now rests on adapter-and-path (Latest, level 3, from the API 9.1 reference). Key changed from A, D, E, G to A, E, G.

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
knowledge_main: vsphere/technology/storage/metrics/host/adapter-and-path
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B8"
answer: [A, E, G]
misconception: [B]
misconception_type: [average-hides-worst]
pair: "0072"
status: draft
```
