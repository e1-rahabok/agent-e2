# Storage DRS: full datastore in a healthy cluster

## Prompt
- A datastore cluster has four VMFS datastores of 10 TB each. Used space: DS-1 9.2 TB (92%), DS-2 8.3 TB (83%), DS-3 7.95 TB (79.5%) and DS-4 4.0 TB (40%). The cluster as a whole is 29.45 TB of 40 TB used (73.6%).
- Storage DRS is enabled with the automation level Fully Automated. I/O metric inclusion is off.
- The space utilization threshold and the minimum space utilization difference are at their defaults. The aggressiveness level was not changed.
- No VM or VMDK affinity or anti-affinity rules are defined, and no datastore is in maintenance mode.
- All VMs use thick-provisioned disks on one datastore each, so used space does not grow. Every VM is between 200 GB and 600 GB.
- A Storage DRS run starts now.

What does Storage DRS recommend, and apply, in this run?

- A. Nothing: it compares the used space of the whole datastore cluster (73.6%) with the space utilization threshold, which it has not reached.
- B. It moves VMs out of DS-1 and DS-2 into DS-4 only, at least enough to bring both back under 80% (1.5 TB in total or more). DS-3 receives nothing.
- C. It moves VMs out of DS-1, DS-2 and DS-3 into DS-4 until all four datastores are close to the cluster average of 73.6% (about 3.4 TB in total).
- D. It moves VMs out of DS-1 and DS-2 into DS-3 and DS-4, split by free space, because every datastore under 80% is a valid destination.
- E. It moves VMs out of DS-1 only, into DS-4. DS-2 is left alone because the nearest datastore below it, DS-3, is within the minimum space utilization difference.

## Likely wrong answer
A (the cluster average is compared with the threshold), C (Storage DRS levels all members to the average), or D (any datastore under the threshold is a destination, with no minimum difference and no check of what the destination looks like after the move).

## Expected key points
- Answer: B.
- The thresholds are set on the datastore cluster but apply to each datastore. DS-1 (92%) and DS-2 (83%) are over the default 80% space utilization threshold, so the 73.6% average does not matter (A is wrong).
- Storage DRS moves enough VMs to bring a source back under the threshold. It does not level the members to the average (C is wrong).
- A destination must be sufficiently less utilized than the source: the default minimum space utilization difference is 5%. DS-2 (83%) to DS-3 (79.5%) is 3.5 points, so it is not allowed.
- DS-1 to DS-3 passes the difference (12.5 points) but fails the other test: DS-3 has 0.05 TB of room under 80% and the smallest VM is 200 GB, so any move would push it over the threshold. DS-4 is the only destination that stays under it (D is wrong).
- DS-2 is a valid source because DS-4 is far below it. The difference check is made per source and destination pair, not against the nearest datastore (E is wrong).
- Fully Automated applies the recommendations.

## Notes
- Public source: Broadcom KB "Storage DRS FAQ" (https://knowledge.broadcom.com/external/article?legacyId=2149938, article 320864, no date shown): default space threshold 80%; thresholds configured on the cluster apply to each datastore; the space utilization difference threshold defaults to 5% (example: no move from an 83% to a 78% datastore); the space threshold is a soft constraint that Storage DRS violates only when no datastore in the cluster is below it. Broadcom TechDocs, vSphere Resource Management 9.0, "Initial Placement and Ongoing Balancing" (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/vsphere-resource-management/creating-a-datastore-cluster/initial-placement.html), last updated 2026-10-19: Storage DRS runs at the configured frequency (default eight hours) or when a datastore exceeds the space utilization threshold. VMware vSphere 8.0 Resource Management, "Storage DRS Aggressiveness" (the 82% / 79% example of the minimum difference), reached through the redirect from docs.vmware.com. Frank Denneman, "SDRS out of space avoidance" (https://frankdenneman.ai/2011-09-13-sdrs-out-of-space-avoidance/): Storage DRS avoids a destination expected to cross the threshold.
- Why one answer: the per-datastore threshold, the 5% minimum difference and the soft-constraint rule together leave DS-4 as the only destination that stays under 80% for both sources. Thick disks remove the thin-provisioning and growth-rate effects. The prompt excludes the stuck state of Broadcom KB 438814 (all members above the threshold, or rules in conflict).
- Debatable risk: the amount moved depends on the VM sizes; option B says "at least" and gives only the lower bound (1.2 TB from DS-1 and 0.3 TB from DS-2). Whether one run produces recommendations for both sources is taken from the FAQ text on thresholds per datastore; the exact destination choice inside DS-4 is not asked.
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
  - vsphere/object-types/datastore-cluster/datastore-cluster-alerts
  - vsphere/object-types/datastore/datastore-alerts
knowledge_main: vsphere/object-types/datastore-cluster/datastore-cluster-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [A, C, D]
misconception_type: [average-hides-worst]
status: draft
```
