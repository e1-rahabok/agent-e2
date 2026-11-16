# Storage DRS: full datastore in a healthy cluster

## Prompt
- A vSphere 9.1 datastore cluster has four VMFS datastores of 10 TB each. Used space: DS-1 9.2 TB (92%), DS-2 8.3 TB (83%), DS-3 7.95 TB (79.5%) and DS-4 4.0 TB (40%). The cluster as a whole is 29.45 TB of 40 TB used (73.6%).
- Storage DRS is enabled with the automation level Fully Automated.
- The space utilization threshold and the minimum space utilization difference are at their defaults. The aggressiveness level was not changed.
- No VM or VMDK affinity or anti-affinity rules are defined, and no datastore is in maintenance mode.
- Every VM has one thick-provisioned virtual disk of 200 GB to 600 GB.
- A Storage DRS run starts now.

Which statements about this Storage DRS run are correct?

- A. DS-1 gives up disks in this run.
- B. Storage DRS compares the datastore cluster's 73.6% with the space utilization threshold.
- C. Disks move until all four datastores sit near the cluster average of 73.6%.
- D. DS-3 receives disks from DS-2.
- E. DS-3 receives disks from DS-1.
- F. DS-4 receives disks in this run.
- G. DS-2 keeps all its disks in this run.
- H. DS-3 gives up disks in this run.
- I. The moves are applied without an administrator approving them.
- J. Storage DRS also moves disks off DS-1 if its I/O latency is high.

## Likely wrong answer
B (the cluster average is compared with the threshold), C (Storage DRS levels all members to the average), or G (a source is skipped when the nearest datastore is within the minimum difference).

## Expected key points
- Answer: A, F, I.
- A is correct: the thresholds are set on the datastore cluster but apply to each datastore. DS-1 (92%) is over the default 80% space utilization threshold, so it is a source.
- B is wrong: the threshold is set on the datastore cluster but checked against each member datastore; an average hides a full member, so DS-1 and DS-2 (over 80%) are sources whatever the 73.6%.
- C is wrong: Storage DRS moves enough disks to bring each source back under the threshold; it does not level the members to the average.
- D is wrong: a destination must be more than the default minimum space utilization difference (5 points) below the source. DS-2 (83%) to DS-3 (79.5%) is 3.5 points.
- E is wrong: DS-1 to DS-3 passes the difference (12.5 points), but a destination must stay under the threshold after the move. DS-3 has 0.05 TB of room under 80% and the smallest virtual disk is 200 GB.
- F is correct: DS-4 (40%) passes the difference for both sources and stays under 80% after taking 1.5 TB or more.
- G is wrong: DS-2 (83%) is over the threshold, so it is a source. The difference is checked per source and destination pair, not against the nearest datastore: DS-3 is within 5 points, but DS-4 is far below DS-2.
- H is wrong: DS-3 (79.5%) is under the threshold; being above the cluster average does not make it a source, as datastores under the threshold are left alone.
- I is correct: Fully Automated applies the recommendations.
- J is wrong: in vSphere 9.1 Storage DRS balances space only; I/O load balancing is gone (Storage I/O Control components deprecated from VCF 9.0).

## Notes
- Public source: Broadcom KB "Storage DRS FAQ" (https://knowledge.broadcom.com/external/article?legacyId=2149938, article 320864, no date shown): default space threshold 80%; thresholds configured on the cluster apply to each datastore; the space utilization difference threshold defaults to 5% (example: no move from an 83% to a 78% datastore); the space threshold is a soft constraint that Storage DRS violates only when no datastore in the cluster is below it. Broadcom TechDocs, vSphere Resource Management 9.0, "Initial Placement and Ongoing Balancing" (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/vsphere-resource-management/creating-a-datastore-cluster/initial-placement.html), last updated 2026-10-19: Storage DRS runs at the configured frequency (default eight hours) or when a datastore exceeds the space utilization threshold. VMware vSphere 8.0 Resource Management, "Storage DRS Aggressiveness" (the 82% / 79% example of the minimum difference), reached through the redirect from docs.vmware.com. Frank Denneman, "SDRS out of space avoidance" (https://frankdenneman.ai/2011-09-13-sdrs-out-of-space-avoidance/): Storage DRS avoids a destination expected to cross the threshold.
- Why this key: the per-datastore threshold, the 5% minimum difference and the soft-constraint rule together leave DS-4 as the only destination that stays under 80% for both sources. Thick disks remove the thin-provisioning and growth-rate effects. The prompt excludes the stuck state of Broadcom KB 438814 (all members above the threshold, or rules in conflict).
- Debatable risk: the amount moved depends on the VM sizes, so no option states it (the lower bound is 1.2 TB from DS-1 and 0.3 TB from DS-2). Whether one run produces recommendations for both sources is taken from the FAQ text on thresholds per datastore; the exact destination choice inside DS-4 is not asked.
- The stem gives one disk per VM with its size, so option E is decidable.
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- 2026-11-15 audit: "I/O metric inclusion is off" removed (the setting is gone in 9.x; knowledge file storage-drs); vSphere 9.1 named in the stem; the reason clauses left G and H (they sat only in wrong options); J added (I/O balancing, false in 9.1).

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
source_path: "Synthetic, 2026-11-13"
answer: [A, F, I]
misconception: [B, C, G]
misconception_type: [average-hides-worst]
status: draft
```
