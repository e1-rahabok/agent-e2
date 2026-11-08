# Device queue full in esxtop batch data

## Prompt
The attached table is one hour of esxtop batch output (esxtop -b, 10-second samples) of one ESXi host. The screenshot is the esxtop disk device panel (u) of the same host during the busiest minute.

- One device shows LOAD above 1, QUED above 0 and %USD at 100.
- On that device, KAVG/cmd is above 0.5 ms and DAVG/cmd stays low.

Where is the latency added, and what do you check?

- A. In the kernel: the device queue is full, so commands wait in the kernel. Check the queue depths along the stack, and whether Storage I/O Control lowered the device queue depth.
- B. In the array: DAVG is the array latency.
- C. In the Guest OS queue.
- D. Nowhere: LOAD above 1 is normal for a busy device.

## Input to supply
- Table: esxtop batch mode (esxtop -b -d 10 -n 360) of one ESXi 9.1 host, CSV, 360 rows. Keep the disk device columns; other columns may stay.
- Screenshot: esxtop disk device panel (press u) of the same host in the busiest minute, with QSTATS fields (DQLEN, ACTV, QUED, %USD, LOAD) and latency fields (DAVG, KAVG, GAVG, QAVG).
- Condition for the key: one device with LOAD above 1, QUED above 0, %USD 100, KAVG/cmd above 0.5 ms, DAVG/cmd low (well within 5 ms).
- How to produce it: lower the device queue depth on a lab LUN and run a high-outstanding-IO load.
- Mask device names if they reveal the customer.
- Save as `benchmark/questions/86/esxtop-batch-one-hour.csv` and `benchmark/questions/86/esxtop-disk-device-queue.png`.

## Likely wrong answer
B: blaming the array when DAVG is low.

## Expected key points
- Answer: A.
- %USD = ACTV / queue length: 100% means the queue is full, so outstanding IO and latency rise. LOAD above 1 with QUED above 0: commands are queued in the kernel.
- KAVG above 0.5 ms points to kernel queues; check QAVG and the queue depths at each level of the stack.
- When SIOC is active, it lowers the device queue depth of each host by shares: the host Maximum Queue Depth then changes over time.
- B is wrong: DAVG is low. C is wrong: esxtop does not see the Guest OS queue.

## Notes
- Previous id: question-0086 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0086"
title: "Device queue full in esxtop batch data"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table, screenshot]
knowledge:
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/technology/storage/metrics/datastore/storage-io-control
attachments:
  - 0086/esxtop-batch-one-hour.csv
  - 0086/esxtop-disk-device-queue.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: awaiting-input
```
