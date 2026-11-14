# High CPU Wait

## Prompt
- A 4-vCPU VM, over the last hour, per vCPU on average: CPU Wait about 90%, Run about 9.5%, Ready about 0.5%, Co-stop 0%.
- The application owner says the VM must be stuck waiting on disk or memory.

Which statements are correct?

- A. CPU Wait counts the time a vCPU sits halted in the Guest OS idle loop.
- B. A Wait of 90% shows the VM is blocked on disk or memory most of the time.
- C. With Run near 10% and almost no Ready or Co-stop, a Wait near 90% is what a mostly idle VM shows.
- D. From the hypervisor scheduler's view an idle vCPU is waiting to be used, hence the name Wait.
- E. A disk or memory bottleneck has to be shown by other counters, such as disk latency or memory contention.
- F. Wait is the share of time a vCPU had work to do but no physical thread to run on.
- G. Time spent waiting for pages from ESXi swap is not part of Wait, so memory waits never show in it.
- H. A vCPU in Wait keeps its physical thread, so a 90% Wait ties up most of four threads.
- I. VM CPU Wait is the same measure as the Guest OS's own IO wait, such as Linux iowait.
- J. Size the VM's vCPUs with all of Wait counted as demand, since the guest asked for that time.

## Likely wrong answer
- B: "Wait is 90%, so the VM is waiting on disk or memory almost all the time."

## Expected key points
- Answer: A, C, D, E.
- A is true: Wait includes idle; a vCPU the guest halts (HLT or MWAIT) is de-scheduled and counted in Wait.
- B is false: most of the 90% is idle time; ESXi cannot tell an idle guest from one blocked on IO.
- C is true: Run + Ready + Co-stop + Wait = 100% per vCPU; most VMs do not run at 100%, so Wait is naturally high.
- D is true: the name is right from the kernel scheduler's vantage point.
- E is true: high Wait alone proves no bottleneck; disk latency and memory latency (contention) give the evidence.
- F is false: that is Ready.
- G is false: Wait = Idle + Swap Wait + Other Wait; Swap Wait is part of it, which is why Wait cannot be read as idle alone without the other counters.
- H is false: a halted vCPU holds no physical thread; another VM can run on it.
- I is false: Guest OS IO wait can show as VM Run (guest IO processing) or as VM Wait.
- J is false: Idle is excluded from sizing; only Swap Wait and Other Wait count as demand.

## Notes
- Tests: Confusing name (distinction).
- Prompt sharpened with Run, Ready and Co-stop values, so option C is decidable.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0001"
title: "High CPU Wait"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/metrics/virtual-motherboard/idle
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/wait
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity (Confusing name)."
answer_type: deterministic
answer: [A, C, D, E]
misconception: [B]
level: 300                      # author 2026-11-05
misconception_type: [layer-confusion]
status: draft
```
