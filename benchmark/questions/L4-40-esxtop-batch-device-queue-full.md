# Device queue full in esxtop batch data

## Prompt
- The application on VMs whose disks sit on LUN naa.624a9370a1 reports slow transactions between 10:20 and 10:40.
- [The attached CSV](0086/esx-07-esxtop-batch-disk-devices-1-hour.csv) is one hour of esxtop batch output of host esx-07 (`esxtop -b -d 60`), reduced to two LUNs and the fields of the disk device panel.
- From 10:20 to 10:40, naa.624a9370a1 shows ACTV equal to DQLEN, QUED above 0, %USD 100 and LOAD near 3. KAVG/cmd rises above 2 ms while DAVG/cmd stays near 1 ms.

Where is the latency added, and what do you check?

- A. In the ESXi kernel: the device queue is full, so commands wait before the array.
- B. In the array: DAVG, the time from the HBA to the array and back, is the cause.
- C. In the Guest OS: the VMs queue the IO inside Windows and Linux before sending it.
- D. Nowhere: a LOAD above 1 is normal for any busy device and needs no action.
- E. Compare the queue depth of 32 with the HBA and the array's per-LUN guidance.

## Likely wrong answer
B: blaming the array.

## Expected key points
- Answer: A, E.
- A: %USD = ACTV / DQLEN = 100% means the device queue is full. LOAD = (ACTV + QUED) / DQLEN near 3: about twice as many commands wait in the kernel as the device accepts. KAVG (and QAVG inside it) carries the added time: GAVG ≈ 3 ms = KAVG 2 ms + DAVG 1 ms.
- E: the device queue depth is the limit here, and queue depths must match along the stack (HBA, device, array). Spreading the busy disks over more LUNs also gives more device queues.
- B is wrong: DAVG stays near 1 ms through the window. The array serves each command as fast as before; the commands wait before they get there.
- C is wrong: esxtop does not see the Guest OS queues.
- D is wrong: LOAD above 1 means commands are queued in the kernel.
- The other LUN, naa.624a9370b2, has no queue at the same time: the host and its adapters are not the limit.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot removed; the batch output reduced to two devices, one-minute samples and the panel's field names; the Storage I/O Control option removed (deprecated in VCF 9.0). Counts only after author approval.

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
knowledge_main: vsphere/tools/esxtop/storage
attachments:
  - 0086/esx-07-esxtop-batch-disk-devices-1-hour.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, E]
misconception: [B]
misconception_type: [layer-confusion]
status: draft
```
