# Storage DRS: full datastore in a healthy cluster

## Prompt
- A datastore cluster has four VMFS datastores of 10 TB each. Used space: DS-1 9.2 TB (92%), DS-2 8.3 TB (83%), DS-3 7.95 TB (79.5%) and DS-4 4.0 TB (40%). The cluster as a whole is 29.45 TB of 40 TB used (73.6%).
- Storage DRS is enabled with the automation level Fully Automated. I/O metric inclusion is off.
- The space utilization threshold and the minimum space utilization difference are at their defaults. The aggressiveness level was not changed.
- No VM or VMDK affinity or anti-affinity rules are defined, and no datastore is in maintenance mode.
- All VMs use thick-provisioned disks, each VM on one datastore. Every VM is between 200 GB and 600 GB.
- A Storage DRS run starts now.

Which statements about this Storage DRS run are correct?

- A. DS-1 gives up disks in this run.
- B. No disk moves, because the datastore cluster as a whole is under the space utilization threshold.
- C. Disks move until all four datastores sit near the cluster average of 73.6%.
- D. DS-3 receives disks from DS-2.
- E. DS-3 receives disks from DS-1.
- F. DS-4 receives disks in this run.
- G. DS-2 keeps all its disks, because DS-3, the next datastore below it, is within the minimum space utilization difference.
- H. DS-3 gives up disks, because it sits above the cluster average.
- I. The moves are applied without an administrator approving them.

## Likely wrong answer
B (the cluster average is compared with the threshold), C (Storage DRS levels all members to the average), or G (a source is skipped when the nearest datastore is within the minimum difference).

## Expected key points
- Answer: A, F, I.
- A is true: the thresholds are set on the datastore cluster but apply to each datastore. DS-1 (92%) is over the default 80% space utilization threshold, so it is a source.
- B is false: DS-1 and DS-2 are over 80%; the 73.6% average does not matter, as an average hides a full member.
- C is false: Storage DRS moves enough disks to bring each source back under the threshold; it does not level the members to the average.
- D is false: a destination must be more than the default minimum space utilization difference (5 points) below the source. DS-2 (83%) to DS-3 (79.5%) is 3.5 points.
- E is false: DS-1 to DS-3 passes the difference (12.5 points), but a destination must stay under the threshold after the move. DS-3 has 0.05 TB of room under 80% and the smallest VM is 200 GB.
- F is true: DS-4 (40%) passes the difference for both sources and stays under 80% after taking 1.5 TB or more.
- G is false: the difference is checked per source and destination pair, not against the nearest datastore; DS-4 is far below DS-2, so DS-2 is a source too.
- H is false: DS-3 (79.5%) is under the threshold, and datastores under the threshold are left alone.
- I is true: Fully Automated applies the recommendations.

## Notes
- Public source: Broadcom KB "Storage DRS FAQ" (https://knowledge.broadcom.com/external/article?legacyId=2149938, article 320864, no date shown): default space threshold 80%; thresholds configured on the cluster apply to each datastore; the space utilization difference threshold defaults to 5% (example: no move from an 83% to a 78% datastore); the space threshold is a soft constraint that Storage DRS violates only when no datastore in the cluster is below it. Broadcom TechDocs, vSphere Resource Management 9.0, "Initial Placement and Ongoing Balancing" (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/vsphere-resource-management/creating-a-datastore-cluster/initial-placement.html), last updated 2026-10-19: Storage DRS runs at the configured frequency (default eight hours) or when a datastore exceeds the space utilization threshold. VMware vSphere 8.0 Resource Management, "Storage DRS Aggressiveness" (the 82% / 79% example of the minimum difference), reached through the redirect from docs.vmware.com. Frank Denneman, "SDRS out of space avoidance" (https://frankdenneman.ai/2011-09-13-sdrs-out-of-space-avoidance/): Storage DRS avoids a destination expected to cross the threshold.
- Why this key: the per-datastore threshold, the 5% minimum difference and the soft-constraint rule together leave DS-4 as the only destination that stays under 80% for both sources. Thick disks remove the thin-provisioning and growth-rate effects. The prompt excludes the stuck state of Broadcom KB 438814 (all members above the threshold, or rules in conflict).
- Debatable risk: the amount moved depends on the VM sizes, so no option states it (the lower bound is 1.2 TB from DS-1 and 0.3 TB from DS-2). Whether one run produces recommendations for both sources is taken from the FAQ text on thresholds per datastore; the exact destination choice inside DS-4 is not asked.
- Options rewritten 2026-11-14 to the option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the five whole outcomes split into single facts (a setting question, so T4 and T5 do not apply); the stem's "so used space does not grow" removed (it interpreted the case). knowledge_main moved to the Storage DRS file. Key changed from B to A, F, I.
- Rewritten 2026-11-13 to raise difficulty: four unequal datastores instead of one full one; the minimum space utilization difference and the destination-after-move check decide which destinations are valid; the 5-point example of the FAQ is turned into a case where the nearest datastore is excluded but the farther one is not.

## Metadata
```yaml
id: "0310"
title: "Storage DRS: full datastore in a healthy cluster"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
object: [datastore]
tool: [vcenter]
knowledge:
  - vsphere/object-types/datastore-cluster/storage-drs
  - vsphere/object-types/datastore-cluster/datastore-cluster-alerts
knowledge_main: vsphere/object-types/datastore-cluster/storage-drs
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A, F, I]
misconception: [B, C, G]
misconception_type: [average-hides-worst]
status: draft
```
