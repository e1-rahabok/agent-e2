# Adding vGPU VMs to a memory-overcommitted cluster

## Prompt
- A cluster of 4 ESXi 9.1 hosts, 1 TB of memory each, no memory tiering. HA admission control: cluster resource percentage, 25% for one host failure.
- Today it runs 4.8 TB of configured VM memory, none of it reserved. Host Consumed is about 55% on each host. No balloon, compression or swap.
- The plan: add 12 AI inference VMs with a vGPU each, 128 GB of memory per VM (1.5 TB in total). The GPUs fit, also with one host down.
- The capacity manager says: "Consumed is 55%, so about 1.8 TB is free. The 1.5 TB of new VMs fit, with HA admission control green."

Is the capacity manager right, and what changes for the existing VMs, in normal operation and after a host failure? Which statements are correct?

- A. Each vGPU VM gets a full memory reservation, and all its memory is allocated at power-on, whatever its guest uses.
- B. The reservation of a vGPU VM counts against HA admission control only; the host's own power-on check leaves it out.
- C. The reserved memory of the vGPU VMs is never ballooned, compressed or swapped: later shortages hit the existing VMs alone.
- D. The existing 4.8 TB of configured memory is then backed by about 2.5 TB, an overcommit of about 1.9:1 instead of 1.2:1.
- E. In normal operation Consumed rises to about 3.7 TB of 4 TB, about 92%, which leaves about 300 GB for growth.
- F. The capacity manager is right: 1.8 TB is free, the new VMs need 1.5 TB, and admission control is green, so the cluster has room.
- G. After a host failure 3 TB remain; with 1.5 TB reserved, the existing VMs have about 1.5 TB for the 2.2 TB they consume today.
- H. If memory tiering is turned on later, the memory of the vGPU VMs stays in DRAM and never moves to the NVMe tier.
- I. HA admission control keeps enough capacity for the Consumed memory of the existing VMs after a host failure.
- J. HA admission control refuses the vGPU VMs, because their 1.5 TB of reservations exceed the 25% kept for failover (1 TB).
- K. After a host failure, ESXi can balloon the vGPU VMs to make room for the existing VMs they share hosts with.
- L. Running the vGPU VMs in a cluster of their own keeps their reservations out of the memory the existing VMs share.

## Answers
A, C, D, E, G, H, L

## Explanation
- A true: a VM with a vGPU (a PCI device) is fully reserved automatically; the device reads and writes guest memory directly, so every page is backed from power-on. Unlike an ordinary reservation, which is backed as the guest touches pages, it shows as Consumed whatever the guest uses.
- B false: the full reservation of a vGPU VM counts in full against host, resource pool and HA admission control.
- C true: reserved memory leaves the reclaimable pool; only the unreserved VMs can be reclaimed.
- D true: 4 TB - 1.5 TB = 2.5 TB for 4.8 TB configured (about 1.92:1), against 4.8 / 4 = 1.2:1 today.
- E true: 55% of 4 TB = 2.2 TB, plus 1.5 TB = 3.7 TB (92.5%). Any growth of the existing VMs runs into balloon, compression and swap.
- F false: right only for today in normal operation; no room for growth, and a host failure hurts the existing VMs.
- G true: 3 TB - 1.5 TB = 1.5 TB for 2.2 TB of Consumed (and 4.8 TB configured): heavy reclamation for the existing VMs.
- H true: a vGPU VM is excluded from memory tiering and stays in DRAM: the device reads and writes guest memory directly, so every page stays backed and in place.
- I false: the percentage policy sums reservations plus overhead, so it does not see the usage of the unreserved VMs; check memory after a failure as remaining capacity minus all reservations, against their Consumed.
- J false: with the percentage policy the reservations are compared with the capacity left after the failover percentage (3 TB), not with the percentage itself; 1.5 TB fits.
- K false: vGPU VMs are fully reserved; nothing is reclaimed from them.
- L true: a separate cluster keeps the reservations out of the reclaimable pool of the existing VMs (hosts kept apart by rules inside one HA cluster are weaker, as HA failover can still mix them); one of the options, with more memory or fewer existing VMs.
- Misconception: F: "Yes: 1.8 TB is free, the new VMs need 1.5 TB, and admission control is green, so the cluster has room." - J: "The vGPU VMs reserve 1.5 TB, more than the 1 TB kept for failover, so HA admission control refuses them."

## Notes
- Sources: the knowledge base, GPU monitoring, section vGPU and host memory (full reservation, never reclaimed, counted in full by admission control, excluded from memory tiering); vSphere 9.1 documentation, vSphere Resource Management (PCI passthrough and vGPU VMs require a full memory reservation) and vSphere Availability, Cluster Resources Percentage.
- Arithmetic: today Consumed 55% of 4 TB = 2.2 TB; plus 1.5 TB = 3.7 TB (92.5%). 4 TB - 1.5 TB = 2.5 TB for 4.8 TB configured (1.92:1); after a failure 3 TB - 1.5 TB = 1.5 TB for 2.2 TB consumed. Overhead ignored.
- Review 2026-11-14: the prompt now says the GPUs fit with one host down, so option G (all 1.5 TB reserved after a failure) does not depend on GPU capacity.
- 2026-11-16 re-review: B (backed only as touched) negated A; replaced in place with the host admission check (false; gpu-monitoring, vGPU and host memory). L stays: it follows from the reclaimable-pool sentence of the same section; no file names a separate cluster.
- Audit 2026-11-15: H (HA admission counts reservations plus overhead) was over the two-question cap (0290, 0355 keep it) and was replaced with the memory tiering fact of the same file; the misconception moved from I to J (gpu-monitoring Misconceptions); L names a separate cluster only.

## Metadata
```yaml
id: "0150"
title: "Adding vGPU VMs to a memory-overcommitted cluster"
product: [vsphere]
technology: [memory, system]
task: decide-capacity
level: 400
answer_type: deterministic
misconception: [F,J]
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
source_path: "Synthetic, 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
