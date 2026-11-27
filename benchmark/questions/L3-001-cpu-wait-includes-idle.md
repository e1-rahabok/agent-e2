# High CPU Wait

## Prompt
- A 4-vCPU VM, over the last hour, per vCPU on average: CPU Wait about 90%, Run about 9.5%, Ready about 0.5%, Co-stop 0%.
- The application owner says the VM must be stuck waiting on disk or memory.

Which statements are correct?

- A. CPU Wait counts the time a vCPU sits halted in the Guest OS idle loop.
- B. A Wait of 90% shows the VM is blocked on disk or memory most of the time.
- C. With Run near 10% and almost no Ready or Co-stop, 90% Wait is what a mostly idle VM shows.
- D. From the hypervisor scheduler's view an idle vCPU is waiting to be used, hence the name Wait.
- E. To find a disk or memory bottleneck in this VM, read the Windows or Linux counters, not VM CPU Wait.
- F. Wait is the share of time a vCPU had work to do but no physical thread to run on.
- G. Time a vCPU spends waiting for pages from ESXi swap is counted outside the Wait state.
- H. A vCPU in Wait keeps its physical thread, so a 90% Wait ties up most of four threads.
- I. VM CPU Wait is the same measure as the Guest OS's own IO wait, such as Linux iowait.
- J. Size the VM's vCPUs with all of Wait counted as demand: the guest asked for that time.

## Answers
A, C, D, E

## Explanation
- A is correct: Wait includes idle; a vCPU the guest halts (HLT or MWAIT) is de-scheduled and counted in Wait.
- B is wrong: most of the 90% is idle time; ESXi cannot tell an idle guest from one blocked on IO.
- C is correct: Run + Ready + Co-stop + Wait = 100% per vCPU; most VMs do not run at 100%, so Wait is naturally high.
- D is correct: the name is right from the kernel scheduler's vantage point.
- E is correct: the hypervisor cannot tell a guest waiting for IO from an idle one, so high Wait alone proves no bottleneck; IO and memory bottlenecks are read and fixed at the Guest OS level, with Windows and Linux metrics.
- F is wrong: that is Ready.
- G is wrong: Wait = Idle + Swap Wait + Other Wait; Swap Wait is part of it, which is why Wait cannot be read as idle alone without the other counters.
- H is wrong: a halted vCPU holds no physical thread; another VM can run on it.
- I is wrong: Guest OS IO wait can show as VM Run (guest IO processing) or as VM Wait.
- J is wrong: Idle is excluded from sizing; only Swap Wait and Other Wait count as demand.
- Misconception: B: "Wait is 90%, so the VM is waiting on disk or memory almost all the time."

## Notes
- Tests: Confusing name (distinction).
- Prompt sharpened with Run, Ready and Co-stop values, so option C is decidable.
- Converted from judged to multiple choice (Q-E2-199 F, 2026-11-14).
- 2026-11-16 re-review: E ("must show in ... disk latency, memory contention") was stronger than the knowledge base: a guest short of its own memory need not show VM memory contention. E now points to the Windows and Linux counters (idle, Sizing; wait, Mechanism). Truth kept; key unchanged.
- 2026-11-15 audit: G and J reworded without absolutes or because clauses (truth kept). Not added: an option on the ESXi 8.0 Update 2 idle-accounting issue (Broadcom KB 338438), which needs a mixed-version estate in the stem.

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
misconception: [B]
level: 300                      # author 2026-11-05
misconception_type: [layer-confusion]
pair: "0372"
status: draft
```
