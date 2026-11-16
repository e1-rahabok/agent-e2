# VM CPU alert: the usage floor in GHz

## Prompt
- VCF Operations. The VM CPU contention alert (one definition for every VM) has three conditions, all required in the same cycle:
  - Red: highest 20-second vCPU Ready above 32%, CPU Ready (%) of the cycle above 8%, and CPU Usage above 1 GHz.
  - Orange: highest 20-second vCPU Ready above 16%, CPU Ready (%) above 4%, and CPU Usage above 1 GHz.
- The infrastructure team receives red and orange. The application team receives red only.
- A colleague proposes to change the 1 GHz usage floor to a percentage so it "scales with VM size": CPU Usage above 5% of the VM's capacity.
- The hosts run at 2.4 GHz per core. In the current cycle, four VMs show:

| VM | vCPUs | CPU Usage | Highest 20-second Ready | CPU Ready (cycle) |
|---|---|---|---|---|
| VM-1 | 64 | 3% | 41% | 9% |
| VM-2 | 2 | 40% | 20% | 5% |
| VM-3 | 8 | 4% | 50% | 12% |
| VM-4 | 4 | 12% | 45% | 3% |

The colleague's change takes effect. Which statements about the notifications of these four VMs, compared with today, are correct?

- A. VM-1 loses its red alert, so its application team is no longer told.
- B. VM-4 gains an orange alert under the 5% floor, since it uses 12% of its capacity.
- C. A 5% floor selects the same VMs as a 1 GHz floor, since both measure the same activity.
- D. Under today's 1 GHz floor VM-3 should already alert, since 4% of its 8 vCPUs is above 1 GHz.
- E. The 5% floor demotes VM-1 from red to orange, so only the infrastructure team is told.
- F. VM-2 keeps its orange alert under the 5% floor, as it has it under the 1 GHz floor today.
- G. VM-3 alerts under neither floor, though its Ready values are the highest of the four.

## Answers
A, F, G

## Explanation
- A is correct: today VM-1 uses 3% of 64 x 2.4 = 153.6 GHz, about 4.6 GHz, over 1 GHz, with Ready 41% (>32%) and 9% (>8%): red, sent to both teams. At 3% it falls under a 5% floor and loses the alert; the application team receives red only, so it is no longer told. A small percentage of a large VM is a large load.
- B is wrong: VM-4 (12%, 1.15 GHz) passes either floor, but its CPU Ready (cycle) of 3% is under the orange 4%; all three conditions must hold in the same cycle.
- C is wrong: the floors select different VMs. VM-1 passes 1 GHz (4.6 GHz) and fails 5% (3%); the load that matters is absolute.
- D is wrong: 4% of 8 x 2.4 = 19.2 GHz is about 0.77 GHz, under 1 GHz.
- E is wrong: the floor is a condition of both the red and the orange alert, so failing it removes the alert; it does not move the VM to the other colour.
- F is correct: VM-2 uses 40% of 4.8 GHz, about 1.9 GHz, so it passes both floors; highest Ready 20% (>16, <32) and 5% (>4, <8) give orange under either floor.
- G is correct: VM-3 is at 4%, about 0.77 GHz: under 1 GHz and under 5%, so no alert either way, though its Ready (50% and 12%) is the highest.
- Misconception: C: a percentage is assumed to scale with size and so to be "fairer". For a 64-vCPU VM, 3% is a large load. Or D: 4% of 8 vCPUs taken for more than 1 GHz.

## Notes
- Public source: VCF Operations VM metrics CPU | Usage (MHz), CPU | Ready (%) (VCF Operations 9.1 documentation, metric reference); the arithmetic uses 64 x 2.4 GHz. The 20-second Ready sample is the vSphere real-time sample.
- Knowledge file logic: vsphere/object-types/vm/vm-alerts, section "Coverage and receivers": the activity gate in GHz, not %, because a small percentage of a monster VM is a sizable load; receivers (infrastructure team red and orange, application team red only); and "Misconceptions" ("Use CPU Usage % to filter idle VMs"). Values: catalog thresholds-alerts.yaml, alerts alert-vm-cpu-contention-red and -orange, and symptom sym-vm-cpu-usage-above-1ghz.
- Changed in the 2026-11-15 audit: the five mutually exclusive outcomes became one fact per option (the format told the reader one was right); throwaway D replaced by the GHz arithmetic of VM-3; F and G added; the stem drops the coinage "activity gate". Under either floor only VM-1 changes.
- Debatable risk: the gate value and the receivers are the author's design. The prompt gives them, so the question tests the effect of the proposal, not the value 1 GHz. A reader who thinks a percentage gate is better in principle still has to see that VM-1 loses its alert. The VM CPU Usage percentage is taken as relative to the VM's configured vCPUs at 2.4 GHz; the VCF Operations usage percentage is based on the VM's CPU capacity, which may use the host frequency rather than a fixed 2.4 GHz. The approximation does not change the results (VM-1 stays far from 5%).

## Metadata
```yaml
id: "0347"
title: "VM CPU alert: the usage floor in GHz"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/object-types/vm/vm-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception: [C, D]
misconception_type: [unit-and-normalization, provider-vs-consumer]
status: draft
```
