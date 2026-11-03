---
id: vsphere-cpu-009
title: "Counters where a vCPU cannot run at all"
scope: vsphere
area: cpu
input: text
tests: distinction
knowledge:
  - vsphere/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/cpu/metrics/virtual-machine/ready
  - vsphere/cpu/metrics/virtual-machine/co-stop
  - vsphere/cpu/metrics/virtual-machine/overlap
  - vsphere/cpu/metrics/virtual-machine/other-wait
  - vsphere/cpu/metrics/virtual-machine/demand
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q6 VM CPU Contention"
status: draft
---

## Prompt
In a shared environment, a VM vCPU may not get the resource it asks for: because of settings (VM, resource pool or ESXi) or a highly utilized ESXi host.

Choose all the counters that measure a VM vCPU being unable to run: it completely stops, not just runs slower.

A. CPU Ready
B. CPU Co-stop
C. CPU Overlap
D. CPU Other Wait
E. CPU Usage
F. CPU Net Run
G. CPU Demand

## Likely wrong answer
Omitting Overlap or Other Wait; including Demand as a contention counter.

## Expected key points
- Answer: A, B, C, D.
- E and F are wrong: consumption metrics, not contention.
- G is wrong: Demand is an internal counter (the key says it is affected by Hyper-Threading).

## Notes
- The knowledge base describes Demand as what utilization would be with no contention, including no Hyper-Threading loss (`vsphere/cpu/metrics/virtual-machine/demand`). The key's reason for G may conflict. Open question Q035 in docs/author-questions.md.
