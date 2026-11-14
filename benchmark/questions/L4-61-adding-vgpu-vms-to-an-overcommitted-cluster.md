# Adding vGPU VMs to a memory-overcommitted cluster

## Prompt
- A cluster of 4 ESXi 9.1 hosts, 1 TB of memory each, no memory tiering. HA admission control: cluster resource percentage, 25% for one host failure.
- Today it runs 4.8 TB of configured VM memory, none of it reserved. Host Consumed is about 55% on each host. No balloon, compression or swap.
- The plan: add 12 AI inference VMs with a vGPU each, 128 GB of memory per VM (1.5 TB in total). The GPUs fit.
- The capacity manager says: "Consumed is 55%, so about 1.8 TB is free. The 1.5 TB of new VMs fit, with HA admission control green."

Is the capacity manager right? What changes for the existing VMs, in normal operation and after a host failure?

## Likely wrong answer
"Yes: 1.8 TB is free, the new VMs need 1.5 TB, and admission control is green, so the cluster has room."

## Expected key points
- A VM with a vGPU (a PCI device) gets a full memory reservation automatically, and its memory is allocated at power-on: 1.5 TB plus overhead is held whatever the VMs use.
- Reserved memory is never ballooned, compressed or swapped. The existing 4.8 TB of configured memory can then be backed only by the rest: about 2.5 TB of 4 TB, an overcommit of about 1.9:1 instead of 1.2:1.
- Normal operation fits: Consumed rises to about 3.7 TB of 4 TB (about 92%), with about 300 GB left. Any growth of the existing VMs runs into balloon, compression and swap, because only they can be reclaimed.
- After a host failure, 3 TB remain; with 1.5 TB reserved, the existing VMs get about 1.5 TB for the 2.2 TB they consume today (and 4.8 TB configured): heavy reclamation for them.
- Admission control stays green because it counts reservations, not usage: the existing VMs have none, so it does not see their need.
- Conclusion: the manager is right only for today, in normal operation. There is no room for growth, and the cluster does not survive a host failure without hurting the existing VMs. Decide on reserved memory plus what the other VMs need; options: separate hosts or a cluster for the vGPU VMs, more memory, or fewer existing VMs.

## Notes
- Sources: the knowledge base, GPU monitoring, section vGPU and host memory (full reservation, never reclaimed, counted in full by admission control, excluded from memory tiering); vSphere 9.1 documentation, vSphere Resource Management (PCI passthrough and vGPU VMs require a full memory reservation) and vSphere Availability, Cluster Resources Percentage.
- Arithmetic: today Consumed 55% of 4 TB = 2.2 TB; plus 1.5 TB = 3.7 TB (92.5%). 4 TB - 1.5 TB = 2.5 TB for 4.8 TB configured (1.92:1); after a failure 3 TB - 1.5 TB = 1.5 TB for 2.2 TB consumed. Overhead ignored.

## Metadata
```yaml
id: "0150"
title: "Adding vGPU VMs to a memory-overcommitted cluster"
product: [vsphere]
technology: [memory, system]
task: decide-capacity
level: 400
answer_type: judged
input: [text]
object: [cluster, vm]
tool: [none]
knowledge:
  - vsphere/technology/gpu/gpu-monitoring
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/gpu/gpu-monitoring
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
