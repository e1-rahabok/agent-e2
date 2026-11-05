# Likely vCPU speed on a busy Hyper-Threaded cluster

## Prompt
Cluster 007 runs ESXi 9.1 hosts with identical specifications:
- Intel Xeon 2.0 GHz.
- All Cores Turbo 3.0 GHz.
- Single Core Turbo 4.0 GHz.
- Hyper-Threading enabled.
- BIOS power management set to OS Controlled.
- ESXi power management set to Balanced, not High Performance, so frequency fluctuates.
- All other host settings are consistent and follow vSphere best practices.

- What CPU speed do you tell tenants their VMs will likely get during actual run? This is not the configured speed.
- It is the real throughput most likely when the cluster CPUs are fairly busy serving many demanding VMs: many cores are busy and most run two threads.

Which number is most realistic for one vCPU, as reported by VM CPU Usage in the vCenter real-time chart?

- A. 1.6 GHz. Lower than the 2.0 GHz nominal because Hyper-Threading has a penalty.
- B. 2.0 GHz. That is what is stated on the box.
- C. 2.4 GHz. All Cores Turbo goes to 3.0 GHz, but Hyper-Threading reduces throughput to 2.4 GHz.
- D. 3.0 GHz. Hyper-Threading does not apply to a vCPU, only to the ESXi physical core.
- E. 4.0 GHz. The CPUs are only fairly busy, not very busy.

## Likely wrong answer
B (2.0 GHz, the nominal speed) or D (3.0 GHz, ignoring the Hyper-Threading charge on VM Usage).

## Expected key points
- Answer: C (2.4 GHz).
- A and B are wrong: a CPU rarely runs at base clock. It spends most time at All Cores Turbo.
- C: 3.0 GHz (All Cores Turbo) x 80%, because Hyper-Threading delivers 1.25x per core in total.
- D is wrong: VM CPU Usage is Hyper-Threading aware.
- E is less likely: most cores are busy and most run two threads, so Single Core Turbo does not apply.

## Notes
- Author confirmed the key (Q034, 2026-11-03). Knowledge: `vsphere/technology/cpu/concepts/cpu-frequency`, section Likely vCPU speed on a busy cluster.

## Metadata
```yaml
id: vsphere-cpu-005
title: "Likely vCPU speed on a busy Hyper-Threaded cluster"
scope: vsphere
product: [vsphere]
technology: [cpu]
area: cpu
input: [text]
tests: judgment
knowledge:
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/configuration/host-power-management
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q2 VM CPU Speed"
answer_type: deterministic
level: 400                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [C]
trap: [B,D]
status: draft
```
