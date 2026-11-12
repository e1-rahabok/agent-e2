# Guest OS Disk Queue

## Layer
- Guest OS layer: Windows or Linux, running on the VM. The VM is a virtual motherboard; it cannot see inside the Guest OS.
- VMware Tools collects this counter inside the Guest OS and vCenter and VCF Operations store it on the VirtualMachine object. That is a data path, not ownership: the counter belongs to the Guest OS.

## Meaning
- Queue inside the Windows or Linux storage subsystem, above the SCSI driver (LSI Logic, PVSCSI). IO in this queue has not reached the driver or the VM.
- With a VMware driver (PVSCSI) and a high queue: discuss with Broadcom support.

| VMware Tools counter | Windows source (WMI) |
|---|---|
| guest.disk.queue | Win32_PerfFormattedData_PerfDisk_PhysicalDisk _Total CurrentDiskQueueLength (point in time at the end of the collection period) |
| guest.disk.queueAvg | Win32_PerfFormattedData_PerfDisk_PhysicalDisk _Total AvgDiskQueueLength (average over the period) |

## Reading it
- Windows documentation: queue length minus spindles should average below 2.
- High guest queue with low VM IOPS: IO is stuck in the OS.
- Compare with VM outstanding IO. They do not correlate: the VM tracks IO sent; the guest queue tracks IO not yet sent.
- VM disk latency stays good: it covers only IO that reached the hypervisor. The application still feels the delay.
- No universal threshold; varies by application.

## Observed values
- 3,000 VMs, 3 months: about 70% below 10; about 10% above 100.
- Some values are extreme (spikes above 1,000). Guest queues are rarer than latency spikes.
![Guest OS disk queue timeline for one VM: regular spikes, last above 1,000](images/guest-os-disk-queue-spikes-timeline.png)
- 20-second peak about 200-250 while the 5-minute average stays above 125: volatile, not sustained.
![Guest disk queue distribution across 3,000 VMs](images/guest-os-disk-queue-distribution-across-vms.png)
![Guest queue spikes with good VM latency](images/guest-os-disk-queue-spikes-while-vm-disk-latency-good.png)

## Guest OS storage questions
| Area | Required data |
|---|---|
| Configuration | Per partition: name, filesystem (NTFS, ext4), network or local, block size. Ideally the partition-to-virtual-disk mapping. |
| Capacity | Per partition: configured and used space; free space in GB and %. Alert before full: the OS crashes. Exclude network drives (shared), except VDI user profiles. |
| Reclamation | From free space. Hard: partitions must shrink. |
| Performance | Queue, read and write latency, IOPS, throughput. |

## Misconceptions
- "VM latency is fine, so the guest sees no storage delay" → IO stuck in the guest queue is invisible to the VM.

## Metadata
```yaml
id: guest-os/storage/disk-queue
retriever_guide: metric-meaning
scope: guest-os
technology:
- storage
pillar:
- performance
product:
- windows
- linux
- vcf-operations
layer:
- guest-os
metric_class: contention
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/concepts/guest-os-vs-vm-storage
- guest-os/system/guest-os-performance
images:
  - path: images/guest-os-disk-queue-spikes-timeline.png
    product: [windows]
    object: [VirtualMachine]
    metric: ['Guest OS Disk Queue']
    image_type: timeline
    sample: '1 VM'
  - path: images/guest-os-disk-queue-distribution-across-vms.png
    product: [windows]
    object: [VirtualMachine]
    metric: ['Guest OS Disk Queue']
    image_type: distribution
    sample: '3,000 VMs'
  - path: images/guest-os-disk-queue-spikes-while-vm-disk-latency-good.png
    product: [windows]
    object: [VirtualMachine]
    metric: ['Guest OS Disk Queue', 'VM Disk Latency']
    image_type: timeline
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: MS Windows > Storage
corrections: []
review_notes: []
status: draft
```
