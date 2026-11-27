# Ballooning on a host with free memory

## Prompt
- A Linux VM named rpt-app-03 has 16 GB of configured memory, a memory reservation of 0 and Normal memory shares. In Edit Settings its memory limit shows Unlimited.
- The VM runs in the resource pool RP-Reporting. The pool tree is Cluster, RP-Tenants, RP-Reporting. RP-Tenants has no memory limit. RP-Reporting has a memory reservation of 0 (expandable) and a memory limit of 24,576 MB, set two years ago for a tenant contract.
- RP-Reporting holds three VMs of 16 GB, 16 GB and 8 GB configured memory (40 GB in total). They run on three different hosts of a DRS cluster.
- The host of rpt-app-03 has 512 GB of memory, about 40% of it consumed. The esxtop memory state of the host is high. No VM outside RP-Reporting shows Balloon or Swapped.
- Last 7 days for rpt-app-03: Granted about 8 GB, Balloon about 4.8 GB, Swapped about 2.1 GB, Compressed about 0.4 GB. The two other VMs of the pool also show Balloon and Swapped, less than rpt-app-03. The Consumed memory of the pool is flat at about 23.9 GB.
- Inside rpt-app-03, `free` reports 16 GB in total, almost nothing free, and 3 GB of guest swap in use. VMware Tools runs and the balloon driver is loaded. The application is slow.
- The application team asks for two changes: set sched.mem.maxmemctl to 0 on the VM so the balloon stops pushing the guest into swap, and move the VM with vMotion to a host that has even more free memory.

Which statements are correct?

- A. Host swapping needs a host that is short of memory, so on this host the Swapped counter is suspect.
- B. The 24,576 MB limit on RP-Reporting is far below the 40 GB of its three VMs; the pool's Consumed is flat near it.
- C. The VM's own limit showing Unlimited does not rule out a limit: a limit on a parent or ancestor pool also caps it.
- D. Linux cannot see the pool limit and fills all 16 GB, so ESX must reclaim memory to keep the pool under it.
- E. Unlike shares, which act only under contention, a limit caps the pool's memory at all times, even with free host memory.
- F. With sched.mem.maxmemctl at 0, reclamation on rpt-app-03 stops, because ESX then has no way left to take memory back.
- G. Host swapping picks pages without knowing which ones the guest needs, unlike a balloon, which lets the guest choose.
- H. Moving rpt-app-03 with vMotion to a host with more free memory ends the host swapping of its memory pages.
- I. The expandable reservation of RP-Reporting lets the pool borrow memory from RP-Tenants above its 24,576 MB limit.
- J. Raise or remove the pool limit to what its VMs need, or size the VMs to fit under it; check ancestor pools too.
- K. Put a memory limit on each of the three VMs, so that the pool's 24 GB is shared out fairly among the three of them.
- L. At the default ceiling of 65% of configured memory, the balloon of rpt-app-03 could hold up to about 10.4 GB.
- M. The 3 GB of swap that Linux reports is the 2.1 GB Swapped that vCenter reports, measured from inside the guest.
- N. The 4.8 GB balloon cannot come from the pool limit, since a limit is enforced by compression and host swapping.

## Answers
B, C, D, E, G, J, L

## Explanation
- A false: a limit is enforced at all times, also on a host with free memory; with no VM outside the pool reclaimed, the swapping comes from a limit on the VM or its pool.
- B true: 24 GB against 40 GB configured on the pool's three VMs; the pool's Consumed is flat just under the cap.
- C true: the vendor's troubleshooting text names the VM, its parent pool or an ancestor pool as the place of a limit that is too restrictive.
- D true: a limit is not visible to the Guest OS, which fills its configured memory; ESX reclaims the excess, balloon first while the driver runs, then compression and host swapping for what the balloon cannot take in time or above its ceiling.
- E true: shares act only when demand exceeds supply; a limit is an absolute cap, applied with free host memory too.
- F false: without the balloon, ESX still reclaims, by compression and host swapping; the memory above the limit must still go.
- G true: ballooning lets the guest choose; compression and host swapping pick pages without guest knowledge.
- H false: the limit belongs to the pool and follows the VM to any host; free memory on the target host does not matter.
- I false: an expandable reservation concerns admission of reservations from the parent; a limit is a separate cap that it does not lift.
- J true: the fix is the pool limit or the VMs' size; if the limit is a real contract, size the VMs to fit it.
- K false: VM limits are invisible to the guest and make performance unpredictable; rightsize instead.
- L true: the balloon ceiling is 65% of configured memory by default (Mem.CtlMaxPercent, or sched.mem.maxmemctl per VM): 0.65 x 16 GB = 10.4 GB.
- M false: host-level swapping is transparent to the guest and distinct from swapping inside the guest OS.
- N false: under a limit the balloon goes first when the driver runs; compression and swapping take over when it cannot reclaim enough. The driver is loaded here, so the pool limit explains the balloon too.
- Misconception: A: "The host is not short of memory and the VM limit is Unlimited, so the counters or the tools are wrong." - F: "Turn the balloon driver off with sched.mem.maxmemctl." - H: "vMotion the VM to a host with more free memory." - N: "A limit compresses and swaps; the balloon must come from somewhere else."

## Notes
- Public source: Broadcom KB 326270, "Impact of virtual machine memory and CPU resource limits" ("The guest operating system is not aware of this limit"; the Updated On field is empty). VMware vSphere 9.1 PDF (build of 2026-11-02): Monitoring and Performance, memory troubleshooting ("the virtual machine (or resource pool) has reached its resource limit"; the virtual machine, its parent pool or ancestor pools may have a limit that is too restrictive); Resource Management, advanced virtual machine attributes (sched.mem.maxmemctl: "If the ESX host needs to reclaim additional memory, it is forced to swap. Swapping is less desirable than ballooning").
- The way a cluster-wide pool limit is split across hosts is not documented in detail, so no option predicts which VM is hit hardest. Whether a pool limit also counts its VMs' overhead is not documented, so the pool's Consumed is set just under the limit.
- Changed in the 2026-11-15 audit: two impossible stem values fixed (pool Consumed 24.3 GB above its 24 GB limit, now 23.9 GB; rpt-app-03 Granted 15.4 GB beside 4.8 GB ballooned, 2.1 GB swapped and 0.4 GB compressed, now about 8 GB, since Granted excludes reclaimed pages); D reworded and its key point updated after Q-E2-214 (balloon first under a limit); N added, the balloon misconception (memory-limit, Misconceptions line 2); A without "only ... must be wrong"; L (swapped pages stay out until touched, redundancy #38) replaced in place by the balloon ceiling; knowledge_main moved to memory-limit, which holds the mechanism and the misconceptions behind A, F, H and N.

## Metadata
```yaml
id: "0291"
title: Ballooning on a host with free memory
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [A, F, H, N]
input: [text]
object: [vm, esxi, resource-pool]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/memory-limit
  - vsphere/object-types/vm/configuration/resource-settings-guidance
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/object-types/resource-pool/resource-pool-design
knowledge_main: vsphere/technology/memory/concepts/memory-limit
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention, consumption-as-contention]
pair: "0140"
status: draft
```
