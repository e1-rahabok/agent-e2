# GPU memory used on a host with idle AI VMs

## Prompt
- An ESXi 9.1 host has 2 NVIDIA GPUs and runs 6 VMs with vGPU profiles.
- vSphere Client, host performance chart, GPU group, last 24 hours: GPU 0 Memory used about 94%, GPU 1 about 88%; Compute usage below 5% on both.
- The data science team says their notebooks have been idle all day.
- The platform team wants to buy more GPUs because "GPU memory is almost full".

Is the GPU memory full because of the workloads? What does this chart show, and where do you read what the workloads use?

## Likely wrong answer
"Memory used at 88-94% means the workloads fill the GPUs; buy more GPUs or move VMs off."

## Expected key points
- No: the host chart's Memory used is the frame buffer allocated to the vGPU profiles of the powered-on VMs, not memory the workloads touch.
- The frame buffer of a profile is allocated in full when the VM powers on and freed at power-off, so it stays high while the VMs are idle.
- NVIDIA vGPU never overcommits frame buffer; only compute is time-sliced. Low compute usage frees no GPU memory.
- What the workloads use: the cluster or resource pool GPU memory used counter on vSphere 9 (gpu.mem.used, at or below the reserved amount), or nvidia-smi inside the guest.
- Whether more VMs fit is a question of free frame buffer per GPU for the profile size, not of this percentage.

## Notes
- Sources: the knowledge base (GPU monitoring); Broadcom KB 439680 (the profile's frame buffer is allocated at power-on and freed at power-off).
- Replaces the retired URL question 0091 at Level 200, judged (2026-11-12).

## Metadata
```yaml
id: "0273"
title: "GPU memory used on a host with idle AI VMs"
product: [vsphere]
technology: [gpu, system]
task: read-metric
level: 200
answer_type: judged
input: [text]
object: [esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/gpu/gpu-monitoring
knowledge_main: vsphere/technology/gpu/gpu-monitoring
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 to replace the retired question 0091"
misconception_type: [same-name-other-object]
status: draft
```
