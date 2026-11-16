# Which object owns CPU Ready

## Prompt
- The vSphere Client shows a CPU Ready counter on a VM and on an ESXi host.

Which statements about CPU Ready on these objects are correct?

- A. On the VM, Ready counts time a vCPU wanted to run and had no physical thread to run on.
- B. On the ESXi host, Ready counts time the host waits for its own physical cores.
- C. The ESXi host's Ready value is measured on its own, apart from the Ready of its VMs.
- D. The Guest OS accounts Ready as time its processes wait for a free vCPU.

## Answers
A

## Explanation
- A is correct: Ready applies to a consumer: a vCPU of a VM that wants to run and has no physical thread to run on.
- B is wrong: a physical core or thread is always ready, so the host has no Ready of its own. The host-level value is a sum of its VMs' Ready.
- C is wrong: the ESXi Ready counter is an aggregate: it sums the Ready of the VMs on the host, so it rises and falls with them.
- D is wrong: Ready is counted by the ESXi scheduler per vCPU of the VM. The Guest OS does not account it (for the guest it is frozen time); a guest process waiting for a vCPU shows in the guest's run queue.
- Misconception: B: reading the host-level Ready as the host waiting. Or C: reading it as a measurement of its own, not of its VMs.

## Notes
- Revised 2026-11-12: the stem no longer gives the answer away ("a consumer waiting"); option D replaces the cluster, which has no Ready counter in the vSphere Client.
- 2026-11-16 re-review: singular stem ("On which object ...") made plural; the options are now four separate statements (C was "A and B": now the host value as a sum of its VMs, provider-consumer, CPU Ready on ESXi). Key unchanged.
- 2026-11-15 audit: D ("Neither: Ready is a DRS value of the cluster", a throwaway) replaced by the Guest OS, a layer a Level 100 reader can take for the owner of the wait.

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
source_path: "Synthetic, 2026-11-05; revised 2026-11-12"
misconception: [B, C]
misconception_type: [provider-vs-consumer]
status: draft
```
