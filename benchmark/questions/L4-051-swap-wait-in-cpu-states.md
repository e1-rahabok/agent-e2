# A CPU counter that points at memory

## Prompt
- erp-db-02: 4 vCPUs, 32 GB of memory, no limit, no reservation.
- Last week its host ran short of memory after another host failed. The host now has 40% free memory.
- Since then: Swapped is flat at 6 GB, and Swap In Rate is above 0 most of the time.
- Users say queries are slow. The DBA says the CPU must be the problem, because a CPU counter is high.
- [The attached vSphere Client export](0109/erp-db-02-cpu-real-time.csv) holds 30 minutes of Real-time points: CPU Run, Ready, Co-stop and Swap wait of the VM, in ms per 20-second sample.

Which statements are correct?

- A. The vCPUs wait for memory pages read back from ESXi swap: the cause is memory, not CPU.
- B. The VM is short of CPU: add vCPUs so the work goes on while some of them wait.
- C. Ready and Co-stop are low: the VM gets its physical threads when it needs them.
- D. Memory Latency shows the same wait and also counts time spent decompressing pages.
- E. Swapped at 6 GB is the size of the swap file the VM has on its datastore.
- F. A faster swap location for the VM would lower its Swap wait as pages come back.
- G. ESXi counts Swap wait inside Ready, so this VM's Ready includes the swap stalls.

## Likely wrong answer
B: a high CPU counter read as a CPU shortage: "the CPU counter is high, so give it more CPU."

## Expected key points
- Answer: A, C, D, F.
- A is correct: Swap wait is time a vCPU waits for a page to come in from ESXi swap. The VM-level ms are summed over the 4 vCPUs (80,000 ms per sample), so about 4,100-9,200 ms is about 5-11% per vCPU. It is a CPU state with a memory cause.
- B is wrong: more vCPUs do not bring the pages back faster.
- C is correct: Ready below 1% and Co-stop below 0.1% per vCPU.
- D is correct: Memory Latency covers swap-in and decompression; Swap wait covers swap-in only. VCF Operations counts this wait in memory contention, not CPU contention.
- E is wrong: Swapped is what sits in swap now. The swap file is sized at configured memory minus the memory reservation (32 GB here).
- F is correct: each wait is the time to read a page back from swap; a faster swap location (like more host memory for the VM) lowers Swap Wait, so Run goes up.
- G is wrong: Swap Wait is part of the Wait state, not of Ready; the export shows it too, with Swap wait far above Ready in every sample.
- What to do: keep the host out of memory pressure. Swapped pages stay in swap until the guest touches them, so the wait fades only as the guest reads them back (Swapped falls, Consumed rises); more vCPUs or a reservation set now do not bring the 6 GB back.

## Notes
- 2026-11-15 audit: the stem no longer gives the normalisation ("summed over the 4 vCPUs (80,000 ms is 100%)" interpreted the value); the column headers are the product's own. Old C ("the host has free memory now, so pages swapped last week can no longer slow the VM") dropped: past swapping read as harmless is tested by the pair 0025/0391 and four more questions (redundancy #38). F added (faster swap location, swap-wait Mechanism; no other question tests it); G added (Swap wait read as part of Ready; swap-wait, Meaning). Letters: A->A, B->B, C dropped, D->C, E->D, F->E, new F. The proposed unit option (7,000 ms read as a third of a sample) was not added: VM-level ms summed over vCPUs is at the two-question cap (0105/0369).

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
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
attachments:
  - 0109/erp-db-02-cpu-real-time.csv
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, C, D, F]
misconception: [B]
misconception_type: [reclamation-as-contention, same-name-other-object]
pair: "0367"
status: draft
```
