# Memory tiering

## Definition
- Tech preview in vSphere 8.0 Update 3; supported from vSphere 9.0. Increased performance and redundancy in vSphere 9.1 (p. 38).
- Uses two types of memory devices to increase memory capacity at a reduced cost.
- Tier 0: DRAM, fast and relatively expensive.
- Tier 1: NVMe storage, secondary, slower and relatively less expensive.
- Tier numbers as the counters and `memstats` use them: DRAM = tier 0, NVMe = tier 1.

## Mechanism
- Memory tiering transparently monitors VM memory activity.
- Frequently accessed data stays on DRAM.
- Infrequently accessed data is placed on the NVMe tier.
- Tiering starts when host memory consumption reaches about 80% of DRAM capacity. Below that, all pages stay in DRAM.
- Pages are classified by recency (how recently accessed) and frequency (how often accessed).
- The whole memory of each VM is scanned in batches; the scan cycle length depends on VM memory size, the scan rate on memory pressure. Pages move at the end of each cycle.
- Only VM pages are tiered. Kernel memory never goes to NVMe.
- CPU cost: about an eighth of a core on smaller hosts.
- Compared with host swapping (including swap to host cache):
  - trigger: swapping is reactive, a last resort under severe memory pressure; tiering is proactive and runs continuously once DRAM consumption passes about 80%;
  - selection: swapping picks pages at random, so active pages go out too and the application stalls; tiering ages pages by recency and frequency and moves only cold ones;
  - placement: hot pages stay in DRAM (tier 0), cold pages go to NVMe (tier 1); swap uses a file, often on shared SAN or NAS storage.

## Capacity management
- Effective host memory = DRAM (tier 0) + NVMe (tier 1). At the default 1:1 ratio, capacity doubles; at most 4 TB of NVMe per host.
- The capacity constraint moves from Consumed to Active memory. Consumed can exceed DRAM by design; Active must stay within DRAM, ideally below 50% of it.
- An NVMe device used for tiering is not available to vSAN. Count the lost vSAN capacity when sizing the cluster.
- Do not overcommit memory on top of tiering (see Interactions). The overcommit ratio counts DRAM only: the NVMe tier exists to avoid overcommit.
- Consumed covers both tiers; once cold pages move to tier 1, consumed can exceed DRAM.
- Unknown: whether VM memory contention (esxtop %LAT_M) counts time spent on pages in the NVMe tier. NVMe is about 1,000x slower than DRAM, so read the NVMe tier counters (read bandwidth and latency) directly. Linux KVM has no such per-VM signal either.

## Sizing (documentation)
- Default DRAM:NVMe ratio 1:1: doubles host memory. NVMe used = the smaller of the ratio and the tier partition, at most 4 TB.
- Example: 256 GB DRAM with a 4 TB NVMe device at 1:1 → 256 GB of tiered memory.
- Good candidates: hosts where consumed memory is high (above 50% allocated across VMs) while active memory stays below 50% of DRAM.
- Most workloads keep active memory between 10% and 30% of host memory.
- Example: 1 TB DRAM host, 200 GB active, 800 GB consumed. With 1 TB NVMe and twice the VMs: 400 GB active is still within 50% of DRAM.
- A tiered host has higher hypervisor overhead: about 7.96% of total memory for 512 GB DRAM + 512 GB NVMe, against about 2% for a 1 TB non-tiered host. Less memory is reservable.

## VMs kept in DRAM
- Excluded from tiering automatically: 1 GB page VMs, confidential VMs, Fault Tolerance VMs, large VMs, low latency VMs, nested virtualization VMs (VBS can opt in), PCI passthrough VMs (including vGPU), preallocated VMs, vQAT VMs.
- VMs with more than 512 GB of memory and 64 vCPUs can degrade on a tiered host. The documentation advises disabling tiering for them, with a full memory reservation.
- A VM with tiering disabled needs a full memory reservation. Without it, it competes for DRAM with tiered VMs and its pages go to the host swap file, slower than NVMe.
- Each DRAM-only reservation shrinks the DRAM left for tiered VMs. Example: 1 TB DRAM, 1 TB NVMe; two 200 GB VMs fully reserved and excluded → the remaining VMs run at about 0.6:1 (600 GB DRAM : 1 TB NVMe).

## Interactions
- Do not combine memory overcommit with memory tiering: ballooning and swapping on top of NVMe pages degrade performance.
- Memory reservations (not pinned memory) can be split between DRAM and NVMe when the reserved VMs together exceed DRAM.
- vMotion of a tiered VM takes 1.5x to 2x longer: pages are fetched from NVMe first. The running VM is barely affected.
- After vMotion the destination host starts tiering the VM from scratch: page heat is not transferred.
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

## Performance thresholds (from the source)
- Active memory:
  - ideal: no more than 50% of the host DRAM capacity,
  - some workloads do not begin to suffer until active memory approaches 75%.
- NVMe read latency:
  - ideal: below 200 microseconds,
  - some workloads do not begin to suffer until latency approaches 400 microseconds.

- Make sure there is enough CPU headroom to handle the CPU cost of memory tiering (9.1 p. 38).

## Monitoring counters (vSphere Client, host and VM)
| Counter | Object | Unit, rollup, level | Meaning |
|---|---|---|---|
| tier.consumed (Tier memory consumed) | Host | MB, Latest, level 2 | ESXi pages consumed per tier. |
| Tier in rate | Host | MBps | Rate at which pages are brought back from the NVMe tier to DRAM. |
| Tier out rate | Host | MBps | Rate at which pages are moved to the NVMe tier. |
| bandwidth.total (Estimated DRAM / NVMe Bandwidth) | Host | MBps, Latest, level 1 | Total read and write bandwidth per memory type. |
| bandwidth.read, bandwidth.write | Host, VM | MBps, Latest, level 2 | Read and write bandwidth per tier (DRAM = tier 0, NVMe = tier 1). |
| latency.read, latency.write | Host | ns, Latest, level 3 | DRAM and NVMe read and write latency. |

- Tier in rate (NVMe read bandwidth) is the performance signal: a VM touches a page that sits on NVMe and waits for it. Tier out rate (NVMe write bandwidth) is cold pages moving down.
- NVMe read bandwidth above 200 MB/s: start watching NVMe device latency (documentation threshold).
- Documentation observation: read latency below 200 µs at about 400 MB/s on a strong device; about 300 µs at similar bandwidth on other devices.
- To investigate one slow VM, check that VM's NVMe read bandwidth.
- NVMe device wear: `esxcli nvme device log smart get -A <adapter>` shows remaining life and wear rate.
- NVMe read latency against the thresholds above uses latency.read of the NVMe tier, in nanoseconds: 200 µs = 200,000 ns.
- The NVMe charts appear only on hosts with memory tiering configured.
- latency.read and latency.write are level 3: not stored at the default statistics level. See `vsphere/tools/vsphere-client/vcenter-statistics`.
- The vSphere Client lists each tier device with its details on the host's Memory Tiering pane.
- Chart path: Monitor > Performance > Advanced, Memory view: Memory type read bandwidth, read latency, write bandwidth, write latency.
- Per VM, tier 1 use from the ESXi shell (MB):

```text
memstats -r vmtier-stats -u mb -s name:memSize:active:tier1Target:tier1Consumed
```

- tier1Target: NVMe memory the VM is meant to hold; tier1Consumed: NVMe memory it holds now.
- Tier 1 consumed at 0 is expected while host DRAM consumption is below about 80%: tiering has not started.

## Operations (book)
- Use memory tiering actively, as part of memory, not as an occasional buffer.
- Leave 25% of the NVMe drive unpartitioned (for example 1.2 TB of a 1.6 TB drive). The flash translation layer then has spare blocks for lazy garbage collection, avoiding urgent inline garbage collection under write pressure.
- Track the read latency of the tier device.
- SSD pages (4-16 KB) are the read/write unit; blocks (4-32 MB) are the erase unit. This asymmetry makes NAND fragmentation the main NVMe performance risk.
- An idle tier device shows latency spikes on sporadic reads: power-state wake-up. See `vsphere/technology/storage/metrics/host/disk`.

## Traps
- "Tiered memory performs like DRAM" → infrequently accessed data sits on the NVMe tier.
- "Any SSD works for memory tiering" → the source specifies a high-performance NVMe device with the write rate and endurance above.
- "Active memory at 75% of DRAM is the limit" → 75% is the point where some workloads begin to suffer. The ideal is 50%.
- "High consumed memory on a tiered host is a problem" → consumed may exceed DRAM by design; active memory against DRAM decides performance.
- "Disable tiering for a VM and it gets DRAM" → only with a full memory reservation; otherwise it can be swapped.
- "Tier 1 shows 0 consumed, so tiering is broken" → by design below about 80% DRAM consumption; also 0 for Fault Tolerance and PCI passthrough VMs, which stay in DRAM.
- "Tiering doubles memory, so plan capacity on Consumed" → plan on Active against DRAM; Consumed may exceed DRAM.
- "The NVMe device can also serve vSAN" → a tiering device is taken out of vSAN capacity.
- "NVMe tiering behaves like swap" → tiering selects cold pages by age on a dedicated device; swap picks random pages.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/memory-tiering
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
- storage
pillar:
- capacity
- value
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/memory/concepts/host-memory-states
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/technology/memory/configuration/host-level-swapping
- vsphere/technology/storage/metrics/host/disk
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Memory Hardware Considerations > Memory Tiering Hardware (p. 14); ESX Memory Considerations > Memory Tiering (p. 38); Storage > ESXi > Disk or Device > Memory Tiering
corrections:
- 'Section ''Capacity management'': overcommit against DRAM only; consumed covers both tiers; whether %LAT_M includes NVMe page faults is unknown to the author (Q082, 2026-11-07).'
- 'Sections ''Definition'' (tier numbering), ''Mechanism'' (swap comparison), ''Capacity management'', ''Interactions'' (DRAM on arrival, DRS), ''Monitoring counters'' (chart path, memstats, zero tier 1): author (2026-11-07). Tier numbering corrected: DRAM = tier 0, NVMe = tier 1, as in the counters.'
review_notes:
- Checked against 9.1 (revision 20260624). Pages 14 and 38 read. Setup changes and CPU headroom bullet added (p. 38).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'Introduced in vSphere 9.0. The 9.1 document (p. 38) refers to ''More Memory, Less Effort: Configuring Memory Tiering in VCF 9.1'' and the ''Memory Tiering Resource Hub''. Not read.'
- 'Section ''Operations (book)'': from Storage > ESXi. The 25% figure is the author''s practice.'
- 'Sections ''Mechanism'' (from the 80% line on), ''Sizing (documentation)'', ''VMs kept in DRAM'', ''Interactions'' and the bandwidth, latency and SMART lines in ''Monitoring counters'': from the vSphere 9.1 documentation, vSphere Resource Management > Memory Tiering over NVMe, Capacity Planning Considerations, Virtual Machine Profiles, Configuration Parameters, Assessing Customer Workloads, Memory Tiering Considerations and Best Practices, NVMe Failure Scenarios, Troubleshooting > The Reservable Memory is Lower than Expected, NVMe Device Health Monitoring (pp. 1844-1849, 1868-1873, 1957-1959).'
- 'Section ''Interactions'': the reason given for not combining overcommit with tiering is Claude''s paraphrase of the documentation (potential performance impact).'
- 'Section ''Monitoring counters'': from the vSphere 9.1 documentation (PDF built 2026-11-02), vSphere Monitoring and Performance > Hosts > Memory (MB), Memory Rate (MBps), Memory Bandwidth (MBps), Memory Latency (ns); View Memory Tiering Device Information (pp. 2038, 2070, 2074-2076, 2145). The reading of tier in rate as the performance signal is Claude''s inference.'
status: draft
```
