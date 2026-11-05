# Which hosts have real storage latency problems

## Prompt
The attached table is a VCF Operations export of 192 ESXi hosts over one week: per storage adapter, the maximum, 99th percentile and 95th percentile of read and write latency.

- Host esx-017 has the highest maximum write latency of all hosts: 250 ms.
- Hosts esx-044 and esx-101 have a 99th percentile write latency above 20 ms.

Which statements are correct? Choose all that apply.

- A. esx-017 has a one-off spike: its 95th percentile write latency is under 1 ms.
- B. esx-017 is the host to fix first, because it has the highest maximum.
- C. esx-044 and esx-101 have real latency problems: drill down per adapter.
- D. Highest latency of each host would give the same ranking as the worst read or write latency.

## Input to supply
- Source: VCF Operations 9.1 export, 192 hosts, 7 days, one row per host and storage adapter.
- Columns: host, vmhba, read latency max, read latency p99, read latency p95, write latency max, write latency p99, write latency p95 (ms).
- Condition for the key: esx-017 has write max 250 ms and write p95 0.33 ms; esx-044 and esx-101 have write p99 above 20 ms on one adapter; every other host has max at or below 5 ms. Rename hosts if needed and keep these three names.
- Save as `benchmark/questions/question-0081/host-adapter-latency-192-hosts.xlsx`.

## Likely wrong answer
B: ranking hosts by the maximum.

## Expected key points
- Answer: A, C.
- One outlier dominates the maximum: esx-017 had 250 ms once with a 95th percentile of 0.33 ms.
- The 95th or 99th percentile reveals the hosts with real latency problems. Drill down per adapter, and read and write separately.
- D is wrong: Highest latency averages read and write per adapter first, so it can rank differently.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0081
title: "Which hosts have real storage latency problems"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/storage/metrics/host/adapter-and-path
  - vsphere/technology/storage/diagnosis/host-storage-latency
attachments:
  - question-0081/host-adapter-latency-192-hosts.xlsx
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: awaiting-input
```
