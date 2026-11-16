# Device queue full in esxtop batch data

## Prompt
- The application on VMs whose disks sit on LUN naa.624a9370a1 reports slow transactions between 10:20 and 10:40.
- [The attached CSV](0086/esx-07-esxtop-batch-disk-devices-1-hour.csv) is one hour of esxtop batch output of host esx-07 (`esxtop -b -d 60`), reduced to two LUNs and the fields of the disk device panel.

Which statements about where the latency is added, and what to check, are correct?

- A. In the ESXi kernel: the device queue is full, so commands wait before the array.
- B. In the array: DAVG is the cause, so the storage team must look at the LUN.
- C. In the Guest OS: the VMs queue the IO inside Windows and Linux before sending it.
- D. In the VMs' virtual SCSI adapters: their queue depth is exceeded, and QAVG shows that wait.
- E. Compare the queue depth of 32 with the HBA and the array's per-LUN guidance.
- F. In the window, CMDS/s × QAVG gives about QUED: those commands wait in the kernel.

## Likely wrong answer
B: blaming the array.

## Expected key points
- Answer: A, E, F.
- A is correct: from 10:20 to 10:40 ACTV equals DQLEN (32), so %USD = ACTV / DQLEN = 100%: the device queue is full. LOAD = (ACTV + QUED) / DQLEN is about 2.8 to 3.5: about twice as many commands wait in the kernel as the device accepts. KAVG (and QAVG inside it) carries the added time: GAVG about 3.3 ms = KAVG 2.3 ms + DAVG 1.1 ms on average. The other LUN, naa.624a9370b2, has no queue at the same time.
- B is wrong: DAVG (the HBA, the fabric and the array) stays near 1 ms through the window. The array serves each command as fast as before; the commands wait before they get there.
- C is wrong: GAVG = KAVG + DAVG accounts for the whole rise; the added time is in the kernel, below the Guest OS, whose queues esxtop does not see.
- D is wrong: a request above the virtual SCSI adapter's queue depth waits in the Guest OS, before the virtual device, and adds nothing to KAVG or QAVG. A high QAVG means a VMkernel limit holds the commands; here ACTV at DQLEN shows it is the device queue.
- E is correct: the device queue depth is the limit here, and queue depths must match along the stack (HBA, device, array). Spreading the busy disks over more LUNs also gives more device queues.
- F is correct: Little's law at the kernel layer: at 10:20, 30,770.6 commands/s × 2.5 ms = 77 = QUED (and 30,770.6 × 1.04 ms = 32 = ACTV at the device). The queued commands are held in the VMkernel.

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Revised 2026-11-12 for question set 1.0: the screenshot removed; the batch output reduced to two devices, one-minute samples and the panel's field names; the Storage I/O Control option removed (deprecated in VCF 9.0). Counts only after author approval.
- 2026-11-14: the stem bullet that read the CSV for the candidate (ACTV equal to DQLEN, QUED, %USD, LOAD, KAVG against DAVG in the window) removed (design.md 6.2); question made plural. Practical half of 0043 (project/question-pairing-2026-11-14.md, A16). Key unchanged.
- Review 2026-11-15: the key point for C names the mechanism. Key unchanged.
- Changed in the 2026-11-15 audit: D ("Nowhere: a LOAD above 1 is normal", a near-throwaway) replaced by the Paravirtual SCSI queue read as QAVG (false: esxi-storage-io-path, Misconceptions); F added (true: Little's law, CMDS/s × QAVG = QUED); A key point gives the CSV averages. Key changed from A, E to A, E, F.
- Left open: real `esxtop -b` output has perfmon-style headers ("Average Driver MilliSec/Command"), one row per sample with a column per device and counter. Regenerating the CSV in that form waits for the esxtop template's header/data field-count mismatch to be resolved (project/sources/export-templates/esxtop).

## Metadata
```yaml
id: "0086"
title: "Device queue full in esxtop batch data"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/storage-configuration-review
  - vsphere/technology/storage/concepts/esxi-storage-io-path
knowledge_main: vsphere/tools/esxtop/storage
attachments:
  - 0086/esx-07-esxtop-batch-disk-devices-1-hour.csv
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [A, E, F]
misconception: [B]
misconception_type: [layer-confusion]
pair: "0043"
status: draft
```
