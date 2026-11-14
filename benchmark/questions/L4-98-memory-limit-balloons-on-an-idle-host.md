# Ballooning on a host with free memory

## Prompt
- A Linux VM named rpt-app-03 has 16 GB of configured memory, a memory reservation of 0 and Normal memory shares. In Edit Settings its memory limit shows Unlimited.
- The VM runs in the resource pool RP-Reporting. The pool tree is Cluster, RP-Tenants, RP-Reporting. RP-Tenants has no memory limit. RP-Reporting has a memory reservation of 0 (expandable) and a memory limit of 24,576 MB, set two years ago for a tenant contract.
- RP-Reporting holds three VMs of 16 GB, 16 GB and 8 GB configured memory (40 GB in total). They run on three different hosts of a DRS cluster.
- The host of rpt-app-03 has 512 GB of memory, about 40% of it consumed. The esxtop memory state of the host is high. No VM outside RP-Reporting shows Balloon or Swapped.
- Last 7 days for rpt-app-03: Granted about 15.4 GB, Balloon about 4.8 GB, Swapped about 2.1 GB, Compressed about 0.4 GB. The two other VMs of the pool also show Balloon and Swapped, less than rpt-app-03. The Consumed memory of the pool is flat at about 24.3 GB.
- Inside rpt-app-03, `free` reports 16 GB in total, almost nothing free, and 3 GB of guest swap in use. VMware Tools runs and the balloon driver is loaded. The application is slow.
- The application team asks for two changes: set sched.mem.maxmemctl to 0 on the VM so the balloon stops pushing the guest into swap, and move the VM with vMotion to a host that has even more free memory.

Which statements are correct?

- A. Host swapping happens only when the host itself runs short of memory, so here the Swapped counter must be wrong.
- B. The 24,576 MB limit on RP-Reporting is far below the 40 GB configured on its three VMs; the pool's Consumed is flat near it.
- C. The VM's own limit showing Unlimited does not rule out a limit: a limit on its parent or an ancestor pool also caps it.
- D. Linux cannot see the pool limit and runs as if all 16 GB were there, so ESX compresses and swaps to stay under it.
- E. Unlike shares, which act only under contention, a limit caps the pool's memory at all times, even on hosts with free memory.
- F. With sched.mem.maxmemctl at 0, reclamation on rpt-app-03 stops, because ESX then has no way left to take memory back.
- G. Host swapping picks pages without knowing which ones the guest needs, unlike a balloon, which lets the guest choose.
- H. Moving rpt-app-03 with vMotion to a host with more free memory ends the swapping of its memory.
- I. The expandable reservation of RP-Reporting lets the pool borrow memory from RP-Tenants above its 24,576 MB limit.
- J. Raise or remove the pool limit so it covers what its VMs need, or size the VMs to fit under it; check ancestor pools too.
- K. Put a memory limit on each of the three VMs, so that the pool's 24 GB is shared out fairly among them.
- L. Once the limit no longer binds, swapped and compressed pages return only as the guest touches them: Swapped falls slowly.
- M. The 3 GB of swap that Linux reports is the 2.1 GB Swapped that vCenter reports, measured from inside the guest.

## Likely wrong answer
- A: "The host is not short of memory and the VM limit is Unlimited, so the counters or the tools are wrong."
- F: "Turn the balloon driver off with sched.mem.maxmemctl."
- H: "vMotion the VM to a host with more free memory."

## Expected key points
- Answer: B, C, D, E, G, J, L.
- A false: with free host memory and no VM outside the pool reclaimed, swapping comes from a limit on the VM or its pool.
- B true: 24 GB against 40 GB configured (rpt-app-03 alone has 15.4 GB granted); the pool's Consumed is pinned at the cap.
- C true: the vendor's troubleshooting text names the VM, its parent pool or an ancestor pool as the place of a limit that is too restrictive.
- D true: a limit is not visible to the Guest OS; when Consumed tries to grow beyond it, the result is Compressed and Swapped memory.
- E true: shares act only when demand exceeds supply; a limit is an absolute cap, applied with free host memory too.
- F false: without the balloon, ESX still reclaims, by compression and host swapping; the memory above the limit must still go.
- G true: ballooning lets the guest choose; compression and host swapping pick pages without guest knowledge.
- H false: the limit belongs to the pool and follows the VM to any host; free memory on the target host does not matter.
- I false: an expandable reservation concerns admission of reservations from the parent; a limit is a separate cap that it does not lift.
- J true: the fix is the pool limit or the VMs' size; if the limit is a real contract, size the VMs to fit it.
- K false: VM limits are invisible to the guest and make performance unpredictable; rightsize instead.
- L true: compressed and swapped data stays out until the guest requests it; the slowness fades gradually.
- M false: host-level swapping is transparent to the guest and distinct from swapping inside the guest OS.

## Notes
- Public source: Broadcom KB 326270, "Impact of virtual machine memory and CPU resource limits" ("The guest operating system is not aware of this limit"; the Updated On field is empty). VMware vSphere 9.1 PDF (build of 2026-11-02): Monitoring and Performance, memory troubleshooting ("the virtual machine (or resource pool) has reached its resource limit"; the virtual machine, its parent pool or ancestor pools may have a limit that is too restrictive); Resource Management, advanced virtual machine attributes (sched.mem.maxmemctl: "If the ESX host needs to reclaim additional memory, it is forced to swap. Swapping is less desirable than ballooning").
- Open author question Q214 (does a memory limit cause ballooning): the knowledge base as written says a limit causes Compressed and Swapped, not Balloon directly. Following it, no option says where the Balloon of the pool's VMs comes from or whether it deflates after the fix; every option holds whichever way Q214 is answered. The old key's balloon-first mechanism (KB 326270) and the expectation that the balloon deflates were dropped for that reason. The prompt keeps the Balloon values as context.
- The way a cluster-wide pool limit is split across hosts is not documented in detail, so no option predicts which VM is hit hardest. No option compares the pool's Consumed with the exact limit: whether the effective limit includes overhead is open (Q205).
- Rewritten 2026-11-13 to raise difficulty: the cause moves from a VM limit shown in Edit Settings to a limit on the parent pool (VM shows Unlimited, VMs on three hosts); two plausible wrong fixes added (sched.mem.maxmemctl, vMotion); chart readings and guest counters added as distractors.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0291"
title: Ballooning on a host with free memory
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B, C, D, E, G, J, L]
misconception: [A, F, H]
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
