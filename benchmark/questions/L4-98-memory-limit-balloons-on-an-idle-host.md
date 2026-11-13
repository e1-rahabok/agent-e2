# Ballooning on a host with free memory

## Prompt
- A Linux VM named rpt-app-03 has 16 GB of configured memory, a memory reservation of 0 and Normal memory shares. In Edit Settings its memory limit shows Unlimited.
- The VM runs in the resource pool RP-Reporting. The pool tree is Cluster, RP-Tenants, RP-Reporting. RP-Tenants has no memory limit. RP-Reporting has a memory reservation of 0 (expandable) and a memory limit of 24,576 MB, set two years ago for a tenant contract.
- RP-Reporting holds three VMs of 16 GB, 16 GB and 8 GB configured memory (40 GB in total). They run on three different hosts of a DRS cluster.
- The host of rpt-app-03 has 512 GB of memory, about 40% of it consumed. The esxtop memory state of the host is high. No VM outside RP-Reporting shows Balloon or Swapped.
- Last 7 days for rpt-app-03: Granted about 15.4 GB, Balloon about 4.8 GB, Swapped about 2.1 GB, Compressed about 0.4 GB. The two other VMs of the pool also show Balloon and Swapped, less than rpt-app-03. The Consumed memory of the pool is flat at about 24.3 GB.
- Inside rpt-app-03, `free` reports 16 GB in total, almost nothing free, and 3 GB of guest swap in use. VMware Tools runs and the balloon driver is loaded. The application is slow.
- The application team asks for two changes: set sched.mem.maxmemctl to 0 on the VM so the balloon stops pushing the guest into swap, and move the VM with vMotion to a host that has even more free memory.

What causes Balloon and Swapped on a host with this much free memory? Would the two requested changes help? What do you change, and what do you expect to see afterwards?

## Likely wrong answer
"Ballooning and swapping happen only when the host is short of memory, and the VM limit is Unlimited, so the counters or the VM tools are wrong." Or: "Turn the balloon driver off with sched.mem.maxmemctl, or vMotion the VM to a bigger host." Both miss the limit on the parent resource pool and the fact that a limit is enforced when the host has free memory.

## Expected key points
- Cause: the memory limit of the parent pool RP-Reporting (24 GB) is lower than the memory its three VMs touch (about 40 GB configured; Granted of rpt-app-03 alone is 15.4 GB). The VM's own limit of Unlimited does not rule this out: the vendor's troubleshooting text says that with free host memory and high swap or balloon, the VM, its parent pool or an ancestor pool has reached its limit. Unlike shares, a limit applies at all times.
- Mechanism: the limit caps the physical memory ESX gives to the VMs of the pool. The Guest OS does not know it (Linux sees 16 GB), so it keeps using memory above what the pool allows. The VMkernel then reclaims from the VMs: it inflates the balloon first, then compresses, then swaps (Broadcom KB 326270). That produces Balloon, Compressed and Swapped with a host in the high state. The evidence in the prompt fits: pool Consumed pinned at the limit, all VMs of the pool affected, no VM outside the pool affected, host state high.
- The first requested change does not help: setting sched.mem.maxmemctl to 0 stops ballooning, but the memory above the limit must still be reclaimed. The vendor says that then the host is forced to swap, which is less desirable than ballooning, and host swapping picks pages blind to what the guest needs.
- The second requested change does not help: the limit belongs to the pool and travels with the VM. Free memory on the target host is not relevant.
- Fix: raise or remove the pool limit so it covers the combined demand of its VMs, or right-size the VMs so their working sets fit under it. If the limit is a real contract, size the VMs to fit it; do not add VM limits. Check the ancestor pools too.
- Expect: the balloon deflates once the VMs are no longer over the limit. Swapped and compressed pages come back only when the guest touches them, so the slowness fades gradually, and the guest swap in use stays until the pages are touched again or swap is emptied.

## Notes
- Public source: Broadcom KB 326270, "Impact of virtual machine memory and CPU resource limits" (limit below configured memory: "The VMkernel first tries to reclaim memory by inflating the Balloon Driver", then compression, then swap; "The guest operating system is not aware of this limit"; the Updated On field is empty). VMware vSphere 9.1 PDF (build of 2026-11-02): Monitoring and Performance, memory troubleshooting ("the virtual machine (or resource pool) has reached its resource limit"; the virtual machine, its parent pool or ancestor pools may have a limit that is too restrictive); Resource Management, advanced virtual machine attributes (sched.mem.maxmemctl: "If the ESX host needs to reclaim additional memory, it is forced to swap. Swapping is less desirable than ballooning").
- Why one answer: the vendor names the pool limit as a cause of balloon and swap on a host with free memory, and the prompt shows the pool limit below the combined memory of its VMs. The two requested changes have no effect on a limit that belongs to the pool.
- Debatable risk: the knowledge file ballooned.md says a limit causes Swapped and Compressed, not Balloon directly; the vendor KB says balloon comes first (author question Q014 is open). The key follows the vendor KB and the prompt shows a non-zero Balloon. The way a cluster-wide pool limit is split across hosts is not documented in detail, so the key does not predict which VM is hit hardest.
- Rewritten 2026-11-13 to raise difficulty: the cause moves from a VM limit shown in Edit Settings to a limit on the parent pool (VM shows Unlimited, VMs on three hosts); two plausible wrong fixes added (sched.mem.maxmemctl, vMotion); chart readings and guest counters added as distractors.

## Metadata
```yaml
id: "0291"
title: Ballooning on a host with free memory
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [vm, esxi, resource-pool]
tool: [vcenter]
knowledge:
  - vsphere/object-types/vm/configuration/resource-settings-guidance
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/object-types/resource-pool/resource-pool-design
knowledge_main: vsphere/object-types/vm/configuration/resource-settings-guidance
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention, consumption-as-contention]
status: draft
```
