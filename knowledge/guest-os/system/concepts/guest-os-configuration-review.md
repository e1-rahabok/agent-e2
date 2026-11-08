# Guest OS configuration review

## Why separate from the VM
- The Guest OS and the VM have their own requirements, and in large organizations two teams own them. The VM review (virtual motherboard and VMware Tools): `vsphere/object-types/vm/configuration/vm-configuration-review`.

## Checks
- **Type**
  - The Guest OS type set at VM creation can differ from what runs now, after an upgrade or a reinstall.
  - Compare the Guest OS property from vCenter (configured) with the one reported by VMware Tools (running). Update vCenter when they differ.
- **Version**
  - Outdated Windows or Linux versions.
  - Too many Linux distributions; within one version, too many builds and patch levels.
  - Too many Windows versions, and too many editions within each.
- **Drivers**
  - PVSCSI used where it fits.
  - VMXNET3, PVRDMA or SR-IOV used where each fits.
- **Agents**
  - Backup, security and monitoring agents add up. Know their total footprint: it is overhead on every VM.
  - Monitoring and log agents (Telegraf, the log agent) only on the VMs meant to have them, current, and collecting.
- **Windows drive letters**
  - Each letter keeps one purpose: C: for the OS only.
  - Temp drive and data drives used the same way on every server. The number of data drives varies, so assign them from Z: backwards.
- **Applications**
  - Know what runs inside. A VM or host name saying webserver does not prove a web server runs.
  - Discover key processes and their connections (Telegraf, service discovery). Shared, overcommitted resources are easier to run when the workload is known; monitoring and troubleshooting need it; some ISVs require it for licensing.
  - A JVM heap or database memory allocation too large for the Guest OS: unless another application runs, memory beyond what the application can address is wasted.
- **Settings**
  - Too many setting options in the corporate standard.
  - Screen saver off: irrelevant on a server OS.

## Traps
- "The Guest OS type in vCenter says Windows Server 2016, so that is what runs" → it is the value set at creation. Compare with the type VMware Tools reports.
- "The VM is named web01, so it runs a web server" → discover the processes and connections.
- "Give the JVM more heap than the Guest OS has free, for headroom" → memory the application cannot use is wasted, and the Guest OS starts paging.
- "One more agent costs little" → agents add up on every VM; count their total footprint.

## Metadata
```yaml
id: guest-os/system/concepts/guest-os-configuration-review
retriever_guide: what-to-set
scope: guest-os
technology:
- system
- storage
- network
pillar:
- performance
- compliance
- capacity
product:
- windows
- linux
layer:
- guest-os
internal_derive:
- operations-management/sp5-framework/configuration-management
related:
- vsphere/object-types/vm/configuration/vm-configuration-review
- guest-os/system/concepts/guest-os-sizing
- vsphere/architecture/vm-vs-guest-os
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Configuration Management > Review List > Consumer Objects > Guest OS (pp. 134-135)'
corrections: []
review_notes:
- 'Section ''Drivers'': the book links a networking driver best-practice page; the link target is not in the source text.'
- 'Section ''Applications'', JVM: ''the Guest OS starts paging'' in the trap is Claude''s addition.'
status: draft
```
