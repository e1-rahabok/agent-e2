# What VM memory contention counts

## Prompt
- In VCF Operations, a VM shows Memory|Contention (%) at 2% for the last hour.

Which statements about this counter are correct?

- A. It rises when a vCPU waits while ESXi reads a page back from the VM's swap file.
- B. It rises when a vCPU is ready to run but waits for a physical core to become free.
- C. The 2% is the share of the VM's memory that sits on media slower than DRAM.
- D. It counts the memory that the balloon driver holds inside the Guest OS for ESXi to reuse.
- E. It rises when a vCPU reads memory that sits on the other NUMA node of the host.
- F. It counts the same waits as CPU Swap Wait, and nothing more.
- G. It rises when a vCPU waits while ESXi decompresses a page that the guest touches.
- H. At 2%, the VM's configured memory is too small: add memory to the VM.

## Likely wrong answer
C: reading the percentage as a share of memory, not of time. Or D: counting the balloon as a wait.

## Expected key points
- Answer: A, G.
- The counter is the share of time a vCPU waits for a page fault that ESXi must resolve: mostly swap-in, plus decompression of a compressed page the guest touches.
- A is right: swap-in is the main source.
- B is wrong: that is CPU Ready, a CPU wait, not a memory wait.
- C is wrong: it is a share of time, not of memory space, and not a latency in nanoseconds.
- D is wrong: ballooned pages are taken inside the guest; ESXi sees no fault on them. The counter excludes balloon.
- E is wrong: a remote NUMA access is a slower memory access, not a page fault; it shows in esxtop N%L and remote memory, not in this counter.
- F is wrong: Memory Latency is a superset of CPU Swap Wait; Swap Wait covers swap-in only, Latency also covers decompression. This is the over-correction of D (only swap counts).
- G is right: decompression of a touched compressed page is a page fault ESXi resolves.
- H is wrong: memory contention measures speed, not space; it comes from host reclamation or a limit, so the configured size is not shown to be short. Find the cause first.

## Notes
- Sources: the knowledge base, VM Memory Latency (esxtop %LAT_M; VCF Operations Memory Contention maps to it); vSphere Monitoring and Performance, memory counters (latency: percentage of time the VM is waiting to access swapped or compressed memory).
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "In the vSphere Client the same counter is the VM's memory Latency."
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): F the over-correction, G the decompression wait and H the wrong action added; stem made plural and the options made statements. Key changed from A to A, G.

## Metadata
```yaml
id: "0149"
title: "What VM memory contention counts"
product: [vsphere, vcf-operations]
technology: [memory]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/tools/esxtop/memory
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, G]
misconception: [C, D]
misconception_type: [unit-and-normalization]
pair: "0392"
status: draft
```
