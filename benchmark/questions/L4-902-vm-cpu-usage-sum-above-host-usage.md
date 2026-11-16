# Sum of VM CPU Usage above host CPU Usage

## Prompt
- ESXi 9.1 host esx-07: 2 sockets of 16 cores, base clock 2.5 GHz, Hyper-Threading on (64 logical processors). It runs 26 VMs.
- Turbo Boost is off in the BIOS of this host for a power test, so the cores ran at 2.5 GHz all hour.
- The finance team builds the CPU chargeback from vCenter. For 14:00-15:00 on one day:
  - sum of the CPU Usage (MHz) of the 26 VMs: 82,450 MHz
  - host CPU Usage (MHz): 70,000 MHz; host Usage (%): 87.5
  - host Utilization (%): 75; host Core Utilization (%): 87.5
  - VMkernel system worlds: below 100 MHz
- Finance says vCenter counts about 12,450 MHz twice.

Which statements are correct?

- A. On a core with both threads busy, VM CPU Usage charges each vCPU 62.5% of the core; host CPU Usage gives each thread half of it.
- B. On average about 20 cores had both threads busy: 75% of 64 threads less 87.5% of 32 cores.
- C. The gap is about a quarter of a core for each of those cores: 20 × 2,500 MHz × 0.25, or 12,500 MHz.
- D. The 12,450 MHz is CPU the VMkernel used for its own work, which the VM counters leave out.
- E. Host CPU Usage counts a core with both threads busy as 125% of the core, so the host value is too high.
- F. The VM sum and the host value have to match, so the gap is a vCenter collection error.
- G. With Turbo on, both counters would rise by the same frequency factor, so Turbo would not close the gap.
- H. Host Usage (%) equals Core Utilization in this hour because the cores ran at their base clock.
- I. Host Usage (%) carries the Hyper-Threading charge for a shared core in the same way as VM Usage (%).
- J. Host Usage of 87.5% shows that 12.5% of the host's CPU is left for new VMs.

## Likely wrong answer
"The VMs cannot use more CPU than the host has, so vCenter double-counts (F); or the host is the one over-counting, at 125% per busy core (E)." E and F are the misconceptions.

## Expected key points
- Answer: A, B, C, G, H.
- A is correct: VM CPU Used and VM CPU Usage carry the 1.25x Hyper-Threading charge, 62.5% of the core per vCPU while the sibling thread runs; ESXi CPU Used, behind host Usage, gives each thread of a busy pair half the core, so the pair adds to 100%.
- B is correct: busy threads = busy cores + cores with both threads busy, and the averages keep that relation: 0.75 × 64 = 48 threads, 0.875 × 32 = 28 cores, 48 − 28 = 20 cores with both threads busy.
- C is correct: each such core is charged 2 × 62.5% = 125% to the VMs and 100% to the host, a quarter of a core more: 20 × 2,500 × 0.25 = 12,500 MHz, against the 82,450 − 70,000 = 12,450 MHz gap (the system worlds account for the rest).
- D is wrong: kernel work runs on the host's threads and sits in the host value, not in the VM sum; it would make the host value higher, not lower.
- E is wrong: host CPU Usage gives a busy pair 100% of the core (half per thread); 62.5% per vCPU, 125% per core, is the VM-side charge.
- F is wrong: the two counters charge a busy Hyper-Threading core by different rules, so on a busy host the VM sum exceeds the host value with no data error.
- G is correct: frequency scales VM CPU Used and ESXi CPU Used alike; Turbo would raise both and the gap with them.
- H is correct: host Usage (%) is 70,000 / 80,000 = 87.5%; with a static clock it equals Core Utilization, as a core counts once whether one or two threads run.
- I is wrong: VM Usage (%) is Hyper-Threading aware; host Usage (%) is not, and a second thread on a busy core adds nothing to it.
- J is wrong: host Usage (%) is not a capacity reading; space for vCPUs is counted in threads (Utilization 75%), and Usage moves with frequency.

## Metadata
```yaml
id: "0444"
title: "Sum of VM CPU Usage above host CPU Usage"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/host/used
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics
  - vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
knowledge_main: vsphere/technology/cpu/metrics/host/used
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/cpu/metrics/host/used"
answer: [A, B, C, G, H]
misconception: [E, F]
misconception_type: [frequency-and-hyper-threading, same-name-other-object]
status: draft
```
