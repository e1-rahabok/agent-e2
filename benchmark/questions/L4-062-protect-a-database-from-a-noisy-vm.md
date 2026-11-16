# Protect a database from a noisy VM on a shared datastore

## Prompt
- A vSphere 9.1 cluster of 8 hosts shares VMFS datastore DS-SHR01 on an FC array.
- Every night from 01:00 to 03:00, reporting VM rpt-07 runs large sequential reads on DS-SHR01.
- In that window, database VM db-11, on another host and the same datastore, sees its read latency rise from 1 ms to 25 ms. Outside the window db-11 is fine.
- In the window, esxtop on rpt-07's host shows its virtual disk at about 1,600 reads per second of 512 KB (about 800 MB/s). On db-11's host, the device row of the LUN behind DS-SHR01 shows DAVG/cmd 24 ms and KAVG/cmd 0.1 ms.
- The team proposes to turn on Storage I/O Control on DS-SHR01 and give db-11 High disk shares, so that the database wins when the datastore is congested.

Will that work in vSphere 9.1, and what do you advise instead? Which statements are correct?

- A. Storage I/O Control throttles rpt-07 once the datastore latency crosses its threshold, so db-11 with High shares wins.
- B. High disk shares on db-11 protect it even without Storage I/O Control, through the IO scheduler of its own host.
- C. The plan will not protect db-11: from VCF 9.0, Storage I/O Control ignores shares and reservations and honours only limits.
- D. An IOPS reservation on the virtual disks of db-11 guarantees it the IOPS it needs in the window.
- E. An IOPS limit on the virtual disks of rpt-07, sized so its job still ends in the window, protects db-11.
- F. A throughput limit in MB/s on the disks of rpt-07 is the right control for its large sequential reads.
- G. An IOPS limit cannot restrain large sequential reads, because each large read counts as a single IO.
- H. Moving rpt-07 or db-11 to storage the other does not share also protects db-11.
- I. The latency rises on db-11 alone, so the cause is on the host of db-11, and a setting on that host fixes it.
- J. The esxtop row on db-11's host shows it waits in the array or fabric, which it shares with rpt-07's host.
- K. Throttling the IO of rpt-07 with the QoS of the array is another control that protects db-11.
- L. A 1,000 IOPS limit loads the array the same on rpt-07 as on a VM doing 4 KB random reads.

## Answers
C, E, H, J, K

## Explanation
- A is wrong: from VCF 9.0 Storage I/O Control honours only limits; shares no longer decide which VM gets the IO (Broadcom KB 385396).
- B is wrong: from VCF 9.0 disk shares are ignored altogether; only the IOPS limit is honoured. Even before, the scheduler of one host saw only its own IO, and rpt-07 runs on another host: its reads load the array, not db-11's host queue.
- C is correct: Storage I/O Control is deprecated; its storage policies honour only limits from VCF 9.0. High shares will not protect db-11.
- D is wrong: a virtual disk has an IOPS limit and shares, and no reservation for IOPS or throughput; Storage I/O Control also ignores reservations from VCF 9.0.
- E is correct: limits are still honoured; put the control on the noisy VM. IO above the limit waits in the kernel queue of rpt-07's host.
- F is wrong: a disk throughput limit does not exist; the limit is in IOPS.
- G is wrong: the ESXi IO scheduler (mClock) counts an IO above 32 KB as several, so an IOPS limit also caps the throughput of large reads: a 512 KB read counts as 16.
- H is correct: separation removes the shared queue in the array and the fabric where db-11 waits.
- I is wrong: the latency rises only in rpt-07's window, and rpt-07 runs on another host: the contention is in what the two hosts share.
- J is correct: DAVG 24 ms with KAVG 0.1 ms places db-11's wait beyond the HBA, in the fabric or the array; no setting on db-11's host alone fixes it.
- K is correct: outside vSphere the array is a point of control of its own; its QoS acts on the IO of every initiator, so it can hold back rpt-07's reads.
- L is wrong: the cost of an IO varies with block size, read/write mix and pattern; rpt-07's 512 KB sequential reads cost the array far more per IO than 4 KB random reads, and mClock counts each of them as 16 against the limit.
- Misconception: A: "Yes. Enable Storage I/O Control and set db-11 to High shares: SIOC throttles rpt-07 when the datastore latency crosses its threshold." - B: "High shares give db-11 priority on the datastore." - L: "1,000 IOPS is 1,000 IOPS, whatever VM it is set on."

## Notes
- Synthetic, 2026-11-12. Counts only after author approval.
- Vendor documents: Broadcom KB 385396, "Deprecation of default Storage Policy Components for SIOC Storage Policy" (https://knowledge.broadcom.com/external/article/385396): from VCF 9.0 the SIOC policy supports only limits and the backend ignores shares and reservations. Deprecation notice with vSphere 8.0 U3 (https://www.yellow-bricks.com/2024/11/25/storage-io-control-aka-sioc-deprecation-notice-with-8-0-u3).
- No option depends on whether SIOC can still be enabled on a datastore in 9.x (only a secondary source says it cannot).
- Review 2026-11-14: option H says storage the two do not share, not "another datastore or LUN": a second LUN on the same array can still share the array or fabric where db-11 waits (option J).
- Audit 2026-11-15: esxtop values added to the stem (rpt-07's 512 KB reads; DAVG and KAVG on db-11's host), so J reads values; H split into H (separation) and K (array QoS), one fact each; L added, the noisy-neighbour misconception that an IOPS limit costs the same on every VM; key point B carries the VCF 9.0 rule. An option on the mClock arithmetic (a 3,200 IOPS limit caps 512 KB reads at about 200 per second) was not added: the mClock fact is already tested by the pair 0424/0425. Key changed from C, E, H, J to C, E, H, J, K.

## Metadata
```yaml
id: "0183"
title: "Protect a database from a noisy VM on a shared datastore"
product: [vsphere]
technology: [storage]
task: judge-setting
level: 400
answer_type: deterministic
misconception: [A,B,L]
input: [text]
object: [vm, datastore]
tool: [esxtop]
knowledge:
  - vsphere/technology/storage/metrics/datastore/storage-io-control
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/architecture/resource-controls
  - sp5-framework/performance/noisy-neighbour
knowledge_main: vsphere/technology/storage/metrics/datastore/storage-io-control
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: []
status: draft
```
