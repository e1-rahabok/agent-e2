# Likely vCPU speed on a busy Hyper-Threaded cluster

## Prompt
Cluster 007 runs ESXi 9.1 hosts with identical specifications:
- Intel Xeon 2.2 GHz.
- All Cores Turbo 3.3 GHz.
- Single Core Turbo 4.5 GHz.
- Hyper-Threading enabled.
- BIOS power management set to OS Controlled.
- ESXi power management set to Balanced, not High Performance.
- All other host settings are consistent and follow vSphere best practices.
- The cluster serves many demanding VMs: many cores are busy and most of them run two threads.

A tenant asks what CPU speed one running vCPU of their VM will get, as VM CPU Usage in the vCenter real-time chart reports it. Which statements are correct?

- A. Most of the time, one running vCPU gets about 1.8 GHz.
- B. Most of the time, one running vCPU gets about 2.2 GHz.
- C. Most of the time, one running vCPU gets about 2.6 GHz.
- D. Most of the time, one running vCPU gets about 3.3 GHz.
- E. Most of the time, one running vCPU gets about 4.5 GHz.
- F. Most of the time, one running vCPU gets about 4.1 GHz.

## Answers
C

## Explanation
- A is wrong: 1.8 GHz is 2.2 GHz × 0.8 (1.76). It applies the Hyper-Threading charge to the base clock, but a busy core runs near All Cores Turbo, not at base.
- B is wrong: 2.2 GHz is the base clock on the label; a loaded CPU rarely runs there.
- C is correct: 3.3 GHz All Cores Turbo × about 0.8 = 2.64 GHz. VM CPU Usage charges a vCPU 62.5% of the core while its sibling thread runs and the full core while the sibling is halted; on a busy cluster the mix comes to about 80%.
- D is wrong: 3.3 GHz leaves out the Hyper-Threading charge; VM CPU Usage is Hyper-Threading aware.
- E is wrong: Single Core Turbo needs most cores idle; here most cores are busy.
- F is wrong: it adds the 1.25x Hyper-Threading gain to one vCPU (3.3 × 1.25 = 4.125). The 1.25x is the total of the two threads of a core; a vCPU is charged at most the full core, about 3.3 GHz at All Cores Turbo.
- Misconception: B (2.2 GHz, the speed on the label) or D (3.3 GHz, the All Cores Turbo with the Hyper-Threading charge on VM Usage left out).

## Notes
- Author confirmed the key (Q034, 2026-11-03). Knowledge: [`vsphere/technology/cpu/concepts/cpu-frequency`](../../knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md), section Likely vCPU speed on a busy cluster.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "so frequency fluctuates" (after the power policy line).
- The 0.8 is a field figure for this scenario (cpu-frequency, section Likely vCPU speed on a busy cluster). Do not add an option at 0.625 × a clock (about 2.06 GHz, 2.8 GHz): the overcommit file states 0.625 to tenants, so two knowledge files would give two answers.
- Changed in the 2026-11-15 audit: reasons stripped from the options (C carried the only mechanism and was the longest), qualifier "most of the time" moved into every option, the interpreting stem lines removed, F (3.75 GHz) added.
- Clocks changed 2026-11-16 (re-review): the stem carried the knowledge-base example of cpu-frequency (2.0 / 3.0 / 4.0 GHz, about 2.4 GHz); now 2.2 / 3.3 / 4.5 GHz, every option recomputed, truth values unchanged.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which number is most realistic for one vCPU".

## Metadata
```yaml
id: "0005"
title: "Likely vCPU speed on a busy Hyper-Threaded cluster"
product: [vsphere]
technology: [cpu]
input: [text]
task: decide-capacity
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/concepts/cpu-frequency
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/configuration/host-power-management
knowledge_main: vsphere/technology/cpu/concepts/cpu-frequency
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q2 VM CPU Speed"
answer_type: deterministic
level: 400                      # author 2026-11-05
misconception: [B, D]
misconception_type: [frequency-and-hyper-threading]
status: draft
```
