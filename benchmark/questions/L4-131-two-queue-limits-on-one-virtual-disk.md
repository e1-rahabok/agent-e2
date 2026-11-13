# Two queue limits on one virtual disk

## Prompt
- A Windows Server 2022 VM runs a batch job on one virtual disk, on a Paravirtual SCSI controller with default driver settings. The virtual disk is on a VMFS datastore backed by one Fibre Channel LUN of an ESX 9.1 host. This VM is the only VM that uses the LUN.
- Over a 5-minute window of the batch job the application team reports 25 ms per I/O and I/O rates that stay flat while the job slows down.
- Performance Monitor, PhysicalDisk of the data disk: Disk Transfers/sec 4,000; Avg. Disk sec/Transfer 0.025; Avg. Disk Queue Length 100.
- vCenter, the same virtual disk: 4,000 IOPS; virtual disk latency 16 ms.
- esxtop, disk device panel, the LUN, the same 5 minutes:

| CMDS/s | DQLEN | ACTV | QUED | %USD | LOAD | DAVG/cmd | KAVG/cmd | QAVG/cmd | GAVG/cmd |
|---|---|---|---|---|---|---|---|---|---|
| 4,000 | 32 | 32 | 31 | 100 | 1.97 | 8.0 | 8.0 | 7.8 | 16.0 |

- The array administrator reports that the front-end ports and the controllers of the array run at about 30% of their rated IOPS, and sees no errors on the LUN. CPU in the VM and on the host is low.
- Three proposals are on the table: (1) raise the Paravirtual SCSI queue depth to 254 in the VM; (2) open a case with the array vendor because the device latency is 8 ms; (3) add vCPUs to the VM.

Split the 25 ms the application sees into the places where the time is spent. What limits the I/O rate? Which proposal helps, which does not, and what do you change first?

## Likely wrong answer
"The array is slow (DAVG 8 ms), or the Paravirtual SCSI queue is too small, so raise it to 254." Or: "KAVG of 8 ms means the VMkernel is slow."

## Expected key points
- The 25 ms splits into about 9 ms in the guest queue, 7.8 ms in the VMkernel device queue, 0.2 ms in the VMkernel stack and 8.0 ms at the device: 9 + 7.8 + 0.2 + 8.0 = 25.
- Guest queue: the virtual disk holds 4,000 x 0.016 = 64 requests, which is the default Paravirtual SCSI device queue depth. The other 100 - 64 = 36 requests of the Windows queue wait in Windows, which is 36 / 4,000 = 9 ms, the difference between 25 ms and the vCenter and esxtop GAVG of 16 ms.
- VMkernel: the device queue depth (DQLEN) is 32 and all 32 slots are active (ACTV 32, %USD 100). 31 commands wait (QUED 31, LOAD about 2), which is 4,000 x 0.0078 = 31 commands and 7.8 ms of QAVG. KAVG of 8.0 ms is almost all QAVG, so the VMkernel code is not slow.
- Device: 32 commands active at 8.0 ms each. The 100 requests in Windows are 36 in the guest queue, 31 in the VMkernel queue, about 1 in the stack and 32 at the device.
- What limits the I/O rate is the smaller concurrency limit on the path, the device queue depth: 32 commands at a time at 8 ms each is 32 / 0.008 = 4,000 IOPS, the observed rate. The array has spare capacity (30%), so it is not the cause, and a flat I/O rate with growing latency is the signature of a queue limit.
- Proposal 1 alone does not help. The device still takes 32 commands at once, so the 9 ms moves from the guest queue to the VMkernel queue and the total stays at 25 ms or grows. Proposal 2 is not supported: the array runs at 30% and the 8 ms is the device latency at this concurrency, with no sign of saturation. Proposal 3 does not help: CPU is low and the wait is queueing.
- Change first: raise the device queue depth of the LUN (the driver parameter of the HBA, within the adapter queue depth and the limits of the array ports), or spread the files over more LUNs. Then raise the Paravirtual SCSI queue depth and ring pages if a guest wait remains. Check with the same figures: ACTV above 32, QUED near 0, a higher IOPS rate at a similar DAVG, and Windows latency close to GAVG.
- The method: three measurements (the Windows latency, GAVG, and the split of GAVG into DAVG and KAVG with QAVG) put the time in the guest queue, the VMkernel queue or the device. Requests at each place are the rate x the time spent there.

## Notes
- Public source: esxtop storage device panel, vSphere Monitoring and Performance 9.1 (last updated 2026-11-09): DQLEN, ACTV, QUED, %USD, LOAD, DAVG/cmd, KAVG/cmd, GAVG/cmd, QAVG/cmd. Broadcom KB 344099 (legacy 1008205): GAVG = DAVG + KAVG. Broadcom KB 343323 (legacy 2053145): the Paravirtual SCSI default queue depth is 64 for a device and 254 for an adapter. Microsoft Learn, "Using Storage-related Parameters and Performance Counters": Avg. Disk Queue Length = Disk Transfers/sec x Disk sec/Transfer, and the requests include those waiting in a Storport queue.
- Why one answer: the numbers satisfy Little's Law at every layer (100 = 36 + 31.2 + 0.8 + 32), so the split is forced, and the ceiling DQLEN / DAVG equals the observed rate.
- Debatable risk: the author's working source says a request that exceeds the Paravirtual SCSI queue depth is seen as QAVG; this question reads it as a wait in the guest (author question Q195). The way to raise the device queue depth depends on the HBA driver and was not verified in a vendor document. The array headroom is stated in the prompt. GAVG is read as starting at the virtual device.
- Prepared from the ESXi storage I/O path source file.

## Metadata
```yaml
id: "0361"
title: "Two queue limits on one virtual disk"
product: [vsphere, windows]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [vm, esxi, datastore, guest-os]
tool: [esxtop, vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-io-path
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - guest-os/storage/windows-storage-io-path
  - guest-os/storage/disk-queue
knowledge_main: vsphere/technology/storage/concepts/esxi-storage-io-path
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 from the ESXi storage I/O path source (project/plan.md)"
misconception_type: [layer-confusion, tool-confusion]
status: draft
```
