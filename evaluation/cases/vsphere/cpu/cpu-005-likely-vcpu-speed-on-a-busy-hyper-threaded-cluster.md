---
id: vsphere-cpu-005
title: "Likely vCPU speed on a busy Hyper-Threaded cluster"
scope: vsphere
area: cpu
input: text
tests: judgment
knowledge:
  - vsphere/cpu/concepts/cpu-frequency
  - vsphere/cpu/concepts/hyper-threading
  - vsphere/cpu/concepts/frequency-and-ht-impact-on-vm
  - vsphere/cpu/metrics/virtual-machine/usage
  - vsphere/cpu/configuration/host-power-management
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q2 VM CPU Speed"
status: draft
---

## Prompt
Cluster 007 runs ESXi 9.1 hosts with identical specifications:
- Intel Xeon 2.0 GHz.
- All Cores Turbo 3.0 GHz.
- Single Core Turbo 4.0 GHz.
- Hyper-Threading enabled.
- BIOS power management set to OS Controlled.
- ESXi power management set to Balanced, not High Performance, so frequency fluctuates.
- All other host settings are consistent and follow vSphere best practices.

What CPU speed do you tell tenants their VMs will likely get during actual run? This is not the configured speed. It is the real throughput most likely when the cluster CPUs are fairly busy serving many demanding VMs: many cores are busy and most run two threads. Which number is most realistic for one vCPU, as reported by VM CPU Usage in the vCenter real-time chart?

A. 1.6 GHz. Lower than the 2.0 GHz nominal because Hyper-Threading has a penalty.
B. 2.0 GHz. That is what is stated on the box.
C. 2.4 GHz. All Cores Turbo goes to 3.0 GHz, but Hyper-Threading reduces throughput to 2.4 GHz.
D. 3.0 GHz. Hyper-Threading does not apply to a vCPU, only to the ESXi physical core.
E. 4.0 GHz. The CPUs are only fairly busy, not very busy.

## Likely wrong answer
B (2.0 GHz, the nominal speed) or D (3.0 GHz, ignoring the Hyper-Threading charge on VM Usage).

## Expected key points
- Answer: C (2.4 GHz).
- A and B are wrong: a CPU rarely runs at base clock. It spends most time at All Cores Turbo.
- C: 3.0 GHz (All Cores Turbo) x 80%, because Hyper-Threading delivers 1.25x per core in total.
- D is wrong: VM CPU Usage is Hyper-Threading aware.
- E is less likely: most cores are busy and most run two threads, so Single Core Turbo does not apply.

## Notes
- Conflict with the knowledge base: `vm/cpu/usage` and `used` say each thread is charged 62.5% when both threads run (1.25x / 2). 3.0 GHz x 62.5% = 1.875 GHz, not 2.4 GHz. The key uses 80% (1 / 1.25). Open question Q034 in docs/author-questions.md.
