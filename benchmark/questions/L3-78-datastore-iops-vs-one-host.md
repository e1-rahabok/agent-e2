# Datastore read IOPS against one host's view

## Prompt
- VMs on host A report slow storage. The administrator compares, in VCF Operations, the Read IOPS of their shared VMFS datastore with the Read IOPS that host A shows for the same datastore, and expected the two to match.
- See [the datastore's Read IOPS](0417/vcf-operations-datastore-read-iops-24h.png) and [the Read IOPS of each mounting host for that datastore](0417/vcf-operations-hosts-datastore-read-iops-24h.png).

Which statements are correct?

- A. The datastore value counts the reads of every host that mounts it; host A's value counts only host A's reads.
- B. One of the two values is wrong, since both count reads on the same datastore.
- C. Host A sends about 40% or less of the datastore's reads in this window.
- D. Adding the same value over every mounting host gives about the datastore's value.
- E. Host A's value also counts the reads of VMs on other hosts that use the same datastore.
- F. Open a case: VCF Operations under-reports host A's datastore IO.
- G. Reads of host A's VMs from other datastores are part of host A's value for this datastore.

## Input to supply
- Product and version: VCF Operations 9.1, vSphere 9.1.
- Object: one shared VMFS datastore mounted by 3 or more hosts, all in the same vCenter, with VMs on each host reading from it; host A is one of them.
- How to produce it: run a read load (fio or a backup read) in VMs on each host, with host A's VMs doing 40% or less of the total.
- Screen 1, VCF Operations > the datastore > Metrics: Read IOPS, last 24 hours, with the average visible. Save as `0417/vcf-operations-datastore-read-iops-24h.png`.
- Screen 2, VCF Operations, the Read IOPS each mounting host shows for that datastore (host > Metrics > the datastore instance), last 24 hours, all hosts on one chart or in a list view with their 24-hour averages; host A labelled as host A. Save as `0417/vcf-operations-hosts-datastore-read-iops-24h.png`.
- Condition the key depends on: host A's 24-hour average 40% or less of the datastore's; the hosts' averages add up to within 10% of the datastore's average; every mounting host is on screen 2.
- Masking: mask every VM, host, datastore and cluster name; label the masked host of interest "host A".

## Likely wrong answer
B: the datastore and host A's view of it must match, so a value is wrong. Or F: open a case.

## Expected key points
- Answer: A, C, D.
- A true: a host's datastore metrics are that host's view only; the datastore object spans all hosts that mount it.
- B false: each value is correct from its own vantage point; the gap is the other hosts' IO.
- C true: the chart shows host A at 40% or less of the datastore's average.
- D true: the datastore object spans the hosts that mount it, so the hosts' values add up to it (within the condition's 10%).
- E false: a host counts only the IO it sends.
- F false: nothing is missing; the other hosts carry the rest.
- G false: the value is per datastore instance; IO to other datastores is counted under those datastores.

## Notes
- Paired with the theory question 0049 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C22 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0417"
title: "Datastore read IOPS against one host's view"
product: [vsphere, vcf-operations]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [datastore, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/architecture/object-relationships
  - vsphere/technology/storage/metrics/host/datastore
  - vsphere/technology/storage/concepts/storage-layers
knowledge_main: vsphere/architecture/object-relationships
attachments:
  - 0417/vcf-operations-datastore-read-iops-24h.png
  - 0417/vcf-operations-hosts-datastore-read-iops-24h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C22"
answer: [A, C, D]
misconception: [B]
misconception_type: [same-name-other-object, provider-vs-consumer]
pair: "0049"
status: awaiting-input
```
