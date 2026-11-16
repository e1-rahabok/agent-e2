# Overlap on a VM with little IO of its own

## Prompt
- A 4-vCPU application VM does little disk or network IO of its own.
- It shares a host whose cores are all busy with VMs that move a lot of storage and network traffic.
- One Real-time sample (20 seconds) in the vSphere Client, VM-level values: Run 52,000 ms, Overlap 2,400 ms, Ready 600 ms, Co-stop 100 ms.

Which statements about Overlap are correct?

- A. Overlap is time a running vCPU lost while the kernel did system work such as IO.
- B. Overlap comes only from this VM's own IO, so this VM must be doing more IO than it seems.
- C. Run keeps counting during Overlap, so it overstates the time the guest executed.
- D. Overlap is part of Ready: the vCPU waited in the ready queue.
- E. For the guest, Overlap is time frozen on that vCPU: its clock does not tick.
- F. VM CPU Used counts the Overlap time as work done by this VM.
- G. Moving this VM's disks to a faster datastore cuts its Overlap.
- H. A VM's own IO never causes Overlap on that VM's own vCPUs.
- I. In this sample, the VM's Net Run comes to about 62% per vCPU.
- J. Overlap of 2,400 ms is 12% of the VM's time in this sample.

## Answers
A, C, E, I

## Explanation
- A is correct: with no free core, the kernel runs IO work (for example incoming packets) on a core that is running a vCPU, and interrupts it.
- B is wrong: the work can be for the host or for other VMs. Here the neighbours drive the IO.
- C is correct: Overlap happens inside the Run state. VCF Operations shows Net Run = Run - Overlap.
- D is wrong: the vCPU stays in Run, so Ready does not include Overlap.
- E is correct: the effect on the guest is a freeze; the guest clock does not tick for that vCPU during the interruption.
- F is wrong: Used subtracts Overlap from Run; Usage goes down when Overlap goes up.
- G is wrong: the interrupting IO belongs to the neighbours and to the host; this VM's own disks are not the source.
- H is wrong: the over-correction of B. The kernel service that interrupts a vCPU can be on behalf of the interrupted VM or of another VM.
- I is correct: VM-level ms in vCenter are summed over the vCPUs, 20,000 ms per vCPU per sample, so 80,000 ms here. Net Run = Run - Overlap = 49,600 ms, about 62% per vCPU.
- J is wrong: 2,400 ms is summed over 4 vCPUs (80,000 ms), so Overlap is about 3% per vCPU, not 12%.
- Misconception: B: Overlap is always caused by the VM's own IO. Or D: Overlap is counted in Ready. Or J: the VM-level ms read against one vCPU's 20 seconds.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): E no longer compares Overlap with Ready (Linux steal time counts Ready and not Overlap); F (Used), G (the wrong action) and H (the over-correction of B) added. Key unchanged, A, C, E.
- 2026-11-15 audit: I and J added so the sample values decide two options (Level 300 stays honest); the stem says "VM-level values" without the summation rule. E's key point no longer says to include Overlap in Guest OS sizing: the knowledge base is open on it (net-run and run remove Overlap from the sizing input; overlap and guest-os-sizing keep it inside Run).

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
source_path: "Synthetic, 2026-11-12"
misconception: [B, D, J]
misconception_type: [provider-vs-consumer, unit-and-normalization]
status: draft
```
