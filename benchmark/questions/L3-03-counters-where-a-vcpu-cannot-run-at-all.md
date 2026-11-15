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
- H. CPU Latency
- I. CPU Swap Wait

## Likely wrong answer
Omitting Overlap, Other Wait or Swap Wait; including Demand or Latency as a counter of a stopped vCPU.

## Expected key points
- Answer: A, B, C, D, I.
- A is true: in Ready the vCPU demands runtime and the kernel has no physical thread for it.
- B is true: in Co-stop the vCPU is held back to stay in step with a sibling vCPU.
- C is true: Overlap is time a running vCPU was interrupted for kernel work; the guest feels a freeze.
- D is true: Other Wait is time the vCPU is blocked by something other than memory (IO, vMotion, snapshot); a freeze for the guest.
- E and F are false: Usage and Net Run count consumption, not time stopped.
- G is false: Demand is what the VM would use with no core sharing, a kernel scheduler value; it does not measure a vCPU unable to run.
- H is false: Latency also counts a vCPU that runs slower (a busy sibling thread, a clock below nominal), so it mixes slower running with stopping.
- I is true: Swap Wait is time the vCPU waits for a page to come in from ESXi swap; the guest feels a freeze, although the cause is memory.

## Notes
- Author confirmed the key (Q035, 2026-11-03). Demand is a VM-realm counter and is affected by Hyper-Threading. The Guest OS realm does not see physical threads. Knowledge: [`vsphere/architecture/vm-vs-guest-os`](../../knowledge/vsphere/architecture/vm-vs-guest-os.md), section Two realms.
- Misconception: applying a Guest OS-realm statement to a VM-realm counter.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "In a shared environment, a VM vCPU may not get the resource it asks for: because of settings (VM, resource pool or ESXi) or a highly utilized ESXi host."
- Options added 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): H (Latency, the over-correction: a contention counter that also counts slower running) and I (Swap Wait). Key changed from A, B, C, D to A, B, C, D, I (author approved, 2026-11-14).

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
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
knowledge_main: vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q6 VM CPU Contention"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [A, B, C, D, I]
misconception: [G, H]
misconception_type: [consumption-as-contention]
pair: "0376"
status: draft
```
