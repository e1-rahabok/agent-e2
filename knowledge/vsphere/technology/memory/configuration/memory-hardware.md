# Memory hardware

## Guidance (9.1 p. 14)
- In most environments, balance memory population across all channels.
- Avoid memory asymmetry across sockets.

## Related
- Memory tiering hardware (NVMe devices, write rate, endurance, capacity): see [`vsphere/technology/memory/concepts/memory-tiering`](../concepts/memory-tiering.md).
- BIOS settings that affect memory: see [`vsphere/object-types/esxi/configuration/bios-settings`](../../../object-types/esxi/configuration/bios-settings.md).
- Memory channels per NUMA node and the channel interleave setting (NPS on AMD EPYC), which set the memory bandwidth a VM gets: see [`vsphere/technology/cpu/configuration/numa-settings`](../../cpu/configuration/numa-settings.md).

## Misconceptions
- "Uneven population across channels is acceptable" → Performance Best Practices for vSphere 9.1 (p. 14) says balance across all channels in most environments.

## Metadata
```yaml
id: vsphere/technology/memory/configuration/memory-hardware
retriever_guide: what-to-set
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
object:
- HostSystem
internal_derive: []
related:
- vsphere/technology/memory/concepts/memory-tiering
- vsphere/object-types/esxi/configuration/bios-settings
- vsphere/technology/cpu/configuration/numa-settings
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Memory Hardware Considerations > General Memory Hardware Considerations (p. 14)
corrections: []
review_notes: []
status: draft
```
