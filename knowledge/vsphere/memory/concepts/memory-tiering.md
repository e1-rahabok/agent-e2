# Memory tiering

## Definition
- Introduced in vSphere 9.0. Increased performance and redundancy in vSphere 9.1 (p. 38).
- Uses two types of memory devices to increase memory capacity at a reduced cost.
- Tier 1: DRAM, fast and relatively expensive.
- Tier 2: NVMe storage, secondary, slower and relatively less expensive.

## Mechanism
- Memory tiering transparently monitors VM memory activity.
- Frequently accessed data stays on DRAM.
- Infrequently accessed data is placed on the NVMe tier.

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

- Tier in rate is the performance signal: a VM touches a page that sits on NVMe and waits for it. Tier out rate is housekeeping of cold pages.
- NVMe read latency against the thresholds above uses latency.read of the NVMe tier, in nanoseconds: 200 µs = 200,000 ns.
- The NVMe charts appear only on hosts with memory tiering configured.
- latency.read and latency.write are level 3: not stored at the default statistics level. See `vsphere/foundations/vcenter-statistics`.
- The vSphere Client lists each tier device with its details on the host's Memory Tiering pane.

## Operations (book)
- Use memory tiering actively, as part of memory, not as an occasional buffer.
- Leave 25% of the NVMe drive unpartitioned (for example 1.2 TB of a 1.6 TB drive). The flash translation layer then has spare blocks for lazy garbage collection, avoiding urgent inline garbage collection under write pressure.
- Track the read latency of the tier device.
- SSD pages (4-16 KB) are the read/write unit; blocks (4-32 MB) are the erase unit. This asymmetry makes NAND fragmentation the main NVMe performance risk.
- An idle tier device shows latency spikes on sporadic reads: power-state wake-up. See `vsphere/storage/metrics/host/disk`.

## Traps
- "Tiered memory performs like DRAM" → infrequently accessed data sits on the NVMe tier.
- "Any SSD works for memory tiering" → the source specifies a high-performance NVMe device with the write rate and endurance above.
- "Active memory at 75% of DRAM is the limit" → 75% is the point where some workloads begin to suffer. The ideal is 50%.

## Metadata
```yaml
id: vsphere/memory/concepts/memory-tiering
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
- vsphere/memory/concepts/overcommit-techniques
- vsphere/foundations/vcenter-statistics
- vsphere/memory/configuration/host-level-swapping
- vsphere/storage/metrics/host/disk
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Memory Hardware Considerations > Memory Tiering Hardware (p. 14); ESX Memory Considerations > Memory Tiering (p. 38); Storage > ESXi > Disk or Device > Memory Tiering
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 14 and 38 read. Setup changes and CPU headroom bullet added (p. 38).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'Introduced in vSphere 9.0. The 9.1 document (p. 38) refers to ''More Memory, Less Effort: Configuring Memory Tiering in VCF 9.1'' and the ''Memory Tiering Resource Hub''. Not read.'
- 'Section ''Operations (book)'': from Storage > ESXi. The 25% figure is the author''s practice.'
- 'Section ''Monitoring counters'': from the vSphere 9.1 documentation (PDF built 2026-11-02), vSphere Monitoring and Performance > Hosts > Memory (MB), Memory Rate (MBps), Memory Bandwidth (MBps), Memory Latency (ns); View Memory Tiering Device Information (pp. 2038, 2070, 2074-2076, 2145). The reading of tier in rate as the performance signal is Claude''s inference.'
status: draft
```
