# Contention on one host in a DRS cluster

## Prompt
- A fully automated DRS cluster has 6 hosts.
- For a week, VMs on host esx03 show CPU Ready of 6-9% per vCPU at the 20-second peak. The other 5 hosts are lightly used, and their VMs show Ready below 0.5%.
- The cluster state is green. No VM has a CPU limit.

What is the most likely cause?

- A. Something stops DRS from moving VMs off esx03, such as a rule or a DRS override.
- B. The cluster is short of CPU: add a host to spread the load.
- C. The VMs on esx03 have CPU shares set too low for this host.
- D. A failing CPU on esx03 slows the VMs that run on it.

## Likely wrong answer
B: concluding that the cluster is short when only one host is hot.

## Expected key points
- Answer: A.
- Contention on one host while the others are idle points to a DRS blocker; contention on all hosts would point to cluster capacity or shares.
- Blockers: VM/VM or VM/Host rules, DRS disabled for the VM, a mounted host device, a reservation too large for other hosts, incompatibility, vMotion not configured, a conservative threshold, unstable load.
- Remove the blocker, or move the migration threshold toward Aggressive, and check again.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0065"
title: "Contention on one host in a DRS cluster"
product: [vsphere]
technology: [system, cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster
  - vsphere/object-types/cluster/concepts/drs-overview
knowledge_main: vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A]
misconception: [B]
misconception_type: [average-hides-worst]
status: draft
```
