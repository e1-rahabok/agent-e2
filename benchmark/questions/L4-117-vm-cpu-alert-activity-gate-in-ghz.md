# VM CPU alert: the activity gate in GHz

## Prompt
- VCF Operations. The VM CPU contention alert (one definition for every VM) has three conditions, all required in the same cycle:
  - Red: highest 20-second vCPU Ready above 32%, CPU Ready (%) of the cycle above 8%, and CPU Usage above 1 GHz.
  - Orange: highest 20-second vCPU Ready above 16%, CPU Ready (%) above 4%, and CPU Usage above 1 GHz.
- The infrastructure team receives red and orange. The application team receives red only.
- The 1 GHz usage floor is called an activity gate. A colleague proposes to change it to a percentage so it "scales with VM size": CPU Usage above 5% of the VM's capacity.
- The hosts run at 2.4 GHz per core. In the current cycle, four VMs show:

| VM | vCPUs | CPU Usage | Highest 20-second Ready | CPU Ready (cycle) |
|---|---|---|---|---|
| VM-1 | 64 | 3% | 41% | 9% |
| VM-2 | 2 | 40% | 20% | 5% |
| VM-3 | 8 | 4% | 50% | 12% |
| VM-4 | 4 | 12% | 45% | 3% |

What does the change from 1 GHz to 5% do to the notifications of these four VMs, compared with today?

- A. It silences the red alert of VM-1 (and so the application team no longer hears of it) and changes nothing for the other three VMs.
- B. It silences the red alert of VM-1 and adds an orange alert on VM-4, because VM-4 uses 12% of its capacity, over 5%.
- C. It changes nothing: a 5% floor and a 1 GHz floor select the same VMs, because both measure the same activity.
- D. It silences VM-1 and VM-2 and adds an alert on VM-3, because the percentage penalizes the large VM and favors the small ones.
- E. It demotes the red alert of VM-1 to orange, so only the infrastructure team is told, and changes nothing for the others.

## Likely wrong answer
C: a percentage is assumed to scale with size and so to be "fairer". For a 64-vCPU VM, 3% is a large load.

## Expected key points
- Answer: A.
- Today's gate: 1 GHz. VM-1 uses 3% of 64 x 2.4 = 153.6 GHz = about 4.6 GHz, over 1 GHz, with Ready 41% (>32%) and 9% (>8%): red, sent to both teams. VM-2 uses 40% of 4.8 GHz = 1.9 GHz: highest Ready 20% (>16, <32) and 5% (>4, <8): orange, infrastructure team only. VM-3 uses 4% of 19.2 GHz = 0.77 GHz, under 1 GHz: no alert although Ready is high. VM-4 uses 12% of 9.6 GHz = 1.15 GHz, but Ready 3% is under 4%: no alert.
- With a 5% gate: VM-1 (3%) falls under the floor and loses its red alert, so the application team of the VM is no longer told: a small percentage of a large VM is a large load. VM-2 (40%) passes as before. VM-3 (4%) stays silent. VM-4 (12%) passes the gate but not the Ready condition. Only VM-1 changes.
- The floor is in GHz because the load that matters is absolute: 3% of a 64-vCPU VM is 4.6 GHz of work, more than the busiest part of a small VM. The gate exists to keep the alert off idle VMs, where the business impact is likely negligible.
- B is wrong because VM-4 has CPU Ready (cycle) of 3%, under the orange 4%. D and E do not follow from the table.

## Notes
- Public source: VCF Operations VM metrics CPU | Usage (MHz), CPU | Ready (%) (VCF Operations 9.1 documentation, metric reference); the arithmetic uses 64 x 2.4 GHz. The 20-second Ready sample is the vSphere real-time sample.
- Knowledge file logic: vsphere/object-types/vm/vm-alerts, section "Coverage and receivers": the activity gate in GHz, not %, because a small percentage of a monster VM is a sizable load; receivers (infrastructure team red and orange, application team red only); and "Misconceptions" ("Use CPU Usage % to filter idle VMs"). Values: catalog thresholds-alerts.yaml, alerts alert-vm-cpu-contention-red and -orange, and symptom sym-vm-cpu-usage-above-1ghz.
- Why one answer: with the rule values in the prompt the four VMs give one result under each gate, and only VM-1 differs.
- Debatable risk: the gate value and the receivers are the author's design. The prompt gives them, so the question tests the effect of the proposal, not the value 1 GHz. A reader who thinks a percentage gate is better in principle still has to see that VM-1 loses its alert. The VM CPU Usage percentage is taken as relative to the VM's configured vCPUs at 2.4 GHz; the VCF Operations usage percentage is based on the VM's CPU capacity, which may use the host frequency rather than a fixed 2.4 GHz. The approximation does not change the results (VM-1 stays far from 5%).

## Metadata
```yaml
id: "0347"
title: "VM CPU alert: the activity gate in GHz"
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
answer: [A]
misconception: [C]
misconception_type: [unit-and-normalization, provider-vs-consumer]
status: draft
```
