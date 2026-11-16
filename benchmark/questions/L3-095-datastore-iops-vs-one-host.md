# Datastore read IOPS against one host's view

## Prompt
- VMs on host esx-c3-02 (host A in the options) report slow storage.
- The VMFS datastore ds-shared-07 is mounted by the four hosts of cluster cl-c3, esx-c3-01 to esx-c3-04, all managed by one vCenter.
- The administrator exported two VCF Operations list views for the last 24 hours: [the cluster's datastores](0417/vcf-operations-datastores-24h.csv) and [the cluster's hosts with their datastore metrics](0417/vcf-operations-hosts-24h.csv). Each value is the 24-hour average; a (Max) column is the highest 5-minute value.
- He expected host A's Read IOPS for ds-shared-07 to match the datastore's Read IOPS.

Which statements are correct?

- A. The datastore's value counts the reads of every host that mounts it.
- B. One of the two values is wrong, since both count reads on the same datastore.
- C. Host A sends between a quarter and two fifths of the datastore's reads in this window.
- D. The four hosts' Read IOPS for ds-shared-07 add up to the datastore's Read IOPS within 10%.
- E. Host A's value also counts the reads of VMs on other hosts that use the same datastore.
- F. Open a case: VCF Operations under-reports host A's datastore IO.
- G. With Storage I/O Control on, ds-shared-07's Aggregate IOPs seen from host A counts only host A's reads.
- H. The datastore value and the per-host values cannot be compared.
- I. Host A's highest 5-minute Read IOPS for ds-shared-07 is above the datastore's highest.

## Likely wrong answer
B: the datastore and host A's view of it must match, so a value is wrong. Or F: open a case.

## Expected key points
- Answer: A, C, D.
- A is correct: the datastore object spans all hosts that mount it; a host's datastore metrics are that host's view only.
- B is wrong: the misconception. Each value is correct from its own vantage point; the gap is the other hosts' IO.
- C is correct: reading. `Datastore:ds-shared-07|Read IOPS` of esx-c3-02 in the hosts export, 780.5, is 34.6% of `Datastore I/O|Read IOPS` of ds-shared-07 in the datastores export, 2,254.3: host A is the largest of the four hosts but sends about a third.
- D is correct: the datastore object spans the hosts that mount it, all four in this vCenter, so the four hosts' `Datastore:ds-shared-07|Read IOPS` add up to the datastore's `Datastore I/O|Read IOPS` within 10%: 2,262.6 against 2,254.3 (the same holds for Write IOPS and for ds-shared-08).
- E is wrong: a host counts only the IO it sends.
- F is wrong: nothing is missing; esx-c3-01, esx-c3-03 and esx-c3-04 carry the rest.
- G is wrong: Storage I/O Control Aggregate IOPs is a datastore-wide counter, summed over all hosts and VMs on the datastore, whichever host's chart shows it; only the host's own datastore counters show its share.
- H is wrong: the over-correction. The datastore object spans the hosts that mount it; their values add up to it.
- I is wrong: reading. Host A's `Read IOPS (Max)` for ds-shared-07 is 1,387.8, the datastore's 3,956.6. In each 5-minute point the datastore counts host A's reads plus the other hosts', so its peak cannot fall below one host's.

## Notes
- Paired with the theory question 0049 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C22 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: H (over-correction) and I (a false screen reading) added; knowledge_main is host/datastore. Key unchanged: A, C, D.
- 2026-11-15: screenshots replaced by generated exports (project/practical-questions-as-exports-2026-11-15.md); the exports carry the key's condition.
- Audit 2026-11-15: G (reads from other datastores counted in this datastore's value, which no operator believes) replaced by Storage I/O Control Aggregate IOPs read from one host (storage-io-control Misconceptions; added to `knowledge`); A shortened (truth unchanged). Key unchanged: A, C, D.
- Re-review 2026-11-16: A and E negated each other, and C and I were exclusive readings of one share; A now states only the datastore side (E tests the host side), I reads the (Max) columns instead of the share. "about" removed from the correct C and D (C names the 25-40% range the case checks, D the 10% the case checks). Key unchanged: A, C, D.

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
  - vsphere/technology/storage/metrics/datastore/storage-io-control
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
