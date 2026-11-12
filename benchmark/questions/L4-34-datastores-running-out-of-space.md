# Which datastores run out of space first

## Prompt
- [The attached export](0080/datastore-space-30-datastores.csv) lists the 30 datastores of one site: type, capacity, used space, the provisioned size of the virtual disks (before the vSAN storage policy), snapshot space, the share of thin virtual disks, the number of VMs, and the vSAN storage policy.
- The storage team asks which datastores will run out of space first, and how far they can overcommit thin disks.

Which datastores are most at risk, and why? How do you set the overcommit ratio?

## Likely wrong answer
"DS-ARCH-01 is the only datastore at risk: it is 95% full. The others are below 80%."

## Expected key points
- Thin disks can grow to their provisioned size, so used % alone under-states the risk. Compare the unwritten thin space (provisioned − used) with free space (capacity − used).
- DS-APP-04, DS-APP-09 and DS-WEB-02 are the top risk: used below 70%, but provisioned 160-175% of capacity with mostly thin disks; their unwritten thin space is 2-3 times their free space. They can fill with no new VM added.
- DS-DB-03 and DS-DEV-11: snapshots are over a quarter of used space (1,720 GB and 980 GB), close to their free space. A delta grows with every write; remove the snapshots once the change is validated.
- VSAN-PROD-A is at 78% with RAID-1 (FTT=1): used includes the second copy. Its thin disks can still claim about (26,000 − 23,950) × 2 ≈ 4 TB, which fits its free space, but keep vSAN below about 80% to leave room to rebuild after a host failure.
- DS-ARCH-01 is 95% used but all thick: its disks cannot grow. Watch it for new snapshots and swap files; it is not the first to run out.
- Overcommit ratio = provisioned ÷ capacity, counting virtual disks only (not snapshots or swap). On vSAN, count the policy: RAID-1 doubles the provisioned size, so 26,000 GB claims 52,000 GB (85% of VSAN-PROD-A) and the ratio that fits is half the VMFS one. The ratio that fits depends on how fast the thin disks fill against the lead time to expand or reclaim.

## Notes
- Previous id: question-0080 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: 200 datastores reduced to 30 so the export is read in the prompt; vSAN provisioned shown before the policy, so the three thin VMFS and NFS datastores stay the most overcommitted. Counts only after author approval.

## Metadata
```yaml
id: "0080"
title: "Which datastores run out of space first"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: judged
input: [table]
object: [datastore]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/datastore-space-headroom
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-space-provisioned
  - vsphere/technology/storage/concepts/snapshot-impact
  - sp5-framework/capacity/overcommit
knowledge_main: vsphere/technology/storage/datastore-space-headroom
attachments:
  - 0080/datastore-space-30-datastores.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
misconception_type: []
status: draft
```
