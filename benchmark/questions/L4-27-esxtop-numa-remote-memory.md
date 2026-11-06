# Remote memory in the esxtop NUMA columns

## Prompt
The attached screenshot is the esxtop memory panel (m) of one ESXi host with the NUMA columns shown.

- The host has 2 sockets of 16 cores each.
- The VM of interest is a database VM. Its owner reports that query times vary from day to day.

Read the NUMA columns of that VM. What do they show, what are the possible causes, and what do you check next?

## Input to supply
- Tool: esxtop on one ESXi 9.1 host with 2 NUMA nodes, memory panel (press m), NUMA fields added (press f).
- Must show the columns NHN, NMIG, NRMEM (MB), N%L, GST_ND0, GST_ND1 for at least 5 VMs.
- Condition for the key: one VM has more vCPUs than cores per NUMA node (for example 20 vCPUs on 16-core sockets), NHN shows two nodes (0,1), N%L below 80%, NRMEM above 0. The other VMs show one home node and N%L 100.
- Mask VM names if they reveal the customer.
- Save as `benchmark/questions/67/esxtop-memory-numa-columns.png`.

## Likely wrong answer
"NMIG is high, so the VM is moving between nodes right now: pin it to one node with CPU affinity."

## Expected key points
- The VM spans two NUMA nodes (NHN 0,1) and part of its memory is remote: N%L below 100% and NRMEM above 0. Remote access raises the average memory latency.
- Causes: more vCPUs than cores per NUMA node (a wide VM); memory larger than one node; CPU Hot Add enabled, which turns vNUMA off and interleaves memory; recent NUMA rebalancing whose page migration has not finished.
- NMIG is cumulative since power-on, not a current rate.
- Next: compare the vCPU count with the cores per node; check CPU Hot Add; check whether the guest sees the vNUMA topology; size the VM to fit one node if the Guest OS demand allows.
- Do not set CPU affinity or memory affinity: the VM then leaves NUMA management, with no rebalancing and no memory migration.

## Notes
- Previous id: question-0067 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0067"
title: "Remote memory in the esxtop NUMA columns"
product: [vsphere]
technology: [memory, cpu]
task: troubleshoot
level: 400
answer_type: judged
input: [screenshot]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/cpu/concepts/numa
  - vsphere/technology/cpu/concepts/virtual-numa
attachments:
  - 0067/esxtop-memory-numa-columns.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
