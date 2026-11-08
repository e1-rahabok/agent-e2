# Contention on one host in a DRS cluster

## Prompt
- A fully automated DRS cluster has 6 hosts.
- VMs on host esx03 show high CPU Ready. The other 5 hosts are lightly used.
- The cluster state is green. No VM has a CPU limit.

What is the most likely cause?

- A. A DRS blocker: for example a VM/Host rule, a mounted CD-ROM or USB device, a DRS override on the VMs, or a conservative migration threshold.
- B. The cluster is short of CPU capacity: add a host.
- C. The VMs' CPU shares are too low.
- D. esx03 has a faulty CPU.

## Likely wrong answer
B: concluding that the cluster is short when only one host is hot.

## Expected key points
- Answer: A.
- Contention on one host while the others are idle points to a DRS blocker; contention on all hosts would point to cluster capacity or shares.
- Blockers: VM/VM or VM/Host rules, DRS disabled for the VM, a mounted host device, a reservation too large for other hosts, incompatibility, vMotion not configured, a conservative threshold, unstable load.
- Remove the blocker, or move the migration threshold toward Aggressive, and check again.

## Notes
- Previous id: question-0065 (renamed 2026-11-05).
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
knowledge:
  - vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster
  - vsphere/object-types/cluster/concepts/drs-overview
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: draft
```
