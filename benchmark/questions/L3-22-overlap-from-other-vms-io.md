# Overlap on a VM with little IO of its own

## Prompt
- A 4-vCPU application VM does little disk or network IO of its own.
- It shares a host whose cores are all busy with VMs that move a lot of storage and network traffic.
- One Real-time sample (20 seconds), summed over the 4 vCPUs: Run 52,000 ms, Overlap 2,400 ms, Ready 600 ms, Co-stop 100 ms.

Which statements about Overlap are correct?

- A. Overlap is time a running vCPU was interrupted so the hypervisor could do system work, such as processing IO.
- B. Overlap comes only from this VM's own IO, so this VM must be doing more IO than it seems.
- C. Run keeps counting during Overlap, so Run overstates the time the guest really executed.
- D. Overlap is part of Ready: the vCPU waited in the ready queue.
- E. For the guest, Overlap is time frozen on that vCPU.
- F. Used counts the Overlap time as work done by the VM.
- G. Moving this VM's disks to a faster datastore cuts its Overlap.

## Likely wrong answer
B: Overlap is always caused by the VM's own IO. Or D: Overlap is counted in Ready.

## Expected key points
- Answer: A, C, E.
- A: with no free core, the kernel runs IO work (for example incoming packets) on a core that is running a vCPU, and interrupts it.
- B is wrong: the work can be for the host or for other VMs. Here the neighbours drive the IO.
- C: Overlap happens inside the Run state. VCF Operations shows Net Run = Run - Overlap.
- D is wrong: the vCPU stays in Run, so Ready does not include Overlap.
- E: the guest clock does not tick for that vCPU during the interruption; include Overlap when sizing the guest.
- F is wrong: Used subtracts Overlap from Run; Usage goes down when Overlap goes up.
- G is wrong: the interrupting IO belongs to the neighbours and to the host; this VM's own disks are not the source.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): E no longer compares Overlap with Ready (Linux steal time counts Ready and not Overlap); F (Used) and G (the wrong action) added. Key unchanged, A, C, E.

## Metadata
```yaml
id: "0110"
title: "Overlap on a VM with little IO of its own"
product: [vsphere]
technology: [cpu]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/overlap
  - vsphere/technology/cpu/metrics/virtual-motherboard/net-run
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/overlap
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, E]
misconception: [B, D]
misconception_type: [provider-vs-consumer]
status: draft
```
