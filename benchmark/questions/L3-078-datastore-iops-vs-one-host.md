# Datastore read IOPS against one host's view

## Prompt
- VMs on host esx-c3-02 (host A in the options) report slow storage.
- The VMFS datastore ds-shared-07 is mounted by the four hosts of cluster cl-c3, esx-c3-01 to esx-c3-04, all managed by one vCenter.
- The administrator exported two VCF Operations list views for the last 24 hours: [the cluster's datastores](0417/vcf-operations-datastores-24h.csv) and [the cluster's hosts with their datastore metrics](0417/vcf-operations-hosts-24h.csv). Each value is the 24-hour average; a (Max) column is the highest 5-minute value.
- He expected host A's Read IOPS for ds-shared-07 to match the datastore's Read IOPS.

Which statements are correct?

- A. The datastore value counts the reads of every host that mounts it; host A's value counts only host A's reads.
- B. One of the two values is wrong, since both count reads on the same datastore.
- C. Host A sends about 40% or less of the datastore's reads in this window.
- D. Adding the same value over every mounting host gives about the datastore's value.
- E. Host A's value also counts the reads of VMs on other hosts that use the same datastore.
- F. Open a case: VCF Operations under-reports host A's datastore IO.
- G. Reads of host A's VMs from other datastores are part of host A's value for this datastore.
- H. The datastore value and the per-host values cannot be compared.
- I. Host A carries most of the datastore's reads in this window.

## Likely wrong answer
B: the datastore and host A's view of it must match, so a value is wrong. Or F: open a case.

## Expected key points
- Answer: A, C, D.
- A true: a host's datastore metrics are that host's view only; the datastore object spans all hosts that mount it.
- B false: each value is correct from its own vantage point; the gap is the other hosts' IO.
- C true: reading. `Datastore:ds-shared-07|Read IOPS` of esx-c3-02 in the hosts export is 40% or less (about a third) of `Datastore I/O|Read IOPS` of ds-shared-07 in the datastores export.
- D true: the datastore object spans the hosts that mount it, all four in this vCenter, so the four hosts' `Datastore:ds-shared-07|Read IOPS` add up to the datastore's `Datastore I/O|Read IOPS` within 10% (the same holds for Write IOPS and for ds-shared-08).
- E false: a host counts only the IO it sends.
- F false: nothing is missing; esx-c3-01, esx-c3-03 and esx-c3-04 carry the rest.
- G false: the value is per datastore instance; host A's reads from ds-shared-08 are in its own column, `Datastore:ds-shared-08|Read IOPS`.
- H false: the over-correction. The datastore object spans the hosts that mount it; their values add up to it.
- I false: reading. Host A is the largest of the four hosts, but its Read IOPS for ds-shared-07 is 40% or less of the datastore's.

## Notes
- Paired with the theory question 0049 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C22 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: H (over-correction) and I (a false screen reading) added; knowledge_main is host/datastore. Key unchanged: A, C, D.
- 2026-11-15: screenshots replaced by generated exports (project/practical-questions-as-exports-2026-11-15.md); the exports carry the key's condition.

## Metadata
```yaml
id: "0417"
title: "Datastore read IOPS against one host's view"
product: [vsphere, vcf-operations]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [table]
object: [datastore, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/architecture/object-relationships
  - vsphere/technology/storage/metrics/host/datastore
  - vsphere/technology/storage/concepts/storage-layers
knowledge_main: vsphere/technology/storage/metrics/host/datastore
attachments:
  - 0417/vcf-operations-datastores-24h.csv
  - 0417/vcf-operations-hosts-24h.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C22"
answer: [A, C, D]
misconception: [B]
misconception_type: [same-name-other-object, provider-vs-consumer]
pair: "0049"
status: draft
```
