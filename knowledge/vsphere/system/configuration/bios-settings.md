# CPU-related BIOS settings

## Status
- Default BIOS settings on servers might not be the best choice for performance.
- Check these settings first when configuring a new server.

## General CPU-related settings
- Run the latest BIOS version. After a BIOS update, check the settings again. New options can appear, and old options can change.
- Activate all populated processor sockets.
- Activate all cores in each socket.
- Activate Turbo Boost if the processors support it.
- Activate hyper-threading if the processors support it. See `vsphere/cpu/concepts/hyper-threading`.
- Node interleaving:
  - some NUMA-capable systems offer an option that deactivates NUMA by activating node interleaving,
  - in most cases, the best performance comes from deactivating node interleaving, which leaves NUMA active.
  - See `vsphere/cpu/concepts/numa`.
- Activate the hardware-assisted virtualization features: VT-x, AMD-V, EPT, RVI, and similar.
- Some systems require a full power-down before these changes take effect.
- Make sure the snoop mode selection is appropriate for the environment. See `vsphere/cpu/concepts/numa`.
- Deactivate devices in the BIOS that will not be used. Examples: serial, USB, or network ports.
- If the BIOS allows the memory scrubbing rate to be set, leave it at the manufacturer default.

## AES-NI
- Choose processors that support AES-NI. Newer processor versions optimize the AES-NI implementation further.
- Use a BIOS version that supports AES-NI. A BIOS upgrade can be required.
- Activate AES-NI in the BIOS.
- Hosts that support AES-NI expose it to VMs with virtual hardware version 7 or later.
- Enhanced vMotion Compatibility (EVC) or a CPU mask can change this exposure.
- Deactivating AES-NI passthrough can allow vMotion from an AES-NI host to a host without it.
- Features that use AES-NI are listed in the source (pp. 42, 73, 88). Not read.

## Intel QAT (9.1 p. 13)
- Intel QuickAssist Technology offloads compression, decompression, and cryptographic encryption and decryption from general-purpose cores.
- Significantly reduces the CPU cost of encrypted vMotion.
- To get this benefit, choose processors that support Intel QAT.
- Verify on an ESX host: `lspci | grep -i qat`.

## Processor-specific settings
### Intel processors (9.1 pp. 21-22)
- Granite Rapids: enable SNC2 or SNC3, depending on processor variant. Effect: reduces memory latency and improves NUMA domain visibility to ESX.
- Latency-sensitive workloads: enable Latency Optimized Mode. It prevents cores and other components from entering a low-power state. Some processors and BIOS versions enable it by default.
- Prefetchers:
  - keep all L1 and L2 core prefetchers enabled, unless workload analysis suggests otherwise,
  - memory-bound, read-heavy workloads with frequent LLC misses: consider disabling LLC prefetch and enabling XPT prefetch, unless workload-specific tuning suggests otherwise.
- DRAM page policy:
  - Open Adaptive: typically best for energy efficiency, server-side Java, and workloads sensitive to idle memory latency,
  - Closed Page: typically best for I/O-intensive workloads, OLTP, and HPC.
### AMD processors
- AMD EPYC NUMA settings: see `vsphere/cpu/concepts/numa`.

## C-states for Intel Granite Rapids (9.1 pp. 22-23)
- Disable deep C-states (C6) for latency-sensitive workloads.
- Recommendations by workload (source Table 1-1):

| Workload | Core C-states | Package C-states | Rationale |
|---|---|---|---|
| Latency critical (AI, network function virtualization) | C0/C1 only (C6 disabled) | Disabled | Avoid jitter and wake latency |
| Cloud native / microservices | C0/C1 (C6 optional) | PC6 allowed | Better performance per watt |
| Databases | C0/C1 (be cautious about C6) | Limited | Balance latency against idle |
| HPC / batch | Typically irrelevant | Typically irrelevant | With high utilization the CPU rarely enters C-states |
| Idle or spare capacity | C6 or C6-P | PC6 | Maximize power savings |


## Traps
- "BIOS defaults are optimal" → the source says defaults might not be the best choice for performance.
- "Turn NUMA off in BIOS for better performance" → in most cases the source recommends leaving NUMA active by deactivating node interleaving.

## Metadata
```yaml
id: vsphere/system/configuration/bios-settings
retriever_guide: what-to-set
scope: vsphere
technology:
- system
- cpu
- memory
pillar:
- performance
- security
product:
- vsphere
object:
- HostSystem
internal_derive: []
related:
- vsphere/cpu/concepts/hyper-threading
- vsphere/cpu/concepts/numa
- vsphere/cpu/concepts/hardware-assisted-virtualization
- vsphere/cpu/configuration/host-power-management
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Hardware BIOS Settings > General BIOS Settings; Processor-Specific BIOS Settings (pp. 21-23); Power Management BIOS Settings (pp. 22-23); AES-NI Support (p. 12); Intel QAT Support (p. 13)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 21-23 and 12-13 read. Intel Granite Rapids settings, C-state table and QAT added.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Source states the BIOS options it lists might not be comprehensive for every server. Server-specific guidance is outside the source.
status: draft
```
