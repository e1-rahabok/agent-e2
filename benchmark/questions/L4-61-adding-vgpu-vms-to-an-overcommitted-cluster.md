# Adding vGPU VMs to a memory-overcommitted cluster

## Prompt
- A cluster of 4 ESXi 9.1 hosts, 1 TB of memory each, no memory tiering. HA admission control: cluster resource percentage, 25% for one host failure.
- Today it runs 4.8 TB of configured VM memory, none of it reserved. Host Consumed is about 55% on each host. No balloon, compression or swap.
- The plan: add 12 AI inference VMs with a vGPU each, 128 GB of memory per VM (1.5 TB in total). The GPUs fit.
- The capacity manager says: "Consumed is 55%, so about 1.8 TB is free. The 1.5 TB of new VMs fit, with HA admission control green."

Is the capacity manager right, and what changes for the existing VMs, in normal operation and after a host failure? Which statements are correct?

- A. Each vGPU VM gets a full memory reservation, and all its memory is allocated at power-on, whatever its guest uses.
- B. The memory of the vGPU VMs is backed only as their guests touch it, like an ordinary reservation, so they add only what they use.
- C. The reserved memory of the vGPU VMs is never ballooned, compressed or swapped: later shortages hit the existing VMs alone.
- D. The existing 4.8 TB of configured memory is then backed by about 2.5 TB, an overcommit of about 1.9:1 instead of 1.2:1.
- E. In normal operation Consumed rises to about 3.7 TB of 4 TB, about 92%, which leaves about 300 GB for growth.
- F. The capacity manager is right: 1.8 TB is free, the new VMs need 1.5 TB, and admission control is green, so the cluster has room.
- G. After a host failure 3 TB remain; with 1.5 TB reserved, the existing VMs have about 1.5 TB for the 2.2 TB they consume today.
- H. HA admission control stays green because it counts reservations and overhead, and the existing VMs reserve nothing.
- I. HA admission control keeps enough capacity for the Consumed memory of the existing VMs after a host failure.
- J. HA admission control refuses the vGPU VMs, because their 1.5 TB of reservations exceed the 25% kept for failover (1 TB).
- K. After a host failure, ESXi can balloon the vGPU VMs to make room for the existing VMs they share hosts with.
- L. Running the vGPU VMs on hosts or a cluster of their own keeps their reservations out of the memory the existing VMs share.

## Likely wrong answer
- F: "Yes: 1.8 TB is free, the new VMs need 1.5 TB, and admission control is green, so the cluster has room."
- I: "HA admission control is green, so the cluster survives a host failure."

## Expected key points
- Answer: A, C, D, E, G, H, L.
- A true: a VM with a vGPU (a PCI device) is fully reserved automatically; the device reads and writes guest memory directly, so every page is backed from power-on.
- B false: unlike an ordinary reservation, the memory of a passthrough or vGPU VM is allocated at power-on and shows as Consumed whatever the guest uses.
- C true: reserved memory leaves the reclaimable pool; only the unreserved VMs can be reclaimed.
- D true: 4 TB - 1.5 TB = 2.5 TB for 4.8 TB configured (about 1.92:1), against 4.8 / 4 = 1.2:1 today.
- E true: 55% of 4 TB = 2.2 TB, plus 1.5 TB = 3.7 TB (92.5%). Any growth of the existing VMs runs into balloon, compression and swap.
- F false: right only for today in normal operation; no room for growth, and a host failure hurts the existing VMs.
- G true: 3 TB - 1.5 TB = 1.5 TB for 2.2 TB of Consumed (and 4.8 TB configured): heavy reclamation for the existing VMs.
- H true: the percentage policy sums reservations plus overhead; unreserved VMs pass whatever their size or usage.
- I false: admission control does not see the usage of the unreserved VMs; check memory after a failure as remaining capacity minus all reservations, against their Consumed.
- J false: with the percentage policy the reservations are compared with the capacity left after the failover percentage (3 TB), not with the percentage itself; 1.5 TB fits.
- K false: vGPU VMs are fully reserved; nothing is reclaimed from them.
- L true: one of the options, with more memory or fewer existing VMs: decide on the reserved memory plus what the other VMs need.

## Notes
- Sources: the knowledge base, GPU monitoring, section vGPU and host memory (full reservation, never reclaimed, counted in full by admission control, excluded from memory tiering); vSphere 9.1 documentation, vSphere Resource Management (PCI passthrough and vGPU VMs require a full memory reservation) and vSphere Availability, Cluster Resources Percentage.
- Arithmetic: today Consumed 55% of 4 TB = 2.2 TB; plus 1.5 TB = 3.7 TB (92.5%). 4 TB - 1.5 TB = 2.5 TB for 4.8 TB configured (1.92:1); after a failure 3 TB - 1.5 TB = 1.5 TB for 2.2 TB consumed. Overhead ignored.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0150"
title: "Adding vGPU VMs to a memory-overcommitted cluster"
product: [vsphere]
technology: [memory, system]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,D,E,G,H,L]
misconception: [F,I]
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
