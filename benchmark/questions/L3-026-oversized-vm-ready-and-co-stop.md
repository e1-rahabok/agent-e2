# Ready and Co-stop on an oversized VM

## Prompt
- ESXi host: 2 sockets of 32 cores, Hyper-Threading on. Host Utilization about 55%.
- A database VM has 24 vCPUs. Over the last week, per vCPU at the 20-second peak: Ready 5%, Co-stop 3%, Net Run 9%.
- The other VMs on the host, all 2-4 vCPUs, show Ready below 0.5%.
- Inside the guest, at the busiest times, 3 CPUs are busy and the run queue is short.
- The owner says the VM waits for CPU and asks for 8 more vCPUs.

Which statements are correct?

- A. Cut the VM toward the guest's use, such as 8 vCPUs, then read Ready and Co-stop again.
- B. Add the 8 vCPUs: a Net Run of 9% per vCPU shows the vCPUs are saturated.
- C. Co-stop of 3% shows the database threads wait on each other inside the guest.
- D. For the guest, a vCPU in Co-stop is frozen, the same as a vCPU in Ready.
- E. Other VMs compete for the host's threads: move some off the host before touching this VM.
- F. Ready of 5% and Co-stop of 3% are too small to matter, so the VM needs no change.

## Likely wrong answer
B: more vCPUs to cure a CPU wait. Or E: the host is short of CPU.

## Expected key points
- Answer: A, D.
- A is correct: a VM with many vCPUs needs many threads free at about the same time; when one vCPU waits in Ready, its siblings are co-stopped to stay in step. Downsizing lowers both. The guest uses about 3 CPUs, so 24 is far more than it needs. The host is not contended (about 55%, other VMs below 0.5% Ready), so the case where a smaller VM on a contended host gets less than it needs per vCPU does not apply.
- B is wrong: Net Run of 9% per vCPU is far from saturated, and more vCPUs make scheduling harder and can raise both Ready and Co-stop.
- C is wrong: Co-stop is a wait in the ESXi scheduler: a vCPU held back to stay in step with a sibling vCPU. The guest's short run queue shows its threads are not waiting.
- D is correct: the effect of Co-stop on the Guest OS is the same as Ready, a freeze; the guest cannot tell which of the two caused it.
- E is wrong: the small VMs on the same host barely wait and the host is at about 55%. The wait is the VM's own size.
- F is wrong: the over-correction. Ready is read against Run (about Net Run here, since Overlap is small): 5% Ready on 9% per vCPU is a wait of more than half the run time, and Co-stop in a high-performing environment stays below 1%.

## Notes
- Options rewritten 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): old D (default shares per vCPU after a downsize) removed because it repeats option G of 0236; new D tests the Co-stop mechanism; B now carries the misreading of Net Run; F (the over-correction) added. Key changed from A to A, D.
- 2026-11-15 audit: D replaced (the old D, a co-stopped vCPU can stop while threads are free, is tested by the pair 0053/0375); the new D tests the effect of Co-stop on the guest (co-stop, Effect on the Guest OS).

## Metadata
```yaml
id: "0107"
title: "Ready and Co-stop on an oversized VM"
product: [vsphere]
technology: [cpu]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter, vcf-operations, guest-os-tools]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, D]
misconception: [B, E]
misconception_type: [provider-vs-consumer]
pair: "0373"
status: draft
```
