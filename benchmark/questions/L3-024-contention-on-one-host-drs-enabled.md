# Contention on one host in a DRS cluster

## Prompt
- A fully automated DRS cluster has 6 hosts.
- For a week, VMs on host esx03 show CPU Ready of 6-9% per vCPU at the 20-second peak. The other 5 hosts are lightly used, and their VMs show Ready below 0.5%.
- The cluster state is green. No VM has a CPU limit.

Which statements about the cause are correct?

- A. Something stops DRS from moving VMs off esx03, such as a rule or a DRS override.
- B. The cluster is short of CPU: add a host to spread the load.
- C. The VMs on esx03 have CPU shares set too low for this host.
- D. A USB device mounted on one VM of esx03 keeps DRS from moving any VM off the host.

## Answers
A

## Explanation
- A is correct: contention on one host while the others are idle points to a DRS blocker: a VM/VM or VM/Host rule, DRS disabled for a VM, a mounted host device, a reservation too large for other hosts, incompatibility, vMotion not configured, a conservative threshold or unstable load. Remove the blocker, or move the threshold toward Aggressive, and check again.
- B is wrong: contention on all hosts would point to cluster capacity; here five hosts are lightly used, so balancing, not a host, is missing.
- C is wrong: shares act only under contention and decide who gets what; low shares do not create a host-wide wait, and the question is why DRS leaves the load on esx03.
- D is wrong: a mounted host device blocks the move of that VM only; DRS can still move the other VMs of esx03, so one such VM does not explain a week of contention on the host.
- Misconception: B: concluding that the cluster is short when only one host is hot.

## Notes
- Synthetic, 2026-11-05. Counts only after author approval.
- 2026-11-15 audit: D (a failing CPU, not decidable and picked by nobody) replaced by a blocker-scope option from the DRS blocker list; stem made plural without "most likely"; level 400 -> 300 (one interpretation line decides it).

## Metadata
```yaml
id: "0065"
title: "Contention on one host in a DRS cluster"
product: [vsphere]
technology: [system, cpu]
task: troubleshoot
level: 300
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/vm/troubleshooting/vm-insufficient-resources-in-drs-cluster
  - vsphere/object-types/cluster/concepts/drs-overview
knowledge_main: vsphere/object-types/vm/troubleshooting/vm-insufficient-resources-in-drs-cluster
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [B]
misconception_type: [average-hides-worst]
status: draft
```
