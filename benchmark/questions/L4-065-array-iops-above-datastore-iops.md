# Array IOPS twice the datastore IOPS at night

## Prompt
- Datastore DS-CRM02 is a VMFS datastore on one LUN (0x2A) of an FC array, mounted by 6 hosts.
- [The attached export](0188/ds-crm02-vs-lun-iops-1-day.csv) puts side by side, hour by hour for one day: the datastore IOPS summed over the 6 hosts (vCenter), the IOPS the array reports for LUN 0x2A, and the datastore read latency the VMs see.
- From 22:00 to 03:00, the CRM batch jobs on the VMs run slower than in the day.
- esxtop on one of the 6 hosts at 23:30, the device row of LUN 0x2A: DAVG/cmd 8.7 ms, KAVG/cmd 0.1 ms, GAVG/cmd 8.8 ms.
- The vSphere team says the VMs do less IO at night, so the array cannot be busy. The storage team says vCenter under-reports.

Why does the array report about twice the IOPS vCenter shows at night, and what does it mean for the slow batch jobs? Which statements are correct?

- A. Both tools are right: vCenter counts only the IO the 6 hosts send, while the array counts all the IO on the LUN.
- B. One of the two tools miscounts, since the IOPS of a datastore and of the one LUN behind it must always match.
- C. The extra IO comes from outside the 6 hosts: another initiator, such as a backup proxy, or array jobs such as replication.
- D. The VMs must be doing more IO at night than vCenter shows, since the array sees twice as much IO as vCenter.
- E. With one datastore on one LUN, array IOPS divided by datastore IOPS should be about 1, as it is in the day.
- F. A ratio of about 2 at night means the IO from sources other than the 6 hosts is about twice what the hosts send.
- G. The VMs do less IO at night than in the day, so the array cannot be what slows down the batch jobs.
- H. The VMs' IO waits behind the other IO at the array: their latency rises while their own IO falls.
- I. Set an IOPS limit on the CRM VMs' disks so that they leave room at night for the other IO on the LUN.
- J. A snapshot on one of the VMs adds IO that the array counts and vCenter does not, which explains the gap.
- K. The esxtop row at 23:30 places the wait in the VMkernel of the host, not in the array or fabric.
- L. The fix lies with the storage team: find what hits the LUN from 22:00, then move or throttle it.

## Answers
A, C, E, H, L

## Explanation
- A is correct: each tool is right from its own vantage point; vCenter sees only its hosts.
- B is wrong: the array counts every initiator and its own jobs; vCenter counts only the IO of its hosts.
- C is correct: a LUN IOPS / datastore IOPS ratio above 1 means the LUN serves IO that no host in vCenter sends: another initiator (a SAN-mode backup proxy, a host of another vCenter) or the array's own jobs (replication, array snapshots, rebuilds).
- D is wrong: the VMs' IO cannot reach the LUN without passing through the hosts that vCenter counts.
- E is correct: from 03:00 to 21:00 the two columns are within a few percent of each other.
- F is wrong: a ratio of 2 means the other IO about equals what the hosts send: from 22:00 to 02:00 the array reports about 3,900-5,100 IOPS against about 2,000-2,500 from the hosts, so about 1,900-2,500 IOPS come from elsewhere.
- G is wrong: the VMs' latency rises from about 1 ms to 7-9 ms exactly when the array serves the other IO; less IO from the VMs does not mean a quiet LUN.
- H is correct: the VMs are not the cause: at night their IO is about a third of the daytime level while their read latency rises from about 1 ms to 7-9 ms, the highest of the day.
- I is wrong: the CRM VMs are the victims: at night their IO is about a third of the daytime level. A limit holds their IO above it in the kernel queue of their hosts (QAVG), which adds to their latency and leaves the other IO on the LUN as it was.
- J is wrong: snapshot IO passes through the hosts and shows in the datastore counters; vCenter counts it.
- K is wrong: it is the reverse: DAVG 8.7 ms with KAVG 0.1 ms places the time beyond the HBA, in the fabric or the array; the commands do not wait in the host's kernel. GAVG 8.8 ms matches the latency the VMs see in the export.
- L is correct: the cause is outside vSphere: ask which initiators and jobs hit the LUN at 22:00, move or throttle them, or move the batch window; track the ratio over time.
- Misconception: B: "One of the two tools miscounts: the IOPS should match." - D: "The VMs must be doing more IO at night than vCenter shows." - G: "The VMs do less IO at night, so the array cannot be busy."

## Notes
- Synthetic, 2026-11-12: the backing device ratio. Counts only after author approval.
- Review 2026-11-14: options F (the ratio) and K (DAVG against KAVG) turned into near misses, so fewer options are correct; each still tests its old key point.
- Audit 2026-11-15: an esxtop row at 23:30 added, so K reads values instead of a reversed rule; weak I (Guest OS queues) replaced by an IOPS limit on the victim VMs; L reworded without the absolute; H shortened (length cue). Key unchanged.
- Re-review 2026-11-16: F reworded so it has one reading (other IO about twice the hosts' IO). Key unchanged.

## Metadata
```yaml
id: "0188"
title: "Array IOPS twice the datastore IOPS at night"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 400
answer_type: deterministic
misconception: [B,D,G]
input: [table]
object: [datastore, esxi]
tool: [vcenter, esxtop]
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
source_path: "Synthetic, 2026-11-12"
misconception_type: [provider-vs-consumer]
pair: "0408"
status: draft
```
