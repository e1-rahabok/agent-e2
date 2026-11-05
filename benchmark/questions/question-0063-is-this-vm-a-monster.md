# Is this VM a monster?

## Prompt
- An ESXi host has 64 cores, 128 threads, 768 GB of DRAM and a 768 GB NVMe memory tier.
- A new VM is planned with 40 vCPUs and 300 GB of memory.
- The monster VM defaults of the vCommunity Cluster Risk metric apply.

Which statements are correct? Choose all that apply.

- A. The VM is a CPU monster: 40 vCPUs is more than 50% of the 64 physical cores.
- B. The VM is not a CPU monster: 40 vCPUs is less than 50% of the 128 threads.
- C. The VM is a memory monster: the threshold is the smaller of 40% of DRAM (about 307 GB) and 256 GB, so 256 GB.
- D. The VM is not a memory monster: the threshold counts DRAM plus NVMe, 40% of 1,536 GB.

## Likely wrong answer
B: counting threads instead of cores.

## Expected key points
- Answer: A, C.
- CPU: a monster has more than 50% of the host physical cores, not threads: above 32 vCPUs here.
- Memory: more than 40% of DRAM or 256 GB, whichever is smaller; NVMe does not count. Here 256 GB.
- Monster VMs raise contention risk even when utilization, reservation and allocation are low.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0063
title: "Is this VM a monster?"
product: [vsphere, vcf-operations]
technology: [system, cpu, memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/object-types/cluster/metrics/cluster-risk
  - vsphere/object-types/cluster/concepts/cluster-operations
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: draft
```
