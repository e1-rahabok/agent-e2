# VM footprint for a migration to slower CPUs

## Prompt
- 20 VMs move from cluster A (nominal clock 2.5 GHz) to cluster B (nominal clock 2.0 GHz).
- Both clusters have the same CPU generation, the same power policy and a similar Hyper-Threading load.
- [The attached export](0083/vm-cpu-peak-sample-20-vms.csv) holds, per VM, the busiest 20-second sample of its peak hour in cluster A. The CPU states are in ms, summed over the VM's vCPU instances; System is the VM-level value.
- The migration lead plans each VM's vCPU count in cluster B from CPU Run: Run ÷ 20,000, rounded up. For db-01 that gives 5 vCPUs.

Which statements about the plan and the CPU footprint of db-01 are correct?

- A. The plan is too small for db-01: Run counts time, and the same work takes more time on a slower clock.
- B. Run is the time the vCPUs ran, so 100,000 ms is 5 vCPUs, and the clock speed does not matter.
- C. Used carries the work: it adjusts the run time for the clock speed and for Hyper-Threading.
- D. Used alone is the right input: 96,000 ms gives about 5 vCPUs.
- E. System must be added: it is VMkernel work for db-01 that the hosts of cluster B must also supply.
- F. The Used in the export already holds System, because it is summed over the vCPU instances.
- G. Ready and Co-stop must be added: run time db-01 demanded and did not get.
- H. The footprint in GHz is Used times the actual Turbo clock of cluster A, not its nominal clock.
- I. db-01's footprint in cluster A is about 13.75 GHz, or about 5.5 vCPUs at 2.5 GHz.
- J. db-01 needs at least 7 vCPUs in cluster B, before any headroom.
- K. Whether the Guest OS has enough vCPUs (its run queue) is a separate check from the footprint.

## Likely wrong answer
- B: "Run is the time the vCPUs ran, so 100,000 ms is 5 vCPUs; the clock speed does not matter."
- D: "Use Used only: 96,000 ms, about 5 vCPUs."

## Expected key points
- Answer: A, C, E, G, I, J, K.
- A true: Run counts time, not work. On a slower clock the same work takes more time.
- B false: Run does not see frequency or Hyper-Threading; 5 vCPUs at 2.0 GHz deliver less than 5 vCPUs at 2.5 GHz.
- C true: Used is converted to ms at the nominal clock and adjusted for the actual frequency and for Hyper-Threading, so it scales with work, not time.
- D false: Used alone leaves out System, Ready and Co-stop, and 96,000 ms is work at the 2.5 GHz clock of cluster A, not of cluster B.
- E true: System is charged at VM level; the target hosts run it for the VM.
- F false: Used per vCPU instance excludes System; only the VM-level Used holds it. Add System once to the sum of the instances.
- G true: leaving them out sizes the VM to what it got, not to what it demanded.
- H false: Used already holds the actual frequency; the GHz figure multiplies by the nominal (static) clock.
- I true: (96,000 + 8,000 + 2,000 + 4,000) ÷ (20,000 × 8) = 0.6875 of 8 vCPUs = 5.5 vCPUs; × 2.5 GHz = 13.75 GHz.
- J true: 13.75 ÷ 2.0 is about 6.9, rounded up to 7, not 5.
- K true: the footprint is the load on the infrastructure; the Guest OS run queue is checked apart.

## Notes
- Revised 2026-11-12: key built on public counters and their mechanism (Used is adjusted for frequency and Hyper-Threading; Ready and Co-stop are unmet demand; System is charged at VM level). The earlier version asked for a named formula; this one asks for the reasoning (benchmark/design.md, section 6.1, F3).
- Overlap and Other Wait are not in the export; with them, the footprint would add them too.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0083"
title: "VM footprint for a migration to slower CPUs"
product: [vsphere, vcf-operations]
technology: [system, cpu]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,E,G,I,J,K]
misconception: [B,D]
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
source_path: "Drafted by Claude 2026-11-05; revised 2026-11-12"
misconception_type: [frequency-and-hyper-threading, unit-and-normalization]
status: draft
```
