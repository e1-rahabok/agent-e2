# High disk latency at low IOPS

## Prompt
- sql-07 is a VM with three virtual disks on one VMFS datastore of an FC array.
- VCF Operations, last hour:

| Virtual disk | Use | Read IOPS | Read latency | Write IOPS | Write latency |
|---|---|---|---|---|---|
| scsi0:0 | OS | 4 | 1.1 ms | 6 | 0.9 ms |
| scsi0:1 | Data | 30 | 24 ms | 5 | 1.3 ms |
| scsi0:2 | Log | 1 | 0.8 ms | 4 | 1.0 ms |

- The storage team says the array is idle and reports 0.6 ms for the LUN, so storage cannot be the cause.

Which statements about this latency and the checks that find where it comes from are correct?

- A. Latency can be high at low IOPS, because each layer below the VM has its own queue.
- B. At 30 IOPS the data disk is not busy, so its latency cannot be a storage problem.
- C. The problem sits in one disk and one direction: the reads of scsi0:1.
- D. A KAVG line that does not follow the DAVG line over the hour shows a fault in the host.
- E. With the array at 0.6 ms and the VM at 24 ms, the extra time is added between the two.
- F. Aborted commands, bus resets and dropped FC frames add delay at any load: check they are 0.
- G. Because the writes of scsi0:1 are fast, the 24 ms of reads must be spent inside the Guest OS.
- H. On a healthy host, nearly all of GAVG is DAVG, while KAVG stays near 0.
- I. On the host, split GAVG into KAVG and DAVG for the LUN behind the datastore.
- J. KAVG high with DAVG low points to the array, since the array returns the data.
- K. DAVG high while the array reports 0.6 ms points to the fabric or the HBA configuration.
- L. DAVG, KAVG and GAVG all below 10 ms on the host would rule out the host and the array.

## Answers
A, C, E, F, H, I, K

## Explanation
- A is correct: every layer below the VM has its own queue (virtual disk, kernel, adapter, fabric, array). Check outstanding I/O with the latency.
- B is wrong: the misconception. Queues and errors add latency at any load.
- C is correct: work on that disk's reads; the VM total hides it, and read and write often have different causes.
- D is wrong: kernel latency and device latency need not correlate; when both are healthy, KAVG stays near 0 whatever DAVG does, so a KAVG line that ignores DAVG is the normal case, not a fault.
- E is correct: the time is added in the host, the HBA or the fabric.
- F is correct: aborted commands and bus resets should be 0 all the time; dropped frames on FC are a sign of contention with an availability impact.
- G is wrong: the VM's virtual disk latency starts below the Guest OS; only one side being slow is common and points to that side's cause, not to the guest.
- H is correct: the bulk of the latency should come from the device; KAVG is near 0 on a healthy host, and a higher KAVG means commands queue in the VMkernel (QAVG).
- I is correct: the split tells kernel latency (the host) from device latency (the HBA, fabric or array).
- J is wrong: KAVG high with DAVG low is queuing inside ESXi: a high QAVG means a VMkernel limit holds the commands (the device queue depth DQLEN, DSNRO on a device that several virtual disks share, or an IOPS limit on a virtual disk), or the adapter is saturated.
- K is correct: DAVG runs from the HBA to the array and back; with the array at 0.6 ms, the difference is in the fabric or the HBA configuration.
- L is wrong: 10 ms (Broadcom KB 344099) is an upper bound for sustained latency on any array, not a healthy level. A KAVG of several ms is time in a VMkernel queue, and on an FC array that reports 0.6 ms a DAVG near 10 ms points to the fabric or the HBA. Read KAVG against QAVG and DAVG against the array's own latency.
- Misconception: B: "At 30 IOPS the disk is not busy, so the latency cannot be a storage problem."

## Notes
- Synthetic, 2026-11-05. Revised 2026-11-12 for question set 1.0: per-disk values and the array's own reading added. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The old key's KAVG level (0-1 ms in the vSphere documentation) is left out of the options; the knowledge files give 0.5 ms.
- Audit 2026-11-15 (redundancy): D (command-weighted total latency; kept by the pair 0044/0414) replaced by "kernel latency follows device latency" (false); H (redo-log snapshot slows reads; kept by 0187 and 0045) replaced by "on a healthy host GAVG is mostly DAVG" (true); L (percentile, not the maximum; kept by the pair 0081/0405) replaced by the 10 ms rule of Broadcom KB 344099 (false, threshold transplanted). E and F shortened (truth unchanged). J key point names the VMkernel limits behind a high QAVG; esxi-storage-io-path added to `knowledge`. Key unchanged: A, C, E, F, H, I, K.
- Re-review 2026-11-16: D and H were paired "On a healthy host" statements, so H decided D; D now reads a KAVG line that ignores DAVG as a host fault (false: esxi-storage-latency-stack, Example). The note on snapshot-impact removed: the snapshot option left in the 2026-11-15 audit and `knowledge` no longer lists it. Key unchanged: A, C, E, F, H, I, K.

## Metadata
```yaml
id: "0062"
title: "High disk latency at low IOPS"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [B]
input: [text]
object: [vm, esxi]
tool: [vcf-operations, esxtop]
knowledge:
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/concepts/esxi-storage-io-path
knowledge_main: vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: [consumption-as-contention, average-hides-worst, threshold-transplanted]
status: draft
```
