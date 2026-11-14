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

Which statements about where the 25 ms is spent, what limits the I/O rate and the three proposals are correct?

- A. About 9 ms of the 25 ms is spent inside Windows, before the requests reach the virtual disk.
- B. The virtual disk holds about 64 requests at a time, the default Paravirtual SCSI device queue depth.
- C. About 7.8 ms of each I/O is spent waiting in the VMkernel queue of the LUN, whose 32 slots are all busy.
- D. KAVG of 8 ms shows that the VMkernel storage code on this host is slow.
- E. The device latency of 8 ms shows the array is the bottleneck, so a case with the array vendor is the fix.
- F. The LUN queue depth caps the I/O rate: 32 commands at 8 ms each allow about 4,000 per second.
- G. Raising the Paravirtual SCSI queue depth to 254 shortens the time per I/O that the application sees.
- H. Adding vCPUs to the VM would raise its I/O rate.
- I. GAVG of 16 ms is the whole time the application waits for each I/O.
- J. Requests above the Paravirtual SCSI device queue depth wait in the VMkernel and show up as QAVG.
- K. The first change is to raise the device queue depth of the LUN, or to spread the data over more LUNs.
- L. A flat I/O rate with growing latency fits a queue limit rather than an array short of capacity.
- M. The VMkernel stack itself, outside its device queue, adds only about 0.2 ms.
- N. Of the 100 requests Windows counts, about 32 are at the device and about 31 wait in the VMkernel queue.
- O. After the fix, success shows as ACTV above 32, QUED near 0, and Windows latency close to GAVG.

## Likely wrong answer
- D: "KAVG of 8 ms means the VMkernel is slow."
- E: "The array is slow (DAVG 8 ms): open a case with the vendor."
- G: "The Paravirtual SCSI queue is too small, so raise it to 254."

## Expected key points
- Answer: A, B, C, F, K, L, M, N, O.
- A true: 25 ms in Windows minus 16 ms of GAVG (vCenter and esxtop) is 9 ms in the guest queue: 36 / 4,000 = 9 ms.
- B true: 4,000 x 0.016 = 64 requests at the virtual disk, the default device queue depth; the other 100 - 64 = 36 wait in Windows.
- C true: DQLEN 32 with ACTV 32 and %USD 100; QUED 31 = 4,000 x 0.0078, which is 7.8 ms of QAVG. LOAD about 2.
- D false: KAVG of 8.0 ms is almost all QAVG (7.8 ms), the wait in the device queue. The cause is the queue depth, not the VMkernel code.
- E false: the array runs at 30% with no errors; 8 ms is the device latency at this concurrency, with no sign of saturation.
- F true: the smaller concurrency limit on the path sets the throughput: 32 / 0.008 = 4,000 IOPS, the observed rate.
- G false: the device still takes 32 commands at once, so the 9 ms moves from the guest queue to the VMkernel queue and the total stays at 25 ms or grows.
- H false: CPU is low and the wait is queueing.
- I false: GAVG starts at the virtual device; the 9 ms in the guest queue is outside it.
- J false: a request above the Paravirtual SCSI device queue depth waits in the Guest OS, before the virtual device takes it; ESXi latency does not include it. A request above the device queue depth (DQLEN) waits in the VMkernel.
- K true: raise the device queue depth of the LUN (the HBA driver parameter, within the adapter queue depth and the limits of the array ports), or spread the files over more LUNs. Then raise the Paravirtual SCSI queue depth and ring pages if a guest wait remains.
- L true: the array has spare capacity (30%), so it is not the cause; a flat I/O rate with growing latency is the signature of a queue limit.
- M true: KAVG 8.0 minus QAVG 7.8 = 0.2 ms; about 1 request at 4,000 per second.
- N true: 4,000 x 0.008 = 32 at the device, 4,000 x 0.0078 = 31 in the VMkernel queue, about 1 in the stack and 36 in the guest queue: 100 in all.
- O true: check with the same figures: ACTV above 32, QUED near 0, a higher IOPS rate at a similar DAVG, and Windows latency close to GAVG.

## Notes
- Public source: esxtop storage device panel, vSphere Monitoring and Performance 9.1 (last updated 2026-11-09): DQLEN, ACTV, QUED, %USD, LOAD, DAVG/cmd, KAVG/cmd, GAVG/cmd, QAVG/cmd. Broadcom KB 344099 (legacy 1008205): GAVG = DAVG + KAVG. Broadcom KB 343323 (legacy 2053145): the Paravirtual SCSI default queue depth is 64 for a device and 254 for an adapter. Microsoft Learn, "Using Storage-related Parameters and Performance Counters": Avg. Disk Queue Length = Disk Transfers/sec x Disk sec/Transfer, and the requests include those waiting in a Storport queue.
- Why one answer: the numbers satisfy Little's Law at every layer (100 = 36 + 31.2 + 0.8 + 32), so the split is forced, and the ceiling DQLEN / DAVG equals the observed rate.
- Debatable risk: the author's working source says a request that exceeds the Paravirtual SCSI queue depth is seen as QAVG; this question reads it as a wait in the guest (author question Q195). The way to raise the device queue depth depends on the HBA driver and was not verified in a vendor document. The array headroom is stated in the prompt. GAVG is read as starting at the virtual device.
- Prepared from the ESXi storage I/O path source file.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Options A, B and J follow the knowledge file's reading of the Paravirtual SCSI limit (Q195 has no recorded answer).

## Metadata
```yaml
id: "0361"
title: "Two queue limits on one virtual disk"
product: [vsphere, windows]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,B,C,F,K,L,M,N,O]
misconception: [D,E,G]
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
