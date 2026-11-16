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
- Three proposals are on the table: (1) raise the Paravirtual SCSI queue depth to 254 in the VM; (2) open a case with the array vendor because the device latency is 8 ms; (3) raise Disk.SchedNumReqOutstanding for the LUN on the host.

Which statements about where the 25 ms is spent, what limits the I/O rate and the three proposals are correct?

- A. About 9 ms of the 25 ms is spent inside Windows, before the requests reach the virtual disk.
- B. The virtual disk holds about 64 requests at a time, the default Paravirtual SCSI device queue depth.
- C. Besides DQLEN, the adapter queue depth of the HBA (AQLEN) also caps the commands this LUN can have active.
- D. A KAVG of 8 ms shows that the VMkernel storage code on this host is slow and needs attention.
- E. The device latency of 8 ms shows the array is the bottleneck, so a case with the array vendor is the fix.
- F. The LUN queue depth caps the I/O rate: 32 commands at 8 ms each allow about 4,000 per second.
- G. Raising the Paravirtual SCSI queue depth to 254 shortens the time per I/O that the application sees.
- H. Raising Disk.SchedNumReqOutstanding on the LUN lets the virtual disk keep more commands at the device.
- I. The GAVG of 16 ms is the whole time that the application waits for each of its I/Os.
- J. Here the requests beyond the Paravirtual SCSI queue depth wait in the VMkernel, inside the 7.8 ms of QAVG.
- K. The first change is to raise the device queue depth of the LUN, or to spread the data over more LUNs.
- L. With the array at 30% of its rated IOPS, a flat I/O rate with growing latency points to a queue limit.
- M. The VMkernel stack itself, outside its device queue, adds only about 0.2 ms.
- N. Of the 100 requests Windows counts, about 32 are at the device and about 31 wait in the VMkernel queue.
- O. Once both limits are raised, success shows as ACTV above 32, QUED near 0 and Windows latency close to GAVG.

## Likely wrong answer
- D: "KAVG of 8 ms means the VMkernel is slow."
- E: "The array is slow (DAVG 8 ms): open a case with the vendor."
- G: "The Paravirtual SCSI queue is too small, so raise it to 254."
- H: "Raise Disk.SchedNumReqOutstanding so the VM gets more commands to the LUN."

## Expected key points
- Answer: A, B, C, F, K, L, M, N, O.
- A is correct: 25 ms in Windows minus 16 ms of GAVG (vCenter and esxtop) is 9 ms in the guest queue: 36 / 4,000 = 9 ms.
- B is correct: 4,000 x 0.016 = 64 requests at the virtual disk, the default device queue depth; the other 100 - 64 = 36 wait in Windows.
- C is correct: with one VM and one virtual disk on the device, the device queue depth (DQLEN) and the adapter queue depth limit the commands; the adapter queue holds the commands of all its devices, so a raised DQLEN helps only within it.
- D is wrong: KAVG of 8.0 ms is almost all QAVG (7.8 ms), the wait in the full device queue (DQLEN 32, ACTV 32, %USD 100, QUED 31). The cause is the queue depth, not the VMkernel code.
- E is wrong: a DAVG above 5 ms rightly sends the operator to check the array, and the array reports 30% of its rated IOPS and no errors on the LUN, so it is not the bottleneck. The ceiling is the LUN queue (F); a case with the vendor is not the fix.
- F is correct: the smaller concurrency limit on the path sets the throughput: 32 / 0.008 = 4,000 IOPS, the observed rate.
- G is wrong: the device still takes 32 commands at once, so the 9 ms moves from the guest queue to the VMkernel queue and the total stays at 25 ms or grows.
- H is wrong: Disk.SchedNumReqOutstanding applies only when several virtual disks issue I/O to the device. With one VM and one virtual disk, DQLEN and the adapter queue depth limit the commands, so the setting changes nothing here.
- I is wrong: GAVG starts at the virtual device; the 9 ms in the guest queue is outside it.
- J is wrong: QUED 31 = 4,000 x 0.0078 is the excess over DQLEN 32 of the 64 requests at the virtual disk; the other 36 requests are outside GAVG, which is 9 ms below the Windows latency. A request beyond the Paravirtual SCSI queue depth waits in the Guest OS, before the virtual device takes it; a request beyond DQLEN waits in the VMkernel.
- K is correct: raise the device queue depth of the LUN (the HBA driver parameter, within the adapter queue depth and the limits of the array ports), or spread the files over more LUNs: each LUN has its own DQLEN, so more LUNs allow more commands at the array at once. Then raise the Paravirtual SCSI queue depth and ring pages if a guest wait remains.
- L is correct: the array has spare capacity (30%), so it is not the cause; with the array ruled out, a flat I/O rate with growing latency is the signature of a queue limit.
- M is correct: KAVG 8.0 minus QAVG 7.8 = 0.2 ms; about 1 request at 4,000 per second.
- N is correct: 4,000 x 0.008 = 32 at the device, 4,000 x 0.0078 = 31 in the VMkernel queue, about 1 in the stack and 36 in the guest queue: 100 in all.
- O is correct: check with the same figures: ACTV above 32, QUED near 0, a higher IOPS rate at a similar DAVG, and Windows latency close to GAVG. Windows latency close to GAVG needs the guest wait gone too, hence both limits.

## Notes
- Public source: esxtop storage device panel, vSphere Monitoring and Performance 9.1 (last updated 2026-11-09): DQLEN, ACTV, QUED, %USD, LOAD, DAVG/cmd, KAVG/cmd, GAVG/cmd, QAVG/cmd. Broadcom KB 344099 (legacy 1008205): GAVG = DAVG + KAVG. Broadcom KB 343323 (legacy 2053145): the Paravirtual SCSI default queue depth is 64 for a device and 254 for an adapter (the Windows driver). Broadcom KB 344706 (legacy 1268): Disk.SchedNumReqOutstanding does not apply when one VM with one virtual disk is active on the LUN, as here. Microsoft Learn, "Using Storage-related Parameters and Performance Counters": Avg. Disk Queue Length = Disk Transfers/sec x Disk sec/Transfer, and the requests include those waiting in a Storport queue.
- Why one answer: the numbers satisfy Little's Law at every layer (100 = 36 + 31.2 + 0.8 + 32), so the split is forced, and the ceiling DQLEN / DAVG equals the observed rate.
- Debatable risk: low. A request beyond the Paravirtual SCSI device queue depth waits in the Guest OS, not in QAVG; A and B also follow from the numbers alone (Windows 25 ms against GAVG and vCenter 16 ms; 4,000 x 0.016 = 64), and J is stated for this case, where QUED 31 = 4,000 x 0.0078 holds only the excess over DQLEN. Performance Best Practices for vSphere 9.1 (revision 20260624): "The depth of the queue of outstanding commands in the guest operating system SCSI driver can significantly impact disk performance" (p. 60), and a small virtual SCSI adapter queue "can hamper the ability of the guest OS to pass data to the next layer down the storage stack" (p. 87). The way to raise the device queue depth depends on the HBA driver and was not verified in a vendor document. The array headroom is stated in the prompt. GAVG is read as starting at the virtual device.
- Prepared from the ESXi storage I/O path source file.
- Review 2026-11-14: J restated for this case and L tied to the array's 30%, so each is decided by the prompt's numbers; O names both limits.
- Review 2026-11-15: H (add vCPUs) replaced by the Disk.SchedNumReqOutstanding misconception, and proposal (3) in the stem with it; C (the VMkernel queue wait, tested by 0043 and 0086) replaced by the adapter queue depth. Key unchanged.

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
misconception: [D,E,G,H]
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
source_path: "Synthetic, 2026-11-13: ESXi storage I/O path source"
misconception_type: [layer-confusion, tool-confusion]
status: draft
```
