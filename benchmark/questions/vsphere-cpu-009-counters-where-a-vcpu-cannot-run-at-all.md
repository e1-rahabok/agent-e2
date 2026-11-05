# Counters where a vCPU cannot run at all

## Prompt
In a shared environment, a VM vCPU may not get the resource it asks for: because of settings (VM, resource pool or ESXi) or a highly utilized ESXi host.

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
- Author confirmed the key (Q035, 2026-11-03). Demand is a VM-realm counter and is affected by Hyper-Threading. The Guest OS realm does not see physical threads. Knowledge: `vsphere/foundations/vm-vs-guest-os`, section Two realms.
- Trap: applying a Guest OS-realm statement to a VM-realm counter.

## Metadata
```yaml
id: vsphere-cpu-009
title: "Counters where a vCPU cannot run at all"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
knowledge:
  - vsphere/foundations/vm-vs-guest-os
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/metrics/virtual-motherboard/overlap
  - vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/demand
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q6 VM CPU Contention"
answer_type: deterministic
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [A,B,C,D]
trap: [G]
status: draft
```
