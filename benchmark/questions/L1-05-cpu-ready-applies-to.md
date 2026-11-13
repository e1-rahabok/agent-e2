# Which object owns CPU Ready

## Prompt
- The vSphere Client shows a CPU Ready counter on a VM and on an ESXi host.

On which object does Ready measure that object's own wait for a physical CPU?

- A. The VM: a vCPU waits for a physical thread.
- B. The ESXi host: the host waits for its physical cores.
- C. Both: each object waits for its own CPU.
- D. Neither: Ready is a DRS value of the cluster.

## Likely wrong answer
B or C: reading the host-level Ready as the host waiting.

## Expected key points
- Answer: A.
- Ready applies to a consumer: a vCPU of a VM that wants to run and has no physical thread to run on.
- A physical core or thread is always ready, so the host has no Ready of its own. The host-level value is a sum of its VMs' Ready.
- D is wrong: Ready is measured by the ESXi scheduler per vCPU, not by DRS.

## Notes
- Revised 2026-11-12: the stem no longer gives the answer away ("a consumer waiting"); option D replaces the cluster, which has no Ready counter in the vSphere Client.

## Metadata
```yaml
id: "0036"
title: "Which object owns CPU Ready"
product: [vsphere]
technology: [system, cpu]
task: read-metric
level: 100
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/architecture/provider-consumer
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6); revised 2026-11-12"
answer: [A]
misconception: [B, C]
misconception_type: [provider-vs-consumer]
status: draft
```
