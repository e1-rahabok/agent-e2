---
id: vsphere/cpu/architecture/bios-settings
type: concept
scope: vsphere
resources: [cpu, memory]
objects: [esxi]
related:
  - vsphere/cpu/architecture/hyper-threading
  - vsphere/cpu/architecture/numa
  - vsphere/cpu/architecture/hardware-assisted-virtualization
  - vsphere/cpu/architecture/host-power-management
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: Hardware for Use with VMware vSphere > Hardware BIOS Settings > General BIOS Settings; Processor-Specific BIOS Settings (pp. 21-22); AES-NI Support (p. 13)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Source states the BIOS options it lists might not be comprehensive for every server. Server-specific guidance is outside the source."
status: draft
---

# CPU-related BIOS settings

## Status
- Default BIOS settings on servers might not be the best choice for performance.
- Check these settings first when configuring a new server.

## General CPU-related settings
- Run the latest BIOS version. After a BIOS update, check the settings again. New options can appear, and old options can change.
- Activate all populated processor sockets.
- Activate all cores in each socket.
- Activate Turbo Boost if the processors support it.
- Activate hyper-threading if the processors support it. See `vsphere/cpu/architecture/hyper-threading`.
- Node interleaving:
  - some NUMA-capable systems offer an option that deactivates NUMA by activating node interleaving,
  - in most cases, the best performance comes from deactivating node interleaving, which leaves NUMA active.
  - See `vsphere/cpu/architecture/numa`.
- Activate the hardware-assisted virtualization features: VT-x, AMD-V, EPT, RVI, and similar.
- Some systems require a full power-down before these changes take effect.
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

## Processor-specific settings
- Snoop mode selection. See `vsphere/cpu/architecture/numa`.
- AMD EPYC NUMA settings (NPS and CCX as NUMA Domain). See `vsphere/cpu/architecture/numa`.

## Traps
- "BIOS defaults are optimal" → the source says defaults might not be the best choice for performance.
- "Turn NUMA off in BIOS for better performance" → in most cases the source recommends leaving NUMA active by deactivating node interleaving.
