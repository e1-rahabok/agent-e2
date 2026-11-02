---
id: vsphere/memory/architecture/memory-hardware
type: concept
scope: vsphere
resources: [memory]
objects: [esxi]
related:
  - vsphere/memory/architecture/memory-tiering
  - vsphere/cpu/architecture/bios-settings
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Memory Hardware Considerations > General Memory Hardware Considerations (p. 14)
corrections: []
review_notes:
  - "Checked against 9.1 (revision 20260624). Page 14 read. Unchanged from previous extraction."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices"
  - "New general memory hardware section in the 9.1 document. Not in the 9.0 document."
status: draft
---

# Memory hardware: general considerations

## Guidance (9.1 p. 14)
- In most environments, balance memory population across all channels.
- Avoid memory asymmetry across sockets.

## Related
- Memory tiering hardware (NVMe devices, write rate, endurance, capacity): see `vsphere/memory/architecture/memory-tiering`.
- BIOS settings that affect memory: see `vsphere/cpu/architecture/bios-settings`.

## Traps
- "Uneven population across channels is acceptable" → the source says balance across all channels in most environments.
