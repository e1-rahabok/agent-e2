# Balloon above 0: is the VM slow?

## Prompt
- In the vSphere Client, a 16 GB Linux VM shows Ballooned memory at 2 GB, flat for the last hour.
- The application owner asks for more memory because "the host is taking memory away from the VM".

Is the VM slow because of memory? What does the balloon tell you, and what do you check?

## Likely wrong answer
"Yes. Balloon above 0 means the VM is short of memory and slow: add memory to the VM."

## Expected key points
- Not necessarily: a balloon is the first sign of memory pressure on the host (now or in the past), or of a VM or resource pool limit. It is not proof that the VM waits for memory.
- The balloon driver inside the Guest OS asks Linux for 2 GB; ESXi frees the physical pages behind them for other VMs. Linux gives free or cache pages first.
- A flat balloon shows that the reclaimed amount has not changed; on its own it shows neither current pressure nor a wait.
- The wait shows in VM Memory Latency (VCF Operations: Memory Contention), swap-in and decompression: check those. Inside the guest, check paging.
- Adding memory to the VM does not stop the balloon: it follows host pressure or a VM or resource pool limit, not VM size.

## Notes
- Revised 2026-11-12: situation and the owner's claim added; key points aligned with the knowledge files.

## Metadata
```yaml
id: "0052"
title: "Balloon above 0: is the VM slow?"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 200
answer_type: judged
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/ballooned
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [reclamation-as-contention]
status: draft
```
