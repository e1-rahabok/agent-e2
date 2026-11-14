# Which VMs to reclaim memory from

## Prompt
- [The attached VCF Operations export](0079/vm-memory-30-days.csv) lists the 40 powered-on VMs of one cluster. Each value is the highest of the last 30 days.
- The cluster owner asks for at least 256 GB of memory back from these VMs, without hurting any application.

Which VMs do you take memory from, and about how much from each? Which counters did you use, which did you not use, and why?

## Likely wrong answer
"Take it from the VMs with the largest gap between configured memory and Active: db-sql-01 alone gives back more than 200 GB."

## Expected key points
- Size from what the Guest OS needs: Guest Needed Memory, with page-out and memory contention as the checks that the guest and the VM are not short already.
- Take memory from app-crm-01, app-hr-02, web-portal-03, file-svc-01, bi-report-02 and dev-build-05: each needs less than a third of its configured memory, with no page-out and no contention. Together they give back at least 256 GB with headroom above Needed Memory (illustrative, at 25% headroom: about 280 GB; bi-report-02 about 76, dev-build-05 about 68, file-svc-01 about 44, app-crm-01 about 40, app-hr-02 about 32, web-portal-03 about 24). Small trims on other VMs on top are fine.
- Not db-sql-01, java-erp-02 or db-pg-03: Active is low, but the guest needs nearly all its memory. SQL Server, the Java heap and PostgreSQL hold caches they depend on; Active is a sampled estimate of recently touched pages and misses them.
- Not legacy-app-07 or appliance-09: VMware Tools is not running, so there is no guest data. Fix the data first; Active and Consumed cannot size the guest.
- Not mq-broker-06 (the guest already pages out heavily: it is short) or rpt-batch-08 (memory contention above 0: it already waits, likely a limit).
- Consumed is not used: it stays near configured once the guest has touched its pages, whatever the guest needs now.
- Reclaim in steps and check page-out and contention after each change.

## Notes
- Revised 2026-11-12: the 300-VM export that was to be supplied is now a generated 40-VM export (a CSV of 1.0 must stay small; design.md, section 13.1). The ask is 256 GB instead of 1 TB.
- The amounts are illustrative. Headroom of 25% above Guest Needed Memory, rounded up to 4 GB, gives 284 GB. An answer with another headroom that names the six VMs and reaches 256 GB is right, with or without small trims on other VMs.

## Metadata
```yaml
id: "0079"
title: "Which VMs to reclaim memory from"
product: [vcf-operations, windows, linux]
technology: [memory]
task: decide-capacity
level: 400
answer_type: judged
input: [table]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - sp5-framework/capacity/rightsizing
  - guest-os/system/concepts/guest-os-sizing
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: guest-os/system/concepts/guest-os-sizing
attachments:
  - 0079/vm-memory-30-days.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [layer-confusion, consumption-as-contention]
status: draft
```
