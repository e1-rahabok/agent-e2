# Array IOPS twice the datastore IOPS at night

## Prompt
- Datastore DS-CRM02 is a VMFS datastore on one LUN (0x2A) of an FC array, mounted by 6 hosts.
- [The attached export](0188/ds-crm02-vs-lun-iops-1-day.csv) puts side by side, hour by hour for one day: the datastore IOPS summed over the 6 hosts (vCenter), the IOPS the array reports for LUN 0x2A, and the datastore read latency the VMs see.
- From 22:00 to 03:00, the CRM batch jobs on the VMs run slower than in the day.
- The vSphere team says the VMs do less IO at night, so the array cannot be busy. The storage team says vCenter under-reports.

Why does the array report about twice the IOPS vCenter shows at night, and what does it mean for the slow batch jobs? Which statements are correct?

- A. Both tools are right: vCenter counts only the IO the 6 hosts send, while the array counts all the IO on the LUN.
- B. One of the two tools miscounts, since the IOPS of a datastore and of the one LUN behind it must always match.
- C. The extra IO comes from outside the 6 hosts: another initiator, such as a backup proxy, or array jobs such as replication.
- D. The VMs must be doing more IO at night than vCenter shows, since the array sees twice as much IO as vCenter.
- E. With one datastore on one LUN, array IOPS divided by datastore IOPS should be about 1, as it is in the day.
- F. A ratio of about 2 at night means the LUN serves about twice as much other IO as the 6 hosts send.
- G. The VMs do less IO at night than in the day, so the array cannot be what slows down the batch jobs.
- H. The VMs' IO waits behind the other IO at the array: their read latency rises from about 1 ms to 7-9 ms while their own IO falls.
- I. The gap is IO that waits in the Guest OS queues, which vCenter does not count and the array does.
- J. A snapshot on one of the VMs adds IO that the array counts and vCenter does not, which explains the gap.
- K. Kernel latency (KAVG) rising at night while device latency (DAVG) stays low would place the wait in the array or fabric.
- L. No vSphere setting fixes it: find with the storage team what hits the LUN from 22:00, then move or throttle it.

## Likely wrong answer
- B: "One of the two tools miscounts: the IOPS should match."
- D: "The VMs must be doing more IO at night than vCenter shows."
- G: "The VMs do less IO at night, so the array cannot be busy."

## Expected key points
- Answer: A, C, E, H, L.
- A true: each tool is right from its own vantage point; vCenter sees only its hosts.
- B false: the array counts every initiator and its own jobs; vCenter counts only the IO of its hosts.
- C true: a LUN IOPS / datastore IOPS ratio above 1 means the LUN serves IO that no host in vCenter sends: another initiator (a SAN-mode backup proxy, a host of another vCenter) or the array's own jobs (replication, array snapshots, rebuilds).
- D false: the VMs' IO cannot reach the LUN without passing through the hosts that vCenter counts.
- E true: from 03:00 to 21:00 the two columns are within a few percent of each other.
- F false: a ratio of 2 means the other IO about equals what the hosts send: from 22:00 to 02:00 the array reports about 3,900-5,100 IOPS against about 2,000-2,500 from the hosts, so about 1,900-2,500 IOPS come from elsewhere.
- G false: the VMs' latency rises from about 1 ms to 7-9 ms exactly when the array serves the other IO; less IO from the VMs does not mean a quiet LUN.
- H true: the VMs are not the cause: at night their IO is about a third of the daytime level while their latency is the highest of the day.
- I false: IO queued inside the Guest OS has not reached the hypervisor, so it cannot reach the array either.
- J false: snapshot IO passes through the hosts and shows in the datastore counters; vCenter counts it.
- K false: it is the reverse: high device latency (DAVG) with low kernel latency (KAVG) places the time in the array or the fabric; a high KAVG places it in the kernel of the host.
- L true: the cause is outside vSphere: ask which initiators and jobs hit the LUN at 22:00, move or throttle them, or move the batch window; track the ratio over time.

## Notes
- Drafted by Claude 2026-11-12: the backing device ratio. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Review 2026-11-14: options F (the ratio) and K (DAVG against KAVG) turned into near misses, so fewer options are correct; each still tests its old key point.

## Metadata
```yaml
id: "0188"
title: "Array IOPS twice the datastore IOPS at night"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 400
answer_type: deterministic
answer: [A,C,E,H,L]
misconception: [B,D,G]
input: [table]
object: [datastore, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/concepts/storage-layers
  - vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/architecture/provider-consumer
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
knowledge_main: vsphere/technology/storage/concepts/storage-layers
attachments:
  - 0188/ds-crm02-vs-lun-iops-1-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [provider-vs-consumer]
status: draft
```
