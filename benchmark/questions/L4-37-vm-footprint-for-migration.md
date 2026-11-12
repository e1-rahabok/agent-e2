# VM footprint for a migration to slower CPUs

## Prompt
- 20 VMs move from cluster A (nominal clock 2.5 GHz) to cluster B (nominal clock 2.0 GHz).
- Both clusters have the same CPU generation, the same power policy and a similar Hyper-Threading load.
- [The attached export](0083/vm-cpu-peak-sample-20-vms.csv) holds, per VM, the busiest 20-second sample of its peak hour in cluster A. The CPU states are in ms, summed over the VM's vCPU instances; System is the VM-level value.
- The migration lead plans each VM's vCPU count in cluster B from CPU Run: Run ÷ 20,000, rounded up. For db-01 that gives 5 vCPUs.

Is the plan right for db-01? Work out db-01's CPU footprint in cluster A, in vCPUs and in GHz, and the vCPUs it needs in cluster B. Say which counters you use and why.

## Likely wrong answer
"Run is the time the vCPUs ran, so 100,000 ms is 5 vCPUs; the clock speed does not matter." Or "Use Used only: 96,000 ms, about 5 vCPUs."

## Expected key points
- No: the plan is too small. Run counts time, not work. On a slower clock the same work takes more time.
- Use Used: it is the run time adjusted for the clock speed and for Hyper-Threading, so it scales with work, not time.
- Add System: VMkernel work done for the VM, which the per-vCPU Used does not hold.
- Add Ready and Co-stop: time db-01 demanded and did not get. Leaving them out sizes the VM to what it got, not to what it demanded.
- db-01 in cluster A: about 13-14 GHz (13.75 GHz with Used + Ready + Co-stop + System: (96,000 + 8,000 + 2,000 + 4,000) ÷ (20,000 × 8) = 0.6875 of 8 vCPUs × 2.5 GHz), so at least 7 vCPUs in cluster B (13.75 ÷ 2.0 ≈ 6.9) before any headroom, not 5.
- The footprint is the load on the infrastructure; whether the Guest OS has enough (its run queue) is a separate check.

## Notes
- Revised 2026-11-12 (question set 1.0): key built on public counters and their mechanism (Used is adjusted for frequency and Hyper-Threading; Ready and Co-stop are unmet demand; System is charged at VM level). The earlier version asked for a named formula; this one asks for the reasoning (benchmark/design.md, section 6.1, F3).
- Overlap and Other Wait are not in the export; with them, the footprint would add them too.

## Metadata
```yaml
id: "0083"
title: "VM footprint for a migration to slower CPUs"
product: [vsphere, vcf-operations]
technology: [system, cpu]
task: decide-capacity
level: 400
answer_type: judged
input: [table]
object: [vm, cluster]
tool: [vcenter]
knowledge:
  - sp5-framework/capacity/vm-footprint-sizing
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: sp5-framework/capacity/vm-footprint-sizing
attachments:
  - 0083/vm-cpu-peak-sample-20-vms.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation; revised 2026-11-12 (question set 1.0)"
misconception_type: [frequency-and-hyper-threading, unit-and-normalization]
status: draft
```
