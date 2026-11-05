# Reading an Intel Xeon specification: base, all-core Turbo, TDP

## Prompt
- Review the attached CPU specification, taken unchanged from the Intel website: Intel Xeon 6 6520P (Granite Rapids).
- 24 cores, 48 threads, Max Turbo Frequency 4 GHz, All Core Turbo Frequency 3.4 GHz, Processor Base Frequency 2.4 GHz, cache 144 MB, TDP 210 W.

- Be aware of the architectural difference between AMD EPYC and Intel Xeon.

Choose all the correct statements about the Xeon 6520P:

- A. The nominal clock speed is 2.4 GHz. However, the CPU can run all cores simultaneously at 3.4 GHz.
- B. TDP stands for Total Drawn Power, so the maximum power consumption is 210 W.
- C. The Max Turbo Frequency can only be reached with the High Performance setting. Balanced will not boost to this level.
- D. With BIOS power management set to OS Controlled and ESXi power management set to Balanced, you sacrifice performance to save energy. This applies to all types of workload.
- E. The 3 speeds (2.4, 3.4, 4.0 GHz) require different power: 4 GHz needs more than 210 W, 2.4 GHz less than 210 W.

## Attachments
![Intel website specification of the Xeon 6 6520P: cores, threads, base, All Core Turbo and Max Turbo frequency, cache, TDP](vsphere-cpu-007/intel-xeon-6520p-specification.png)

## Likely wrong answer
B (TDP read as maximum power draw), C or D (Balanced assumed to cap performance).

## Expected key points
- Answer: A only.
- B is wrong: TDP is Thermal Design Power: the average power the processor dissipates at Base Frequency with all cores active under an Intel-defined high-complexity workload.
- C is wrong: Balanced also boosts to Max Turbo, and is likely to, because power per core is more flexible.
- D is wrong: performance is not necessarily sacrificed. Most workloads suit Balanced.
- E is wrong: the relation is not that simple. At Single Core Turbo, total power can be below 210 W because other cores are idle.

## Notes
- Fact source for the TDP definition: Intel's published definition, as quoted in the author's key.

## Metadata
```yaml
id: vsphere-cpu-007
title: "Reading an Intel Xeon specification: base, all-core Turbo, TDP"
product: [vsphere]
technology: [cpu]
input: [screenshot]
task: explain-mechanism
knowledge:
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/concepts/power-states
  - vsphere/technology/cpu/configuration/host-power-management
  - vsphere/object-types/esxi/configuration/bios-settings
attachments: 
  - vsphere-cpu-007/intel-xeon-6520p-specification.png
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q4 ESXi CPU Frequency"
answer_type: deterministic
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [A]
trap: [B,C,D]
status: draft
```
