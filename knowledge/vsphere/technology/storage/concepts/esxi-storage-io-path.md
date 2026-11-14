# ESXi storage I/O path

## Control plane
- Every layer between the Guest OS driver and the physical controller passes a command descriptor and an address translation. The layers below the Guest OS are a control plane: they route and queue commands.
- A counter at one of these layers counts commands, not bytes. A 4 KB command and a 1 MB command each count as one command while active.

## Path of one write command
| Step | Layer | What it does |
|---|---|---|
| 1 | Guest application and file system | Prepare the data and translate the file offset into a Guest OS block address. |
| 2 | Guest driver (pvscsi) | Writes the command into the Paravirtual SCSI ring in shared memory and signals the virtual adapter. |
| 3 | Virtual device layer | Takes the command from the ring and translates guest memory addresses into host addresses. |
| 4 | VMFS | Maps the offset in the virtual disk file to a block of the datastore device. |
| 5 | VMkernel storage core | Queues the command in the queue of the device when the device queue depth is reached. |
| 6 | Pluggable Storage Architecture or High Performance Plug-in | Selects the path and checks queue depths. |
| 7 | Native driver | Converts the command to the device protocol and writes it to the queue of the physical controller. |
| 8 | Physical controller and device | Execute the command. |

## Queues on the path
| Queue | Limit | Where the wait shows |
|---|---|---|
| Guest queue (Storport in Windows, block layer in Linux) | Paravirtual SCSI queue depth: 64 per device and 254 per adapter by default | In the Guest OS counters. ESXi latency does not include it. |
| Paravirtual SCSI ring | 8 pages by default | In the Guest OS: the driver waits for a free entry. |
| VMkernel device queue | Device queue depth (esxtop DQLEN) | QUED, QAVG and KAVG in esxtop. |
| Adapter queue | Adapter queue depth (esxtop AQLEN) | In esxtop, as the sum of the commands of its devices. |
| Device and array | Set by the hardware | DAVG in esxtop. |

- Each limit holds the requests above it. A request that waits for a free slot of the Paravirtual SCSI device waits in the Guest OS, before the virtual device takes it. A request that waits for a free slot of the device queue waits in the VMkernel.
- Raising a limit above a smaller limit below it moves the wait down the path. It does not shorten the total time.

## esxtop figures for a device
- DQLEN is the current queue depth of the device. ACTV is the number of commands active in the VMkernel. QUED is the number of commands queued in the VMkernel. %USD is the share of the queue depth used by active commands. LOAD is the active plus the queued commands, divided by the queue depth.
- LOAD above 1 means commands are queued in the VMkernel: the device queue is full.
- DAVG is the average device latency per command. KAVG is the average VMkernel latency per command. QAVG is the average queue latency per command. GAVG is DAVG plus KAVG.
- The queue depth sets a ceiling on the throughput of a device: the commands active at one time divided by the device latency. At a DQLEN of 64 and a DAVG of 4 ms the ceiling is 16,000 commands per second.
- Little's Law holds at each layer: the commands active at the device equal CMDS/s x DAVG, and the commands queued in the VMkernel equal CMDS/s x QAVG.
- The meaning and healthy values of DAVG, KAVG and QAVG, and the NFS case: [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](esxi-storage-latency-stack.md).

## Locating the delay with three measurements
- The latency measured inside the Guest OS (Windows Avg. Disk sec/Transfer, Linux await), GAVG for the virtual disk, and the split of GAVG into KAVG and DAVG, put the time in one of four places.
| Difference | Where the time is | Check |
|---|---|---|
| Guest latency minus GAVG | The guest queue, above the virtual device | Paravirtual SCSI queue depth and ring pages, the number of virtual disks |
| QAVG, most of KAVG | The VMkernel device queue | DQLEN against ACTV and QUED, other VMs on the device |
| DAVG | The device, the fabric or the array | Array load, paths, the fabric |
| KAVG minus QAVG | The VMkernel stack itself | A small value. A large value points to the host. |
- Requests at each place follow from the rate and the time spent there: the guest queue is the rate x (guest latency - GAVG); the VMkernel queue is the rate x QAVG; the device is the rate x DAVG. They add up to the Guest OS queue figure: [`guest-os/storage/windows-storage-io-path`](../../../../guest-os/storage/windows-storage-io-path.md) and [`guest-os/storage/linux-storage-io-path`](../../../../guest-os/storage/linux-storage-io-path.md).
- Two limits can act at the same time, one in the guest and one in the VMkernel. The smaller of the concurrency limits on the path sets the throughput. Fix it first, then read the figures again.

## Misconceptions
- "High KAVG means ESXi is slow" → KAVG is mostly QAVG, the wait in the device queue. The cause is the queue depth, not the VMkernel code.
- "A VM that exceeds the Paravirtual SCSI queue depth shows a high KAVG" → it waits in the Guest OS, before the virtual device. ESXi latency stays low.
- "Raising the Paravirtual SCSI queue depth speeds up a VM whose device queue is full" → the commands move from the guest queue to the VMkernel queue. The device still takes the same number at once.
- "GAVG is everything the application waits for" → GAVG starts at the virtual device. The wait in the guest queue is outside it.
- "There is one queue depth" → the guest device and adapter, the VMkernel device and the adapter each have their own.

## Metadata
```yaml
id: vsphere/technology/storage/concepts/esxi-storage-io-path
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive:
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
related:
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/storage/concepts/storage-layers
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
- guest-os/storage/disk-queue
- guest-os/storage/windows-storage-io-path
- guest-os/storage/linux-storage-io-path
source:
  document: vSphere Monitoring and Performance 9.1, esxtop storage device, storage adapter and virtual machine storage panels (Broadcom TechDocs, last updated 2026-11-09); Broadcom KB 344099, Using esxtop to identify storage performance issues for ESXi (legacy 1008205); Broadcom KB 343323 (legacy 2053145)
  path: Using esxtop or resxtop in interactive mode > Storage device panel
corrections: []
review_notes:
- 'To check: Section ''Path of one write command'': the names and order of the layers below the Guest OS (virtual device layer, VMFS, the VMkernel storage core, the Pluggable Storage Architecture and the High Performance Plug-in), against the vSphere Storage documentation.'
- 'To check: Section ''Queues on the path'': that a command that exceeds the Paravirtual SCSI queue depth waits in the Guest OS and not in the VMkernel. It follows from how a driver queue depth works and from the Microsoft list of where a Windows request can wait; no vendor page states it. The working source file names the Paravirtual SCSI queue depth as a cause of a high KAVG or QAVG (author question Q195).'
- 'To check: Section ''Queues on the path'': the option Disk.SchedNumReqOutstanding, named in the working source as a limit that queues requests in the VMkernel. No Broadcom page was read for its default, its scope or its relation to the device queue depth, so the file does not state them.'
- 'To check: the working source states that ESX does not copy the data payload: the controller reads the guest pages by their host address. Not read in a vendor document, and not stated here. NFS, vSAN and other paths can differ.'
- 'To check: Section ''Locating the delay with three measurements'': the split by subtraction is a derivation from Little''s Law, not a vendor procedure. The vCenter and esxtop pages give one-line definitions only; the vSphere API reference definitions of totalLatency, kernelLatency, queueLatency and virtualDisk.totalReadLatency were not read.'
- 'To check: the thresholds differ by source: Broadcom KB 344099 gives 10 ms for sustained DAVG, KAVG and GAVG, a VMware blog gives 2 ms for KAVG, the existing latency stack file gives 0.5 ms for KAVG. The values belong in the threshold catalog, not here.'
- 'Source URL, esxtop storage device panel: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-monitoring-and-performance/performance-monitoring-utilities-resxtop-and-esxtop/using-esxtop-or-resxtop-in-interactive-mode/storage-device-panel.html'
- 'Source URL, Broadcom KB 344099: https://knowledge.broadcom.com/external/article?legacyId=1008205'
status: draft
```
