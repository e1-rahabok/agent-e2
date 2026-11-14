# Ready and Co-stop on an oversized VM

## Prompt
- ESXi host: 2 sockets of 32 cores, Hyper-Threading on. Host Utilization about 55%.
- A database VM has 24 vCPUs. Over the last week, per vCPU at the 20-second peak: Ready 5%, Co-stop 3%, Net Run 9%.
- The other VMs on the host, all 2-4 vCPUs, show Ready below 0.5%.
- Inside the guest, at the busiest times, 3 CPUs are busy and the run queue is short.
- The owner says the VM waits for CPU and asks for 8 more vCPUs.

Which statements are correct?

- A. Reduce the VM toward what the guest uses, for example 8 vCPUs, so that Ready and Co-stop fall.
- B. Add the 8 vCPUs: a Net Run of 9% per vCPU shows the vCPUs are saturated.
- C. Co-stop of 3% shows the database threads wait on each other inside the guest.
- D. A vCPU of this VM can be co-stopped at moments when the host has a free thread for it.
- E. The host is short of CPU: move other VMs off it first.

## Likely wrong answer
B: more vCPUs to cure a CPU wait. Or E: the host is short of CPU.

## Expected key points
- Answer: A, D.
- A: a VM with many vCPUs needs many threads free at about the same time; when one vCPU waits in Ready, its siblings are co-stopped to stay in step. The guest uses about 3 CPUs, so 24 is far more than it needs.
- B is wrong: Net Run of 9% per vCPU is far from saturated, and more vCPUs make scheduling harder and can raise both Ready and Co-stop.
- C is wrong: Co-stop is a wait in the ESXi scheduler: a vCPU held back to stay in step with a sibling vCPU. The guest's short run queue shows its threads are not waiting.
- D: a co-stopped vCPU is held back because it is too far ahead of a sibling, even when physical threads are free for it.
- E is wrong: the small VMs on the same host barely wait and the host is at about 55%. The wait is the VM's own size.

## Notes
- Options rewritten 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): old D (default shares per vCPU after a downsize) removed because it repeats option G of 0236; new D tests the Co-stop mechanism; B now carries the misreading of Net Run. Key changed from A to A, D.

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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, D]
misconception: [B, E]
misconception_type: [provider-vs-consumer]
pair: "0373"
status: draft
```
