# Memory tiering

## Definition
- Tech preview in vSphere 8.0 Update 3; supported from vSphere 9.0. Increased performance and redundancy in vSphere 9.1 (p. 38).
- Uses two types of memory devices to increase memory capacity at a reduced cost.
- DRAM: fast and relatively expensive.
- NVMe: secondary, slower and relatively less expensive.
- The counters and `memstats` number the two tiers: DRAM is tier 0, NVMe is tier 1 (`tier1Target`, `tier1Consumed`). This knowledge base writes DRAM and NVMe: Tier-0 and Tier-1 also name NSX gateways.

## Mechanism
- Memory tiering transparently monitors VM memory activity.
- Frequently accessed data stays on DRAM.
- Infrequently accessed data is placed on the NVMe tier.
- Tiering starts when host DRAM consumption reaches about 80%: from then, new memory is allocated from NVMe. Below it, all pages stay in DRAM. The 80% is fixed, not a setting.
- Pages are classified by recency (how recently accessed) and frequency (how often accessed). Hot pages are those accessed most often in about the past minute; the rest are cold.
- The classification module computes guest activeness, tier bandwidth, per-VM tier quotas and per-tier activeness thresholds, then places pages; it keeps adjusting as workloads change phase.
- The whole memory of each VM is scanned in batches; the scan cycle length depends on VM memory size, the scan rate on memory pressure. Pages move at the end of each cycle.
- Only VM pages are tiered. Kernel memory never goes to NVMe.
- CPU cost: about an eighth of a core on smaller hosts.
- Host large pages are disabled by default on a tiered host: tiering works on small pages.

## Touching a page on NVMe
- The CPU cannot read or write NVMe directly. A page on NVMe is fetched back to DRAM when it becomes active; the vCPU that touched it waits for the fetch.
- So a guest write to a cold page waits too: an access to a page on NVMe raises a page fault, and the page is fetched to DRAM before the access completes (vSphere 9.1 documentation, pp. 1848, 1872). The fetch shows as NVMe read bandwidth, which counts pages fetched from NVMe when they become active; NVMe write bandwidth counts cold pages moved down (p. 1848).
- NVMe write bandwidth is demotion: cold pages moved down in the background, off the vCPU's path. It costs device endurance and device time: under heavy writes the device's garbage collection can raise read latency.
- One fetch costs about 1,000x a DRAM access: about 100-200 µs against about 100 ns. Each fetch delays the touching vCPU once, for the full fetch (a wake-up delay of an idle device included). A few fetches cost little, not nothing; many fetches at a healthy latency still slow a VM.
- VM memory contention (esxtop %LAT_M; VCF Operations Memory Contention) does not count time spent on pages in the NVMe tier: the memory latency counter is unaware of memory tiering. A VM can wait on NVMe while its memory contention reads near 0. Read the NVMe tier counters (read bandwidth and latency) directly, or NVMe wait ([`vsphere/object-types/cluster/cluster-performance`](../../../object-types/cluster/cluster-performance.md), section NVMe wait formula).
- Compared with host swapping (including swap to host cache):
  - trigger: swapping is reactive, a last resort under severe memory pressure; tiering is proactive and runs continuously once DRAM consumption passes about 80%;
  - selection: swapping picks pages at random, so active pages go out too and the application stalls; tiering ages pages by recency and frequency and moves only cold ones;
  - placement: hot pages stay in DRAM, cold pages go to NVMe; swap uses a file, often on shared SAN or NAS storage.

## Capacity management
- Effective host memory = DRAM + NVMe. At the default 1:1 ratio, capacity doubles; at most 4 TB of NVMe per host.
- The capacity constraint moves from Consumed to Active memory. Consumed can exceed DRAM by design; Active must stay within DRAM, ideally below 50% of it.
- An NVMe device used for tiering is not available to vSAN. Count the lost vSAN capacity when sizing the cluster.
- Overcommit is counted against DRAM only; tiering is what makes a memory overcommit ratio above 1:1 workable. At the default 1:1 tier ratio, a host can carry up to 2x its DRAM in VM memory. Broadcom's warning not to overcommit on top of tiering is against allocation beyond DRAM + NVMe, where ballooning and swapping run on top of NVMe pages.
- Consumed covers both tiers; once cold pages move to NVMe, consumed can exceed DRAM.
- The capacity plan sizes DRAM; tiering is not part of the overcommit ratio ([`sp5-framework/capacity/overcommit`](../../../../sp5-framework/capacity/overcommit.md)). In the running stage, consumed memory above DRAM is expected on a tiered host.

## Sizing (documentation)
- Default DRAM:NVMe ratio 1:1: doubles host memory. NVMe used = the smaller of the ratio and the tier partition, at most 4 TB.
- Example: 256 GB DRAM with a 4 TB NVMe device at 1:1 → 256 GB of tiered memory.
- Good candidates: hosts where consumed memory is high (above 50% allocated across VMs) while active memory stays below 50% of DRAM.
- Most workloads keep active memory between 10% and 30% of host memory.
- Example: 1 TB DRAM host, 200 GB active, 800 GB consumed. With 1 TB NVMe and twice the VMs: 400 GB active is still within 50% of DRAM.
- A tiered host has higher hypervisor overhead: about 7.96% of total memory for 512 GB DRAM + 512 GB NVMe, against about 2% for a 1 TB non-tiered host. Less memory is reservable.

## VMs kept in DRAM
- Excluded from tiering automatically: 1 GB page VMs, confidential VMs, Fault Tolerance VMs, large VMs, low latency VMs, nested virtualization VMs (VBS can opt in), PCI passthrough VMs (including vGPU), preallocated VMs, vQAT VMs.
- VMs with more than 512 GB of memory and 64 vCPUs can degrade on a tiered host (documentation). The VCF 9.0 performance study sets the line lower: no VMs larger than 32 vCPUs and 512 GB with tiering. The documentation advises disabling tiering for them, with a full memory reservation.
- A VM with tiering disabled needs a full memory reservation. Without it, it competes for DRAM with tiered VMs and its pages go to the host swap file, slower than NVMe.
- To turn tiering off for one VM, set the advanced parameter `sched.mem.enableTiering = "FALSE"` with the VM powered off, then power it on (Broadcom KB 426485, KB 448305). The change needs a power cycle, so it waits for a maintenance window; turning tiering back on needs one too.
- Each DRAM-only reservation shrinks the DRAM left for tiered VMs. Example: 1 TB DRAM, 1 TB NVMe; two 200 GB VMs fully reserved and excluded → the remaining VMs run at about 0.6:1 (600 GB DRAM : 1 TB NVMe).

## Interactions
- Reclamation still exists on a tiered host. Balloon, compression and swap can run while NVMe has free space:
  - a VM excluded from tiering without a full memory reservation competes for DRAM, and its pages can go to the host swap file, which is slower than NVMe;
  - a memory limit on a VM or resource pool reclaims whatever the host has free;
  - demand beyond DRAM + NVMe: swap stays as the last resort, for correctness, for example during evacuations at 3x-4x overcommit.
- Broadcom does not state that compression and swap now wait until NVMe is full. The host's total memory is DRAM + NVMe, and new pages are allocated from NVMe once DRAM passes 80%, so host-wide reclamation is expected only when both tiers are nearly full.
- Do not allocate beyond DRAM + NVMe: ballooning and swapping on top of NVMe pages degrade performance. An overcommit ratio above 1:1 against DRAM, within DRAM + NVMe, is the purpose of tiering.
- Memory reservations (not pinned memory) are served from both tiers. The vendor example, reserved VMs that together exceed DRAM, shows the split; it is not a condition for it.
- A memory reservation is a floor against reclamation (balloon, compression, swap), not a DRAM placement lock. Once DRAM consumption passes about 80%, cold pages of a reserved tiered VM go to NVMe, whatever the total of the reservations. Only its overhead memory always sits in DRAM. To keep a VM in DRAM, turn tiering off for it and reserve all its memory (vSphere 9.1 documentation, pp. 1871, 1873, 1969).
- vMotion of a tiered VM takes 1.5x to 2x longer: pages are fetched from NVMe first. The running VM is barely affected.
- After vMotion the destination host starts tiering the VM from scratch: page heat is not transferred (planned for a future release).
- Measured (VCF 9.0 performance study): evacuating 4 Oracle VMs took 82 s with tiering against 23.5 s DRAM only; downtime stayed below 1 s and the guest penalty below 5%. The extra time is in the precopy, reading cold pages from NVMe.

## HA admission control
- DRAM is required to power on a VM: its overhead memory always sits in DRAM, and NVMe cannot replace DRAM at restart.
- vSphere 9.1 and earlier: admission control counted DRAM and NVMe as one pool. It could show green while the surviving hosts lacked the DRAM to restart the VMs: a silent failure found only at a real host failure.
- vSphere 9.1.1 and later: admission control tracks DRAM as its own resource, with Current DRAM Failover Capacity beside CPU and memory. Supported with the cluster resource percentage and dedicated failover hosts policies; not with the slot policy. Do not use the slot policy on a tiered cluster.
- On a tiered destination host, DRS also weighs active memory in its placement decision.
- On arrival all of the VM's pages are in DRAM; they move back to NVMe over time. DRS migrations take longer for the same reason.

## Hardware selection
- Select a high-performance NVMe device with:
  - at least 100,000 writes per second,
  - endurance of at least 3 full Drive Writes per Day (DWPD),
  - sufficient capacity.

## Setup (9.1 p. 38)
- Setup no longer requires manual ESX CLI commands or scripts.
- Setup uses vSphere Configuration Profiles, at cluster level.
- Software mirroring: a new feature in 9.1, also configured at cluster level.
- Hosts go into maintenance mode for the changes to take effect. A reboot is not necessary.

## In the cluster models
- Cluster Consumption: DRAM consumed on tiered hosts (green to 80%), and NVMe consumption as saturation, 15/30/45/60% of the usable DRAM of tiered hosts ([`vsphere/object-types/cluster/models/cluster-consumption`](../../../object-types/cluster/models/cluster-consumption.md)).
- Cluster Performance and VM Performance (%): memory wait = memory latency + NVMe wait, per VM ([`vsphere/object-types/cluster/cluster-performance`](../../../object-types/cluster/cluster-performance.md)).
- Cluster Risk: active memory 50/62.5/75/100% of DRAM; NVMe read latency 100/200/400/800 µs ([`vsphere/object-types/cluster/models/cluster-risk`](../../../object-types/cluster/models/cluster-risk.md)).

## Performance thresholds (documentation)
- Active memory, as % of host DRAM:
  - 50% or lower: green, recommended;
  - 50-75%: test and monitor the workloads; some run fine;
  - above 75%: significant performance loss expected in most cases.
- NVMe device read latency:
  - below 200 µs: performance stays good;
  - 200-400 µs: potential for issues;
  - above 400 µs: workload impact expected.
- NVMe read bandwidth above 200 MB/s on a host: start watching the device latency. A trigger to look, not a limit.
- In a cluster that mixes tiered and non-tiered hosts: host CPU above 75% on a non-tiered host can reduce the efficiency of tiering (VCF 9.0 performance study, p. 39).
- Measured cost at the default 1:1 ratio and 2x VM density (VCF 9.0): VDI 0-8% loss, VMmark 5%, Oracle below 5%, SQL Server and MySQL 5-10%.

## Monitoring counters (vSphere Client, host and VM)
| Counter | Object | Unit, rollup, level | Meaning |
|---|---|---|---|
| tier.consumed (Tier memory consumed) | Host | MB, Latest, level 2 | ESXi pages consumed per tier. |
| Tier in rate | Host | MBps | Rate at which pages are brought back from the NVMe tier to DRAM. |
| Tier out rate | Host | MBps | Rate at which pages are moved to the NVMe tier. |
| bandwidth.total (Estimated DRAM / NVMe Bandwidth) | Host | MBps, Latest, level 1 | Total read and write bandwidth per memory type. |
| bandwidth.read, bandwidth.write | Host, VM | MBps, Latest, level 2 | Read and write bandwidth per tier (DRAM, NVMe). |
| latency.read, latency.write | Host | ns, Latest, level 3 | DRAM and NVMe read and write latency. |

- Active memory: vCenter Active (KB); esxtop TCHD per VM, summed for the host (esxtop has no host-wide TCHD); VCF Operations Guest Active.
- Tier in rate (NVMe read bandwidth) is the performance signal: a VM touches a page that sits on NVMe and waits for it. Tier out rate (NVMe write bandwidth) is cold pages moving down.
- Documentation observation: read latency below 200 µs at about 400 MB/s on a strong device; about 300 µs at similar bandwidth on other devices.
- To investigate one slow VM, check that VM's NVMe read bandwidth.
- NVMe device wear: `esxcli nvme device log smart get -A <adapter>` shows remaining life and wear rate.
- NVMe read latency against the thresholds above uses latency.read of the NVMe tier, in nanoseconds: 200 µs = 200,000 ns.
- The NVMe charts appear only on hosts with memory tiering configured.
- latency.read and latency.write are level 3: not stored at the default statistics level. See [`vsphere/tools/vsphere-client/vcenter-statistics`](../../../tools/vsphere-client/vcenter-statistics.md).
- The vSphere Client lists each tier device with its details on the host's Memory Tiering pane.
- Chart path: Monitor > Performance > Advanced, Memory view: Memory type read bandwidth, read latency, write bandwidth, write latency.
- Per VM, NVMe use from the ESXi shell (MB):

```text
memstats -r vmtier-stats -u mb -s name:memSize:active:tier1Target:tier1Consumed
```

- tier1Target: NVMe memory the VM is meant to hold; tier1Consumed: NVMe memory it holds now.
- NVMe consumed at 0 is expected while host DRAM consumption is below about 80%: tiering has not started.

## Operations
- Leave CPU headroom for the CPU cost of tiering (9.1 p. 38; the cost: section Mechanism).
- Use memory tiering actively, as part of memory, not as an occasional buffer.
- Leave 25% of the NVMe drive unpartitioned (for example 1.2 TB of a 1.6 TB drive). The flash translation layer then has spare blocks for lazy garbage collection, avoiding urgent inline garbage collection under write pressure.
- Track the read latency of the tier device.
- SSD pages (4-16 KB) are the read/write unit; blocks (4-32 MB) are the erase unit. This asymmetry makes NAND fragmentation the main NVMe performance risk.
- An idle tier device shows latency spikes on sporadic reads: power-state wake-up. See [`vsphere/technology/storage/metrics/host/disk`](../../storage/metrics/host/disk.md).

## Misconceptions
- "Tiered memory performs like DRAM" → infrequently accessed data sits on the NVMe tier.
- "Any SSD works for memory tiering" → Performance Best Practices for vSphere 9.1 (p. 14) specifies a high-performance NVMe device with the write rate and endurance above.
- "Active memory at 75% of DRAM is the limit" → 75% is the point where some workloads begin to suffer. The ideal is 50%.
- "High consumed memory on a tiered host is a problem" → consumed may exceed DRAM by design; active memory against DRAM decides performance.
- "A memory reservation keeps a tiered VM in DRAM" → it keeps the VM from being ballooned or swapped; its cold pages still go to NVMe, also when the reservations fit in DRAM. Turn tiering off for the VM and reserve all its memory.
- "Lower the reservation of a VM with tiering off to free DRAM for the other VMs" → a VM with tiering off and no full reservation competes for DRAM and its pages go to the host swap file. To give DRAM back, turn tiering back on for that VM (a power cycle) and keep its reservation.
- "Disable tiering for a VM and it gets DRAM" → only with a full memory reservation; otherwise it can be swapped.
- "NVMe shows 0 consumed, so tiering is broken" → by design below about 80% DRAM consumption; also 0 for Fault Tolerance and PCI passthrough VMs, which stay in DRAM.
- "Tiering doubles memory, so the host is still at 1:1" → the overcommit ratio is against DRAM: a 1 TB DRAM host carrying 1.66 TB of VM memory runs at 1.66:1. Tiering makes that ratio workable; it does not reset it.
- "Tiering doubles memory, so plan capacity on Consumed" → plan on Active against DRAM; Consumed may exceed DRAM.
- "The NVMe device can also serve vSAN" → a tiering device is taken out of vSAN capacity.
- "NVMe tiering behaves like swap" → tiering selects cold pages by age on a dedicated device; swap picks random pages.
- "Writes do not hurt: only reads come from NVMe" → a guest write to a cold page waits for the page to come back from NVMe; only demotion writes are off the vCPU's path.
- "Swap and compression wait until the NVMe tier is full" → not stated by Broadcom; non-tiered VMs without a full reservation and memory limits are reclaimed while tier 1 has room.
- "VM memory contention is near 0, so the VM does not wait for memory" → on a tiered host it does not count NVMe fetches; read the VM's NVMe read bandwidth or NVMe wait.
- "NVMe consumed means the VMs are slow" → it holds cold pages: it is saturation, memory spilled beyond DRAM, not contention. On a tiered host it replaces compression and swap as the saturation signal; the performance signals are active memory against DRAM and NVMe reads.
- "HA admission control is green, so the VMs will restart" → before 9.1.1 it counted NVMe as if it were DRAM; restarts need DRAM.
- "NVMe read latency of 900 µs on an idle device can be ignored: it is only a wake-up" → the VM that touched the page waited 900 µs. The wake-up is the why. What the VMs lost is reads × latency: few reads, little total wait, but never zero.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/memory-tiering
up_front: 'Lower the reservation of a VM with tiering off to free DRAM for the other VMs'
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
- storage
pillar:
- performance
- capacity
- value
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
- vsphere/technology/memory/concepts/host-memory-states
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/technology/memory/configuration/host-level-swapping
- vsphere/technology/storage/metrics/host/disk
source:
  document: Knowledge base; Performance Best Practices for VMware vSphere 9.1 (revision 20260624); VMware vSphere 9.1 documentation (PDF built 2026-11-02); Memory Tiering Performance, VMware Cloud Foundation 9.0 (performance study, July 2025); Broadcom KB 426485 and KB 448305 (per-VM memory tiering setting)
  path: 'Memory Hardware Considerations > Memory Tiering Hardware (p. 14); ESX Memory Considerations > Memory Tiering (p. 38); vSphere Resource Management > Memory Tiering over NVMe: Capacity Planning Considerations, Virtual Machine Profiles, Configuration Parameters, Assessing Customer Workloads, Considerations and Best Practices, NVMe Failure Scenarios, Troubleshooting, NVMe Device Health Monitoring (pp. 1844-1849, 1868-1873, 1957-1959); vSphere Availability > Memory Tiering and HA Admission Control (pp. 1969-1971); Monitoring and Performance > Hosts > Memory (MB), Memory Rate, Memory Bandwidth, Memory Latency; View Memory Tiering Device Information (pp. 2038, 2070, 2074-2076, 2145); performance study > Using and monitoring Memory Tiering (pp. 34-39, https://www.vmware.com/docs/memtier-vcf9-perf); Storage > ESXi > Disk or Device > Memory Tiering'
corrections: []
review_notes:
- 'To check: Section ''Mechanism'': that the 80% tiering point is fixed and not a setting; vSphere 9.1 documentation (p. 1869) gives around 80% and names no setting; the fixed value comes from a blog (yellow-bricks.com, Memory Tiering Considerations and frequently asked questions, 2026-07-16).'
- 'To check: Section ''Interactions'': whether the host memory states and host-wide reclamation count NVMe as free memory; vSphere 9.1 documentation, Resource Management > Memory Reclamation (p. 1839), does not say.'
- 'To check: Section ''Monitoring counters'': that Tier in rate (p. 2071) and NVMe read bandwidth (p. 1848) count the same fetches; compare both on a tiered 9.1 host.'
status: draft
```
