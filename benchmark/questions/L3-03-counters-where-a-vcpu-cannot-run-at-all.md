# Counters where a vCPU cannot run at all

## Prompt
Choose all the counters that measure a VM vCPU being unable to run: it completely stops, not just runs slower.

- A. CPU Ready
- B. CPU Co-stop
- C. CPU Overlap
- D. CPU Other Wait
- E. CPU Usage
- F. CPU Net Run
- G. CPU Demand

## Likely wrong answer
Omitting Overlap or Other Wait; including Demand as a contention counter.

## Expected key points
- Answer: A, B, C, D.
- E and F are wrong: consumption metrics, not contention.
- G is wrong: Demand is an internal counter (the key says it is affected by Hyper-Threading).

## Notes
- Author confirmed the key (Q035, 2026-11-03). Demand is a VM-realm counter and is affected by Hyper-Threading. The Guest OS realm does not see physical threads. Knowledge: [`vsphere/architecture/vm-vs-guest-os`](../../knowledge/vsphere/architecture/vm-vs-guest-os.md), section Two realms.
- Misconception: applying a Guest OS-realm statement to a VM-realm counter.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "In a shared environment, a VM vCPU may not get the resource it asks for: because of settings (VM, resource pool or ESXi) or a highly utilized ESXi host."

## Metadata
```yaml
id: "0009"
title: "Counters where a vCPU cannot run at all"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/metrics/virtual-motherboard/overlap
  - vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/demand
knowledge_main: vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q6 VM CPU Contention"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [A,B,C,D]
misconception: [G]
misconception_type: [consumption-as-contention]
status: draft
```
