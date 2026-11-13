# Storage DRS: full datastore in a healthy cluster

## Prompt
- A datastore cluster has four datastores of 10 TB each. Used space: 9.2 TB, 7.5 TB, 6.0 TB and 5.5 TB (the cluster as a whole is 70.5% used).
- Storage DRS is enabled with the automation level Fully Automated. I/O metric inclusion is off.
- No VM or VMDK affinity or anti-affinity rules are defined, and every VM is small compared with the free space of the other three datastores.
- The space utilization threshold and the minimum space utilization difference are at their defaults.

What does Storage DRS do about the datastore that is 92% used?

- A. Nothing: it compares the used space of the whole datastore cluster (70.5%) with the space utilization threshold, which it has not reached.
- B. It compares each datastore with the space utilization threshold. The 92% datastore is over it, so Storage DRS generates Storage vMotion recommendations to move VMs to datastores with enough lower utilization, and applies them because the cluster is Fully Automated.
- C. Nothing for space: Storage DRS balances only I/O latency after a VM is placed, and uses space only for initial placement.
- D. It raises an alarm and leaves the VMs where they are: Storage DRS never migrates a VM for space, even in Fully Automated mode.
- E. It moves VMs until all four datastores are at the cluster average of 70.5%.

## Likely wrong answer
A: a datastore cluster is treated as one pool of space, so the cluster average is compared with the threshold. Or E: Storage DRS is assumed to balance until all members are equal.

## Expected key points
- Answer: B.
- The thresholds are set on the datastore cluster but apply to each datastore in it. A datastore over the space utilization threshold is a reason for Storage DRS to recommend migrations, whatever the cluster average is.
- Storage DRS runs at its configured interval (default every eight hours) and also when a datastore exceeds the space utilization threshold.
- The default space utilization threshold is 80%, so 92% is over it.
- It moves enough VMs to bring the datastore back under the threshold, to datastores that are sufficiently less utilized (the minimum space utilization difference). It does not level all datastores to the average.
- Fully Automated applies the recommendations; Storage DRS recommends space migrations as well as initial placement.

## Notes
- Public source: Broadcom TechDocs, vSphere Resource Management 9.0, "Initial Placement and Ongoing Balancing" (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/vsphere-resource-management/creating-a-datastore-cluster/initial-placement.html), page last updated 2026-10-19 as shown. It states that Storage DRS is invoked at the configured frequency (by default every eight hours) or when one or more datastores exceed the user-configurable space utilization thresholds, and that it checks each datastore's space utilization. The defaults (80% space threshold, 5% minimum space utilization difference) are in Broadcom KB "Storage DRS FAQ" (https://knowledge.broadcom.com/external/article/320864/storage-drs-faq.html, no date shown, written for vSphere 5.x onward, thresholds are effective on each datastore inside the cluster).
- Why one answer: the vendor documents that the check is made per datastore, so the cluster average cannot be the test; E contradicts the minimum space utilization difference and the threshold logic.
- Debatable risk: the 80% default comes from the FAQ, not from a 9.0 page. Broadcom KB 438814 describes a stuck state at 99% with several full datastores or affinity conflicts; the prompt excludes those (one over-threshold datastore, no rules, small VMs, I/O metric off).

## Metadata
```yaml
id: "0310"
title: "Storage DRS: full datastore in a healthy cluster"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 300
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
misconception: [A, E]
misconception_type: [average-hides-worst]
status: draft
```
