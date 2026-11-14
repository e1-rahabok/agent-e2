# GPU memory used on a host with idle AI VMs

## Prompt
- An ESXi 9.1 host has 2 NVIDIA GPUs and runs 6 VMs with vGPU profiles.
- vSphere Client, host performance chart, GPU group, Real-time (last hour): GPU 0 Memory used about 94%, GPU 1 about 88%; Compute usage below 5% on both.
- The data science team says their notebooks have been idle all day.
- The platform team wants to buy more GPUs because "GPU memory is almost full".

Which statements are correct?

- A. Memory used at 88-94% shows that the notebooks fill the GPUs with work.
- B. The host chart's Memory used is the frame buffer allocated to the vGPU profiles of the powered-on VMs.
- C. NVIDIA allocates a profile's whole frame buffer when the VM powers on.
- D. NVIDIA vGPU never overcommits the frame buffer.
- E. On vSphere 9.1, the cluster counter gpu.mem.used counts the frame buffer that the workloads use.
- F. A vGPU's frame buffer sits on one physical GPU; it never spans two.
- G. When the cluster's free GPU memory exceeds a profile's size, a VM with that profile is sure to power on.
- H. A 1-week chart of these per-GPU host counters at the default statistics level would show the same lines.
- I. The memory of a GPU given to a VM by DirectPath I/O passthrough is counted in the cluster's gpu.mem.reserved.
- J. With compute below 5%, these GPUs have room for another vGPU VM.
- K. Buy more GPUs now: these workloads have outgrown the two GPUs.

## Likely wrong answer
- A: "GPU memory is at 90%, the GPUs are full of work: we need more GPUs."

## Expected key points
- Answer: B, C, D, E, F.
- A is false: the per-device Memory used is allocation, not workload use; with compute below 5% the workloads are idle.
- B is true: the host per-device counter shows the frame buffer allocated to vGPUs, so a host can show high GPU memory while its VMs are idle.
- C is true: NVIDIA allocates the profile's whole frame buffer on the physical GPU at power-on and frees it at power-off (Broadcom KB 439680), so it stays high while the VMs idle.
- D is true: frame buffer is never overcommitted with NVIDIA vGPU; only compute is time-sliced, so low compute frees no GPU memory.
- E is true: at cluster and resource pool level vCenter reports gpu.mem.reserved (memory consumed by virtual GPUs) and gpu.mem.used (memory used by workloads); on 9.0 and 9.1 used is at or below reserved.
- F is true: a vGPU never spans two physical GPUs; placement needs one GPU with a contiguous free frame buffer of the profile size.
- G is false: placement is per physical GPU and per profile; four GPUs with 8 GB free each cannot place a 16 GB profile (Broadcom KB 312021).
- H is false: the per-device host GPU counters are statistics level 4; at the default level 1 vCenter keeps no history for them. Use the cluster or resource pool GPU counters, which are level 1.
- I is false: a passthrough GPU bypasses the NVIDIA vGPU Manager, so the host does not count its memory; read it inside the guest with nvidia-smi.
- J is false: the frame buffer is allocated whole at power-on and never overcommitted; only compute is shared, so idle compute frees no frame buffer. This is the over-correction of A.
- K is false: the workloads are idle; the frame buffer is held by the profiles of the powered-on VMs, not by work. Whether another vGPU VM fits is a placement question per GPU and per profile, not this percentage.

## Notes
- Sources: the knowledge base (GPU monitoring); Broadcom KB 439680 (the profile's frame buffer is allocated at power-on and freed at power-off).
- Replaces the retired URL question 0091 at Level 200, judged (2026-11-12).
- Prompt sharpened: the chart is Real-time (last hour), because the per-device host GPU counters are level 4 and have no 24-hour history at the default statistics level.
- Dropped from the key: nvidia-smi inside a vGPU guest as a second way to read workload use; the knowledge base names nvidia-smi only for passthrough GPUs.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one fact per option (A, C, D, E); F stated as the placement fact instead of next to its negation G; J the over-correction and K the wrong action added. Key unchanged: B, C, D, E, F.

## Metadata
```yaml
id: "0273"
title: "GPU memory used on a host with idle AI VMs"
product: [vsphere]
technology: [gpu, system]
task: read-metric
level: 200
answer_type: deterministic
answer: [B, C, D, E, F]
misconception: [A]
input: [text]
object: [esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/gpu/gpu-monitoring
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/gpu/gpu-monitoring
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 to replace the retired question 0091"
misconception_type: [same-name-other-object]
status: draft
```
