# What VM memory contention counts

## Prompt
- In VCF Operations, a VM shows Memory|Contention (%) at 2% for the last hour. In the vSphere Client the same counter is the VM's memory Latency.

What can raise this counter?

- A. Time a vCPU waits while ESXi reads a page back from the VM's swap file.
- B. Time a vCPU is ready to run but waits for a physical core to become free.
- C. The share of the VM's memory, 2% here, that sits on media slower than DRAM.
- D. Memory that the balloon driver holds inside the Guest OS for ESXi to reuse.
- E. Time spent reading memory that sits on the other NUMA node of the host.

## Likely wrong answer
C: reading the percentage as a share of memory, not of time. Or D: counting the balloon as a wait.

## Expected key points
- Answer: A.
- The counter is the share of time a vCPU waits for a page fault that ESXi must resolve: mostly swap-in, plus decompression of a compressed page the guest touches.
- B is wrong: that is CPU Ready, a CPU wait, not a memory wait.
- C is wrong: it is a share of time, not of memory space, and not a latency in nanoseconds.
- D is wrong: ballooned pages are taken inside the guest; ESXi sees no fault on them. The counter excludes balloon.
- E is wrong: a remote NUMA access is a slower memory access, not a page fault; it shows in esxtop N%L and remote memory, not in this counter.

## Notes
- Sources: the knowledge base, VM Memory Latency (esxtop %LAT_M; VCF Operations Memory Contention maps to it); vSphere Monitoring and Performance, memory counters (latency: percentage of time the VM is waiting to access swapped or compressed memory).

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
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A]
misconception: [C, D]
misconception_type: [unit-and-normalization]
status: draft
```
