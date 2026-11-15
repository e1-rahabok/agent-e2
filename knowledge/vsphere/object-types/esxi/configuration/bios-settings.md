# CPU-related BIOS settings

## Status
- Default BIOS settings on servers might not be the best choice for performance.
- Check these settings first when configuring a new server.
- The BIOS options below might not be comprehensive for every server model (Performance Best Practices 9.1, p. 21): check the server vendor's guidance as well.

## General CPU-related settings
- Run the latest BIOS version. After a BIOS update, check the settings again. New options can appear, and old options can change.
- Activate all populated processor sockets.
- Activate all cores in each socket.
- Activate Turbo Boost if the processors support it.
- Activate hyper-threading if the processors support it. See [`vsphere/technology/cpu/concepts/hyper-threading`](../../../technology/cpu/concepts/hyper-threading.md).
- Node interleaving:
  - some NUMA-capable systems offer an option that deactivates NUMA by activating node interleaving,
  - in most cases, the best performance comes from deactivating node interleaving, which leaves NUMA active.
  - See [`vsphere/technology/cpu/concepts/numa`](../../../technology/cpu/concepts/numa.md).
- Activate the hardware-assisted virtualization features: VT-x, AMD-V, EPT, RVI, and similar.
- Some systems require a full power-down before these changes take effect.
- Make sure the snoop mode selection is appropriate for the environment. See [`vsphere/technology/cpu/concepts/numa`](../../../technology/cpu/concepts/numa.md).
- Deactivate devices in the BIOS that will not be used. Examples: serial, USB, or network ports.
- If the BIOS allows the memory scrubbing rate to be set, leave it at the manufacturer default.
- DIMM population (balanced across channels, no asymmetry across sockets) is set in hardware, not in the BIOS: [`vsphere/technology/memory/configuration/memory-hardware`](../../../technology/memory/configuration/memory-hardware.md).

## AES-NI
- Choose processors that support AES-NI. Newer processor versions optimize the AES-NI implementation further.
- Use a BIOS version that supports AES-NI. A BIOS upgrade can be required.
- Activate AES-NI in the BIOS.
- Hosts that support AES-NI expose it to VMs with virtual hardware version 7 or later.
- Enhanced vMotion Compatibility (EVC) or a CPU mask can change this exposure.
- Deactivating AES-NI passthrough can allow vMotion from an AES-NI host to a host without it.
- Features that use AES-NI: VM encryption, encrypted vMotion (without AES-NI it can have unacceptable performance) and vSAN encryption (Performance Best Practices 9.1, pp. 44, 73, 88).

## Intel QAT
- Intel QuickAssist Technology offloads compression, decompression, and cryptographic encryption and decryption from general-purpose cores.
- Significantly reduces the CPU cost of encrypted vMotion.
- To get this benefit, choose processors that support Intel QAT.
- Verify on an ESX host: `lspci | grep -i qat`.

## Processor-specific settings
### Intel processors
- Granite Rapids: enable SNC2 or SNC3, depending on processor variant. Effect: reduces memory latency and improves NUMA domain visibility to ESX.
- Latency-sensitive workloads: enable Latency Optimized Mode. It prevents cores and other components from entering a low-power state. Some processors and BIOS versions enable it by default.
- Prefetchers:
  - keep all L1 and L2 core prefetchers enabled, unless workload analysis suggests otherwise,
  - memory-bound, read-heavy workloads with frequent LLC misses: consider disabling LLC prefetch and enabling XPT prefetch, unless workload-specific tuning suggests otherwise.
- DRAM page policy:
  - Open Adaptive: typically best for energy efficiency, server-side Java, and workloads sensitive to idle memory latency,
  - Closed Page: typically best for I/O-intensive workloads, OLTP, and HPC.
### AMD processors
- AMD EPYC NUMA settings: [`vsphere/technology/cpu/configuration/numa-settings`](../../../technology/cpu/configuration/numa-settings.md), section AMD EPYC.

## C-states for Intel Granite Rapids
- Disable deep C-states (C6) for latency-sensitive workloads.
- Recommendations by workload (Performance Best Practices 9.1, Table 1-1):

| Workload | Core C-states | Package C-states | Rationale |
|---|---|---|---|
| Latency critical (AI, network function virtualization) | C0/C1 only (C6 disabled) | Disabled | Avoid jitter and wake latency |
| Cloud native / microservices | C0/C1 (C6 optional) | PC6 allowed | Better performance per watt |
| Databases | C0/C1 (be cautious about C6) | Limited | Balance latency against idle |
| HPC / batch | Typically irrelevant | Typically irrelevant | With high utilization the CPU rarely enters C-states |
| Idle or spare capacity | C6 or C6-P | PC6 | Maximize power savings |


## Misconceptions
- "BIOS defaults are optimal" → Performance Best Practices 9.1 says defaults might not be the best choice for performance: check the settings of this file on every new server.
- "Turn NUMA off in BIOS for better performance" → node interleaving hides the NUMA layout from ESXi, so its NUMA scheduler cannot keep a VM's memory local; in most cases Performance Best Practices 9.1 recommends deactivating node interleaving, which leaves NUMA active.

## Metadata
```yaml
id: vsphere/object-types/esxi/configuration/bios-settings
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
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/concepts/numa
- vsphere/technology/cpu/concepts/hardware-assisted-virtualization
- vsphere/technology/cpu/configuration/host-power-management
- vsphere/technology/memory/configuration/memory-hardware
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Hardware BIOS Settings > General BIOS Settings; Processor-Specific BIOS Settings (pp. 21-23); Power Management BIOS Settings (pp. 22-23); AES-NI Support (p. 12); Intel QAT Support (p. 13)
corrections: []
review_notes: []
status: draft
```
