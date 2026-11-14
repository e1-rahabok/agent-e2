# VM availability

## Prompt
- A VM is powered on, but Windows inside it has crashed and is stuck on a blue screen.

Which statements are correct?

- A. Record this crash as VM downtime in the monthly availability report.
- B. The VM is down, because the Windows inside it has crashed.
- C. The Guest OS, Windows, is the layer that is unavailable in this situation.
- D. A VM is unavailable only when it is powered off, or frozen with its clock paused.
- E. A VM is the virtual hardware; Windows is a separate layer that runs on it.
- F. A VM sitting at the BIOS screen with no OS booted counts as available.
- G. Guest OS availability is checked from inside the OS, for example by querying the RPC service on Windows.
- H. Process count and thread count are VM metrics that vCenter keeps for this VM.
- I. On Linux, `systemctl is-system-running` returning `degraded` means the kernel is down.
- J. The memory copy phase of a vMotion, which can take minutes, is time when the VM is unavailable.
- K. The applications on this VM count as available, because the VM itself is available.

## Likely wrong answer
- B: "Windows crashed, so the VM is down." Or the over-correction K: "the VM is up, so the applications on it are up."

## Expected key points
- Answer: C, D, E, F, G.
- A is false: the wrong action. The VM stayed available (its BIOS ran); the outage belongs to the Guest OS and the applications, and counting it as VM downtime mixes the layers.
- B is false: it mixes the two layers; the Guest OS is down, the VM is not.
- C is true: Windows is the layer that failed.
- D is true: the only two VM-unavailable states are powered off and frozen (the actual vMotion downtime, about 0.2 s when healthy).
- E is true: a VM is not a complete machine and not the OS; VM and Guest OS are adjacent layers, 1:1, but distinct.
- F is true: if the BIOS is running, the VM is 100% available, even if Windows or Linux has not booted.
- G is true: Guest OS availability needs OS-level checks such as `sc query RpcSs` (Windows) or `systemctl is-system-running` (Linux).
- H is false: processes, threads and system calls are Guest OS metrics; they do not apply to a VM.
- I is false: `degraded` means the kernel and main system are up and at least one service has failed.
- J is false: the VM is frozen only during the actual switch-over downtime, not during the copy time.
- K is false: the over-correction. The applications run on the Guest OS, which is down; an available VM says nothing about the layers above it.

## Notes
- Paired with the screenshot question 0435 (design.md, section 3.9).
- Tests: Principle: a VM is the virtual hardware, not the OS.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A ("the VM is available", the negation of B) replaced by the wrong action; K added as the over-correction (author approved, 2026-11-14). Key changed from A, C, D, E, F, G to C, D, E, F, G.

## Metadata
```yaml
id: "0015"
title: "VM availability"
product: [vsphere]
technology: [system]
input: [text]
task: explain-mechanism
knowledge:
  - vsphere/architecture/vm-vs-guest-os
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: What, exactly, is a VM?"
answer_type: deterministic
answer: [C, D, E, F, G]
misconception: [B, K]
level: 300                      # author 2026-11-05
object: [vm, guest-os]
tool: [none]
knowledge_main: vsphere/architecture/vm-vs-guest-os
misconception_type: [layer-confusion]
pair: "0435"
status: draft
```
