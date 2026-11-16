# A slow disk scan with a fast array

## Prompt
- Users of the reporting VM rpt-scan-03 say a scan of its data disk takes hours. The data disk is Hard disk 2 (scsi0:1), on LUN naa.624a93701c2d3e4f5a6b7c8d00011a07; no other VM uses that LUN.
- The VM owner says vCenter proves the storage is slow. The storage team says the array answers in under a millisecond.
- You export [the VM's Virtual disk chart](0425/vcenter-vm-virtual-disk-realtime.csv), Real-time, 10 minutes during the scan. The chart legend (not in the export) gives the units: rates in KBps, latencies in ms.
- On the VM's host, esx-c2-07, esxtop shows the disk device panel (u) during the same minutes:

```text
2:41:07am up 41 days 03:12, 1214 worlds, 18 VMs, 64 vCPUs; CPU load average: 0.20, 0.19, 0.20
DEVICE                                PATH/WORLD/PARTITION DQLEN WQLEN ACTV QUED %USD  LOAD   CMDS/s  READS/s WRITES/s MBREAD/s MBWRTN/s DAVG/cmd KAVG/cmd GAVG/cmd QAVG/cmd 
naa.624a93701c2d3e4f5a6b7c8d00011a02           -              64     -    1    0    1  0.02   378.66   231.94   146.71     1.81     1.15     0.72     0.02     0.74     0.01 
naa.624a93701c2d3e4f5a6b7c8d00011a07           -              64     -    0   16    0  0.25   249.59   249.50     0.09    31.19     0.00     0.80    63.94    64.74    63.53 
mpx.vmhba32:C0:T0:L0                           -               1     -    0    0    0  0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00     0.00 
```

- The VM's virtual disks, from PowerCLI:

```text
PS C:\> (Get-VM rpt-scan-03).ExtensionData.Config.Hardware.Device |
>> Where-Object { $_ -is [VMware.Vim.VirtualDisk] } |
>> Select-Object @{N='Disk';E={$_.DeviceInfo.Label}}, UnitNumber, @{N='LimitIOPS';E={$_.StorageIOAllocation.Limit}}

Disk        UnitNumber LimitIOPS
----        ---------- ---------
Hard disk 1          0        -1
Hard disk 2          1      1000
```

Which statements are correct?

- A. The reads are about 128 KB each: read rate divided by read requests per second.
- B. With 128 KB reads, the 1,000 IOPS limit caps the disk at about 250 reads per second.
- C. The disk runs at about a quarter of its limit, so the limit is not what holds it back.
- D. The time is spent in the ESXi kernel queue: KAVG and QAVG are high while DAVG stays below 1 ms.
- E. The array is slow: the virtual disk latency comes from the device.
- F. Ask the storage team to move the LUN to faster media.
- G. A high QAVG on a LUN always means an IOPS limit on one of its virtual disks.
- H. Setting Limit - IOPS back to Unlimited, its default, takes away the wait in the kernel queue.
- I. In the esxtop disk device panel, DAVG/cmd is higher than KAVG/cmd.

## Likely wrong answer
E or F: the latency is high, so the array is slow. Or C: 250 reads per second is far below the 1,000 limit, so the limit cannot be the cause.

## Expected key points
- Answer: A, B, D, H.
- A true: reading. `Read rate for scsi0:1` (KBps) divided by `Average read requests per second for scsi0:1` is 127-129 KB in every row (about 32,000 KBps at about 250 reads per second).
- B true: mClock counts an IO above 32 KB as several: a 128 KB read counts as 4, so 1,000 / 4 = 250 reads per second; `Average read requests per second for scsi0:1` stays flat at 230-260 in every row.
- C false: the misconception. The limit counts 128 KB reads four times; the disk sits at its limit.
- D true: IO above the limit waits in the kernel queue: high QAVG, inside KAVG and GAVG, with normal DAVG (Broadcom KB 426790). In the esxtop row of the LUN, DAVG/cmd is below 1 ms, KAVG/cmd at least 10 times DAVG/cmd, QAVG/cmd within 20% of KAVG/cmd, and GAVG/cmd = DAVG/cmd + KAVG/cmd, close to `Read latency for scsi0:1`.
- E false: DAVG below 1 ms shows the device answers fast; the wait is before the IO reaches it.
- F false: the wrong action. Faster media do not change a wait set by the VM's own limit.
- G false: the over-correction. High QAVG means IO waits in a VMkernel queue; the device queue depth (DQLEN) and Disk.SchedNumReqOutstanding on a device that several virtual disks share are other causes. Here the PowerCLI output shows the limit on Hard disk 2.
- H true: the default is no limit (-1 in the PowerCLI output); without it the reads are no longer held in the kernel queue. The device queue does not take over: the LUN row shows ACTV at 0-1 against a DQLEN of 64, and no other VM uses the LUN.
- I false: reading. DAVG/cmd is below 1 ms and KAVG/cmd at least 10 times higher.

## Reasoning path
1. Read rate / read requests per second: the IO size.
2. Limit / (IO size / 32 KB): the cap in reads per second; compare with the flat read requests per second.
3. esxtop: where the time is spent (KAVG and QAVG against DAVG; ACTV against DQLEN).

## Notes
- Practical half of pair D6 with 0424 (theory; design.md, section 3.9).
- No option rests on the Paravirtual SCSI queue depth or Disk.SchedNumReqOutstanding.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D6 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: H names the setting as the product shows it; I (a false screen reading) added. Key unchanged: A, B, D, H.
- 2026-11-15: screenshots replaced by a generated export and tool text (project/practical-questions-as-exports-2026-11-15.md). The PowerCLI block is literal; the esxtop block is generated.

## Metadata
```yaml
id: "0425"
title: "A slow disk scan with a fast array"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, esxi]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/tools/esxtop/storage
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/iops
attachments:
  - 0425/vcenter-vm-virtual-disk-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D6"
answer: [A, B, D, H]
misconception: [C, E]
misconception_type: [consumption-as-contention, unit-and-normalization]
pair: "0424"
status: draft
```
