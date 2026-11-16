# Highest disk latency above every device

## Prompt
- ESXi 9.1 host esx-12 uses memory tiering with a local NVMe device as tier 1. Its VMs' disks sit on two Fibre Channel LUNs, LUN-01 and LUN-02.
- The team's host dashboard shows vCenter's Highest latency (`disk.maxTotalLatency`) for esx-12. Two Real-time captures of the host's Disk chart, each read live, 20-second samples:
- 02:00-02:30, night, little load:
  - Highest latency: spikes of 70 to 90 ms in a few samples.
  - NVMe tier device, same samples: Physical device read latency 68 to 88 ms, Read rate 0 KBps.
  - LUN-01 and LUN-02: Physical device latency below 1 ms, Kernel latency below 0.1 ms.
- 10:00-10:30, business hours:
  - Highest latency: 6 to 7 ms in most samples.
  - All three devices: Physical device latency below 1 ms.
  - LUN-02: Kernel command latency 5.5 to 6.2 ms.
- The storage team calls the 10:00 chart an array problem and wants the NVMe device replaced for the night spikes. The platform team calls the night spikes an artefact, as the device read 0 KBps.

Which statements are correct?

- A. Highest latency is the top kernel plus device latency among the disks, so it can exceed every device line.
- B. At 10:00, the 6 to 7 ms is mostly kernel latency on LUN-02: time spent in the host, not at the array.
- C. Highest latency is the device latency of the worst disk, so at 10:00 it contradicts the device lines and is faulty.
- D. With Highest latency at 6 to 7 ms at 10:00, the array is the place to look first.
- E. An NVMe device idling in a deep power state adds tens of milliseconds to the first IO after it wakes.
- F. A Read rate of 0 KBps on the tier device means no read was issued, so its 70 to 90 ms is a sampling artefact.
- G. A device latency of 70 to 90 ms on the tier device shows a failing SSD that should be replaced now.
- H. The VMs whose pages were read during the night spikes did not wait for them, as memory tiering is invisible to the guests.
- I. One 4 KB tier read in a 20-second sample averages 0.2 KBps, so a chart can show a working device at 0.

## Answers
A, B, E, I

## Explanation
- A is correct: Highest latency (disk.maxTotalLatency) is the highest total latency, kernel latency plus device latency, among the disks the host uses.
- B is correct: LUN-02's device latency is below 1 ms and its kernel latency is 5.5 to 6.2 ms, so its total of about 6 to 7 ms is mostly VMkernel time. Read the kernel and queue latency per device next.
- C is wrong: the misconception. The counter adds kernel latency, so it can be well above every device line and still be right.
- D is wrong: the wrong action. The device latency, the part at the array and the fabric, is below 1 ms on all devices.
- E is correct: an idle NVMe controller drops into deep power states, and waking it adds about 50 to 100 ms to the first IO.
- F is wrong: the misconception. Tiering moves pages in 4 KB; a few reads in a 20-second sample round to 0, and the IO is not 0.
- G is wrong: the latency at near-zero activity is the wake-up from a power state, not a device fault.
- H is wrong: a vCPU that touches a page on the NVMe tier waits for the fetch, so the reads that woke the device waited that long. How much the VMs lost depends on how many reads hit it.
- I is correct: 4 KB / 20 s = 0.2 KBps, which rounds to 0 on a chart in KBps.
- Misconception: "Highest latency is the worst disk's latency, so with every device under 1 ms the chart is wrong" (C), or the storage team's "6 to 7 ms means the array" (D). For the night: "0 KBps, no IO, so the latency is noise" (F), or "nothing in the guest waits on it" (H).

## Notes
- Per-device latency history needs statistics level 3; the captures are Real-time, so the default level does not matter.
- E is worded as tens of milliseconds because the 50-100 ms wake-up is a knowledge-base value with an open review note (host/disk: NVMe power states, against the NVMe specification or the device vendor's documentation).

## Metadata
```yaml
id: "0462"
title: "Highest disk latency above every device"
product: [vsphere]
technology: [storage, memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/host/disk
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/technology/memory/concepts/memory-tiering
knowledge_main: vsphere/technology/storage/metrics/host/disk
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/storage/metrics/host/disk"
misconception: [C, D, F, H]
misconception_type: [unit-and-normalization]
status: draft
```
