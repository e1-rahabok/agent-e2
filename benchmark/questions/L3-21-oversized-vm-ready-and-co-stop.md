# Ready and Co-stop on an oversized VM

## Prompt
- ESXi host: 2 sockets of 32 cores, Hyper-Threading on. Host Utilization about 55%.
- A database VM has 24 vCPUs. Over the last week, per vCPU at the 20-second peak: Ready 5%, Co-stop 3%, Net Run 9%.
- The other VMs on the host, all 2-4 vCPUs, show Ready below 0.5%.
- Inside the guest, at the busiest times, 3 CPUs are busy and the run queue is short.
- The owner says the VM waits for CPU and asks for 8 more vCPUs.

Which statements are correct?

- A. Reduce the VM toward what the guest uses, for example 8 vCPUs: fewer vCPUs are easier to schedule, so Ready and Co-stop fall.
- B. Add the 8 vCPUs: the work spreads over more vCPUs, so each one waits less.
- C. Co-stop of 3% shows the database threads wait on each other inside the guest.
- D. A smaller VM gets fewer shares per vCPU by default, so each vCPU waits longer under contention.
- E. The host is short of CPU: move other VMs off it first.

## Likely wrong answer
B: more vCPUs to cure a CPU wait. Or E: the host is short of CPU.

## Expected key points
- Answer: A.
- A: a VM with many vCPUs needs many threads free at about the same time; when one vCPU waits in Ready, its siblings are co-stopped to stay in step. The guest uses about 3 CPUs, so 24 is far more than it needs.
- B is wrong: more vCPUs make scheduling harder and can raise both Ready and Co-stop.
- C is wrong: Co-stop is a wait in the ESXi scheduler: a vCPU held back to stay in step with a sibling vCPU. The guest's short run queue shows its threads are not waiting.
- D is wrong: default shares are set per vCPU (1,000 per vCPU at Normal), so each vCPU keeps the same share. The VM as a whole gets fewer shares, which matters only when the host is contended.
- E is wrong: the small VMs on the same host barely wait and the host is at about 55%. The wait is the VM's own size.

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
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2)"
answer: [A]
misconception: [B, E]
misconception_type: [provider-vs-consumer]
status: draft
```
