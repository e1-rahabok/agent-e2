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
| Guest queue (Storport in Windows, block layer in Linux) | Paravirtual SCSI queue depth, per device and per adapter | In the Guest OS counters. ESXi latency does not include it. |
| Paravirtual SCSI ring | 8 pages by default | In the Guest OS: the driver waits for a free entry. |
| VMkernel queue of a device shared by several virtual disks | Disk.SchedNumReqOutstanding (DSNRO) | QUED, QAVG and KAVG in esxtop. |
| VMkernel device queue | Device queue depth (esxtop DQLEN) | QUED, QAVG and KAVG in esxtop. |
| Adapter queue | Adapter queue depth (esxtop AQLEN) | In esxtop, as the sum of the commands of its devices. |
| Device and array | Set by the hardware | DAVG in esxtop. |

- Each limit holds the requests above it. Raising a limit above a smaller limit below it moves the wait down the path. It does not shorten the total time.
- A request above the Paravirtual SCSI device queue depth stays in the Guest OS storage stack: the guest driver does not write it into the ring, so the VMM sees no command. Its wait adds to the Guest OS latency and queue length, not to GAVG, KAVG or QAVG.
- Performance Best Practices for vSphere 9.1 places that wait in the guest: the queue depth of the guest SCSI driver limits the bandwidth a VM can push (p. 60), and guest operating systems queue by disk controller (p. 87).
- A request above the device queue depth (DQLEN), or above DSNRO on a device that several virtual disks share, waits in the VMkernel: esxtop counts it in QUED and its wait in QAVG, inside KAVG and GAVG.
- A Paravirtual SCSI depth above DQLEN or DSNRO lets one virtual disk fill the VMkernel queue, so raising it can raise QAVG; DQLEN or DSNRO still holds the commands.
- The Paravirtual SCSI defaults differ by guest driver: [`guest-os/storage/windows-storage-io-path`](../../../../guest-os/storage/windows-storage-io-path.md), [`guest-os/storage/linux-storage-io-path`](../../../../guest-os/storage/linux-storage-io-path.md).

## Disk.SchedNumReqOutstanding (DSNRO)
- Per device since vSphere 5.5; the host-wide option is deprecated. esxcli storage core device list shows it as No of outstanding IOs with competing worlds; esxcli storage core device set -d <device> -O <value> sets it (Broadcom KB 344706).
- DSNRO limits the commands all virtual disks on one host have outstanding to one device together, when more than one virtual disk issues I/O to it (Broadcom KB 344706).
- With one VM and one virtual disk active on the device, DSNRO does not apply: DQLEN and the adapter queue depth limit the commands.
- Default 32 commands; range 1 to the maximum queue depth of the device (Broadcom KB 344706).
- DSNRO is a host setting: every host that sees the device needs the same value.
- Raise DSNRO only on the storage vendor's advice: more commands reach the array at once (Broadcom KB 344706). Performance Best Practices for vSphere 9.1 names two uses: evening out the bandwidth of the VMs on one VMFS volume (p. 44), and NVMe with the High Performance Plug-in (p. 43).

## esxtop figures for a device
- DQLEN is the current queue depth of the device. ACTV is the number of commands active in the VMkernel. QUED is the number of commands queued in the VMkernel. %USD is the share of the queue depth used by active commands. LOAD is the active plus the queued commands, divided by the queue depth.
- LOAD above 1 means commands are queued in the VMkernel: the device queue is full.
- DAVG is the average device latency per command. KAVG is the average VMkernel latency per command. QAVG is the average queue latency per command. GAVG is DAVG plus KAVG.
- The queue depth sets a ceiling on the throughput of a device: the commands active at one time divided by the device latency. At a DQLEN of 64 and a DAVG of 4 ms the ceiling is 16,000 commands per second.
- Little's Law holds at each layer: the commands active at the device equal CMDS/s x DAVG, and the commands queued in the VMkernel equal CMDS/s x QAVG.
- The meaning and reading of DAVG, KAVG and QAVG, and the NFS case: [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](esxi-storage-latency-stack.md).

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
- "High KAVG and QAVG with low DAVG mean the VM exceeds its Paravirtual SCSI queue depth" → a request above the Paravirtual SCSI depth waits in the Guest OS, before the virtual device, and adds nothing to KAVG or QAVG. A high QAVG means a VMkernel limit holds the commands: DQLEN, DSNRO on a device that several virtual disks share, or an IOPS limit on a virtual disk.
- "Raising DSNRO speeds up a VM that is alone on its LUN" → with one VM and one virtual disk active on the device, DSNRO does not apply; DQLEN and the adapter queue depth limit the commands.
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
  document: vSphere Monitoring and Performance 9.1, esxtop storage device, storage adapter and virtual machine storage panels (Broadcom TechDocs, last updated 2026-11-09); Performance Best Practices for VMware vSphere 9.1 (revision 20260624); Broadcom KB 344099, Using esxtop to identify storage performance issues for ESXi (legacy 1008205); Broadcom KB 343323 (legacy 2053145); Broadcom KB 344706, Setting the Maximum Outstanding Disk Requests for virtual machines (legacy 1268)
  path: 'Using esxtop or resxtop in interactive mode > Storage device panel (DQLEN, QUED, QAVG). Performance Best Practices: ESX Storage Considerations > NVMe Recommendations (p. 43), General ESX Storage Recommendations (p. 44); Guest Operating System Storage Considerations (p. 60); vSAN Configuration and Use (p. 87)'
corrections: []
review_notes:
- 'To check: Section ''Path of one write command'': the names and order of the layers below the Guest OS (virtual device layer, VMFS, the VMkernel storage core, the Pluggable Storage Architecture and the High Performance Plug-in), against the vSphere Storage documentation.'
- 'To check: Section ''Disk.SchedNumReqOutstanding (DSNRO)'': the default of 32 against the vSphere 9.1 Storage documentation or the ESXCLI 9.1 reference (https://developer.broadcom.com/xapis/esxcli-command-reference/9.1.0/namespace/esxcli_storage.html). Read in the vSphere 6.5 Troubleshooting page Change the Outstanding IO Requests Setting (example output No of outstanding IOs with competing worlds: 32), which now redirects to TechDocs; Broadcom KB 344706 gives no default.'
- 'To check: Section ''Disk.SchedNumReqOutstanding (DSNRO)'': how the collective limit of Broadcom KB 344706 (all virtual disks on the host together) relates to the per-world WQLEN of the esxtop storage device panel. Neither page states it.'
- 'To check: the working source states that ESX does not copy the data payload: the controller reads the guest pages by their host address. Not read in a vendor document, and not stated here. NFS, vSAN and other paths can differ.'
- 'To check: Section ''Locating the delay with three measurements'': the split by subtraction is a derivation from Little''s Law, not a vendor procedure. The vCenter and esxtop pages give one-line definitions only; the vSphere API reference definitions of totalLatency, kernelLatency, queueLatency and virtualDisk.totalReadLatency were not read.'
- 'Source URL, esxtop storage device panel: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-monitoring-and-performance/performance-monitoring-utilities-resxtop-and-esxtop/using-esxtop-or-resxtop-in-interactive-mode/storage-device-panel.html'
- 'Source URL, Broadcom KB 344099: https://knowledge.broadcom.com/external/article?legacyId=1008205'
- 'Source URL, Broadcom KB 344706: https://knowledge.broadcom.com/external/article/344706/setting-the-maximum-outstanding-disk-req.html'
status: draft
```
