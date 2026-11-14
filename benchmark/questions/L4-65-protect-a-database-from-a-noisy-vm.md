# Protect a database from a noisy VM on a shared datastore

## Prompt
- A vSphere 9.1 cluster of 8 hosts shares VMFS datastore DS-SHR01 on an FC array.
- Every night from 01:00 to 03:00, reporting VM rpt-07 runs large sequential reads on DS-SHR01.
- In that window, database VM db-11, on another host and the same datastore, sees its read latency rise from 1 ms to 25 ms. Outside the window db-11 is fine.
- The team proposes to turn on Storage I/O Control on DS-SHR01 and give db-11 High disk shares, so that the database wins when the datastore is congested.

Will that work in vSphere 9.1, and what do you advise instead? Which statements are correct?

- A. Storage I/O Control throttles rpt-07 once the datastore latency crosses its threshold, so db-11 with High shares wins.
- B. High disk shares on db-11 protect it even without Storage I/O Control, through the IO scheduler of its own host.
- C. The plan will not protect db-11: from VCF 9.0, Storage I/O Control ignores shares and reservations and honours only limits.
- D. An IOPS reservation on the virtual disks of db-11 guarantees it the IOPS it needs.
- E. An IOPS limit on the virtual disks of rpt-07, sized so its job still ends in the window, protects db-11.
- F. A throughput limit in MB/s on the disks of rpt-07 is the right control for its large sequential reads.
- G. An IOPS limit cannot restrain large sequential reads, because each large read counts as a single IO.
- H. Moving rpt-07 or db-11 to another datastore or LUN, or using the QoS of the array, also separates the two.
- I. The latency rises on db-11 alone, so the cause is on the host of db-11, and a setting on that host fixes it.
- J. High device latency (DAVG) with low kernel latency (KAVG) on the host of db-11 shows that it waits in the array or fabric, which it shares with the host of rpt-07.

## Likely wrong answer
- A: "Yes. Enable Storage I/O Control and set db-11 to High shares: SIOC throttles rpt-07 when the datastore latency crosses its threshold."
- B: "High shares give db-11 priority on the datastore."

## Expected key points
- Answer: C, E, H, J.
- A false: from VCF 9.0 Storage I/O Control honours only limits; shares no longer decide which VM gets the IO (Broadcom KB 385396).
- B false: without a datastore-wide control, the scheduler of one host sees only its own IO; rpt-07 runs on another host and its reads load the array, not db-11's host queue.
- C true: Storage I/O Control is deprecated; its storage policies honour only limits from VCF 9.0. High shares will not protect db-11.
- D false: there is no reservation for disk IOPS or throughput, and Storage I/O Control ignores reservations from VCF 9.0.
- E true: limits are still honoured; put the control on the noisy VM. IO above the limit waits in the kernel queue of rpt-07's host.
- F false: a disk throughput limit does not exist; the limit is in IOPS.
- G false: the ESXi IO scheduler (mClock) counts an IO above 32 KB as several, so an IOPS limit also caps the throughput of large reads.
- H true: separation removes the shared queue; the array's QoS works across all its initiators.
- I false: the latency rises only in rpt-07's window, and rpt-07 runs on another host: the contention is in what the two hosts share.
- J true: confirm where db-11 waits before changing anything; no setting on db-11's host alone fixes a wait in the array or fabric.

## Notes
- Drafted by Claude 2026-11-12. Counts only after author approval.
- Vendor documents: Broadcom KB 385396, "Deprecation of default Storage Policy Components for SIOC Storage Policy" (https://knowledge.broadcom.com/external/article/385396): from VCF 9.0 the SIOC policy supports only limits and the backend ignores shares and reservations. Deprecation notice with vSphere 8.0 U3 (https://www.yellow-bricks.com/2024/11/25/storage-io-control-aka-sioc-deprecation-notice-with-8-0-u3).
- The key does not depend on whether SIOC can still be enabled on a datastore in 9.x (only a secondary source says it cannot). An answer that says so is a correct alternative, not a requirement.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). No option depends on whether Storage I/O Control can still be enabled on a datastore in 9.x.

## Metadata
```yaml
id: "0183"
title: "Protect a database from a noisy VM on a shared datastore"
product: [vsphere]
technology: [storage]
task: judge-setting
level: 400
answer_type: deterministic
answer: [C,E,H,J]
misconception: [A,B]
input: [text]
object: [vm, datastore]
tool: [none]
knowledge:
  - vsphere/technology/storage/metrics/datastore/storage-io-control
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/storage/metrics/datastore/storage-io-control
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: []
status: draft
```
