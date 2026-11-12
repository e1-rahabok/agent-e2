# A CPU counter that points at memory

## Prompt
- erp-db-02: 4 vCPUs, 32 GB of memory, no limit, no reservation.
- Last week its host ran short of memory after another host failed. The host now has 40% free memory.
- Since then: Swapped is flat at 6 GB, and Swap In Rate is above 0 most of the time.
- Users say queries are slow. The DBA says the CPU must be the problem, because a CPU counter is high.
- [The attached vSphere Client export](0109/erp-db-02-cpu-real-time.csv) holds 30 minutes of Real-time points: CPU Run, Ready, Co-stop and Swap wait, in ms per 20-second sample, summed over the 4 vCPUs (80,000 ms is 100%).

Which statements are correct?

- A. The vCPUs wait for memory pages read back from ESXi swap: the cause is memory, not CPU.
- B. The VM is short of CPU: add vCPUs to absorb the wait.
- C. The host has free memory now, so pages swapped last week can no longer slow the VM.
- D. Ready and Co-stop are low: the VM gets its physical threads when it needs them.
- E. The VM's Memory Latency counter shows the same wait, and also counts time spent decompressing pages.
- F. Swapped at 6 GB is the size of the VM's swap file.

## Likely wrong answer
B: a high CPU counter read as a CPU shortage. Or C: swapping is over, so it cannot hurt now.

## Expected key points
- Answer: A, D, E.
- A: Swap wait is time a vCPU waits for a page to come in from ESXi swap, about 5-11% per vCPU here. It is a CPU state with a memory cause.
- B is wrong: more vCPUs do not bring the pages back faster.
- C is wrong: swapped pages stay in swap until the guest touches them. Each touch reads the page back (Swap In Rate above 0) and the vCPU waits.
- D: Ready below 1% and Co-stop below 0.1% per vCPU.
- E: Memory Latency covers swap-in and decompression; Swap wait covers swap-in only. VCF Operations counts this wait in memory contention, not CPU contention.
- F is wrong: Swapped is what sits in swap now. The swap file is sized at configured memory minus the memory reservation (32 GB here).
- What to do: keep the host out of memory pressure. The wait fades as the guest reads its pages back (Swapped falls, Consumed rises).

## Metadata
```yaml
id: "0109"
title: "A CPU counter that points at memory"
product: [vsphere]
technology: [cpu, memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
attachments:
  - 0109/erp-db-02-cpu-real-time.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2)"
answer: [A, D, E]
misconception: [B, C]
misconception_type: [reclamation-as-contention, same-name-other-object]
status: draft
```
