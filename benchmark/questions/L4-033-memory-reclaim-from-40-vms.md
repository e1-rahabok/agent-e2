# Which VMs to reclaim memory from

## Prompt
- [The attached VCF Operations export](0079/vm-memory-30-days.csv) lists the 40 powered-on VMs of one cluster. Each value is the highest of the last 30 days.
- The cluster owner asks for at least 256 GB of memory back from these VMs, without hurting any application.

Which statements about the VMs to take memory from, and the counters to use, are correct?

- A. Size each VM from Guest Needed Memory, not from the VM-level Active or Consumed counters.
- B. Take memory from the VMs with the largest gap between configured memory and Active: db-sql-01 alone gives back more than 200 GB.
- C. app-crm-01, app-hr-02, web-portal-03, file-svc-01, bi-report-02 and dev-build-05 can give back 256 GB, keeping headroom above Needed Memory.
- D. db-sql-01, java-erp-02 and db-pg-03 are not donors: their guests need nearly all their memory, though Active is low.
- E. The new size of a donor is its peak Needed Memory itself; headroom above it is waste.
- F. legacy-app-07 and appliance-09 cannot be sized: VMware Tools is not running, so there is no guest data.
- G. A 30-day window can miss a quarter-end or year-end peak; the sizing data must cover the business cycle.
- H. rpt-batch-08 is not a donor: its memory contention above 0 shows it already waits.
- I. Ballooned memory is not deducted from a donor's Needed Memory before the donor is sized.
- J. Non Zero Active sits above Guest Needed Memory on most of these VMs.
- K. For db-sql-01, the size comes from SQL Server's own memory limit first, then from Needed Memory.
- L. Active misses the cache that SQL Server, the Java heap and PostgreSQL work from.
- M. Consumed near configured on most VMs shows that the cluster is short of memory.

## Likely wrong answer
- B: "Take it from the VMs with the largest gap between configured memory and Active: db-sql-01 alone gives back more than 200 GB."

## Expected key points
- Answer: A, C, D, F, G, H, I, K, L.
- A true: size from what the Guest OS needs: Guest Needed Memory, with page-out and memory contention as the checks that the guest and the VM are not short already.
- B false: db-sql-01 has low Active, but its guest needs 241.2 of its 256 GB. Active is a sampled estimate of recently touched pages and misses the buffer pool.
- C true: each needs less than a third of its configured memory, with no page-out and no contention. Illustrative, at 25% headroom rounded up to 4 GB: bi-report-02 about 76, dev-build-05 about 68, file-svc-01 about 44, app-crm-01 about 40, app-hr-02 about 32, web-portal-03 about 24: about 284 GB. Small trims on other VMs on top are fine.
- D true: Needed Memory is 241.2 of 256, 117.9 of 128 and 89.6 of 96 GB.
- E false: the new size is peak Needed Memory plus headroom, so the result lands in the green band, not at 100%.
- F true: no Needed Memory, so no sizing. Active and Consumed do not stand in for it; restore the guest data first.
- G true: the projection covers the business cycle (annual sales need annual data); a month of peaks shows that month only.
- H true: memory contention of 3.4%: the VM already waits, whatever the cause. Contention is excluded from the size, not from the choice of VM.
- I true: size on Needed Memory as VMware Tools reports it, with no deduction for the balloon; the balloon also takes in-use pages that the guest pages out and still needs.
- J false: in the export Non Zero Active is below Guest Needed Memory on all 38 VMs that have guest data; Active is usually far below Consumed and below what the guest needs.
- K true: an application that keeps its own cache grows into the limit it is given, so its working set and Needed Memory show the limit; size from the application's limit first (SQL Server max server memory), then from Needed Memory.
- L true: SQL Server, the Java heap and PostgreSQL hold caches they depend on; Active is a sample of recently touched pages and does not see how the application uses its cache.
- M false: Consumed holds guest cache; memory used as cache is not demand. Six VMs need less than a third of their configured memory.

## Notes
- Revised 2026-11-12: the 300-VM export that was to be supplied is now a generated 40-VM export (a CSV of 1.0 must stay small; design.md, section 13.1). The ask is 256 GB instead of 1 TB.
- The amounts are illustrative. Headroom of 25% above Guest Needed Memory, rounded up to 4 GB, gives 284 GB. An answer with another headroom that names the six VMs and reaches 256 GB is right, with or without small trims on other VMs.
- Option C holds for any headroom up to about 50%: 432 GB configured minus 1.5 x 111.6 GB needed leaves about 265 GB.
- Changed in the 2026-11-15 audit: three true options over the two-question cap replaced in place by true facts from guest-os-sizing: G (guest page-out, kept by 0400/0401) by the business-cycle window; I (Consumed stays after the guest frees a page, kept by 0095/0386) by the no-deduction rule for ballooned memory (pair half 0021 C tests it as a misconception); K (cut in steps, kept by 0400/0401) by sizing from the application's own limit. mq-broker-06 (page-out 1,240/s) stays in the export as a non-donor; C does not depend on it. H key point no longer guesses a limit. Key unchanged.
- Paired with 0021 (theory and practical; design.md, section 3.9).

## Metadata
```yaml
id: "0079"
title: "Which VMs to reclaim memory from"
product: [vcf-operations, windows, linux]
technology: [memory]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,D,F,G,H,I,K,L]
misconception: [B]
pair: "0021"
input: [table]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - sp5-framework/capacity/rightsizing
  - guest-os/system/guest-os-sizing
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - guest-os/memory/sql-server-memory
knowledge_main: guest-os/system/guest-os-sizing
attachments:
  - 0079/vm-memory-30-days.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: [layer-confusion, consumption-as-contention]
status: draft
```
