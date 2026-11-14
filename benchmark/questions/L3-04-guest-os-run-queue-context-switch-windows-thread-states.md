# Guest OS run queue, context switch, Windows thread states

## Prompt
Choose all the correct sentences about Windows and Linux CPU performance:

- A. The Guest OS is aware of Hyper-Threading and schedules its processes accordingly.
- B. The CPU run queue has no bearing on application performance, since Windows and Linux queue threads all the time.
- C. A high context switch rate calls for more vCPUs.
- D. Windows Processor Queue Length leaves out the running threads; the Linux run queue counts them.
- E. A context switch costs CPU time that could otherwise run application work.
- F. In Windows, the processor queue length counts threads in the Ready, Standby and Deferred Ready (Unknown) states.
- G. A thread blocked on a lock adds to the Windows processor queue length.
- H. A sustained queue of 1 thread per vCPU already shows a CPU shortage.

## Likely wrong answer
A (Guest OS assumed Hyper-Threading aware), B (the queue dismissed as normal), or C (a high switch rate read as a CPU shortage).

## Expected key points
- Answer: D, E, F.
- A is false: the Guest OS is unaware of host Hyper-Threading.
- B is false: queued threads cannot run; the run queue is the primary Guest OS counter for whether the CPU keeps up with demand.
- C is false: a high switch rate is not a CPU shortage; check the run queue. More vCPUs can raise switching.
- D is true: Windows excludes running threads from the queue; Linux includes them.
- E is true: a switch costs scheduler work, TLB flushes and cache reloads.
- F is true: Ready, Standby and Deferred Ready all indicate a CPU problem, and all three are in the counter.
- G is false: a thread blocked on a lock is in the Wait state; it joins the queue only when the lock is released.
- H is false: a short queue is normal; MSDN reads above 2 per processor sustained as congestion, and PerfMon below 10 per processor as acceptable.

## Notes
- Author confirmed D, E, F (Q036, 2026-11-03). The quiz document's answer column lists D, E only.
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Windows or Linux performance affects application performance. Some of these issues are not visible to the VM."
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the true D and E no longer negate B and C; C is now the wrong action; G and H are new (H is the over-correction of B). Key letters unchanged, D, E, F; D now states a different fact (author approved, 2026-11-14).

## Metadata
```yaml
id: "0010"
title: "Guest OS run queue, context switch, Windows thread states"
product: [vsphere, windows]
technology: [cpu]
input: [text]
task: read-metric
object: [guest-os]
tool: [guest-os-tools]
knowledge:
  - guest-os/cpu/windows-cpu-scheduling
  - guest-os/cpu/metrics/run-queue
  - guest-os/cpu/metrics/context-switch
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
knowledge_main: guest-os/cpu/windows-cpu-scheduling
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q7 Guest OS CPU"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [D, E, F]
misconception: [A, B, C]
misconception_type: [layer-confusion, frequency-and-hyper-threading]
pair: "0434"
status: draft
```
