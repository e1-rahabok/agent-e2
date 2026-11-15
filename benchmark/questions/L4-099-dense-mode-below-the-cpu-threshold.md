# Dense mode below the CPU threshold

## Prompt
- A cluster of five ESX 9.1 hosts. Each host has 2 sockets with 8 cores each: 16 cores and 32 logical processors (Hyper-Threading on).
- On hosts 1, 2, 3 and 5 an administrator set the advanced option /Net/NetTuneHostMode to "dense" last month, to raise the consolidation ratio. Host 4 stays at the default value of the option. DRS is fully automated.
- State at 14:00 today, read from the vSphere Client:

| Host | /Net/NetTuneHostMode | Powered-on VMs | vCPUs of those VMs | Host CPU utilization |
|---|---|---|---|---|
| Host 1 | dense | 44 | 130 | 62% |
| Host 2 | dense | 70 | 180 | 49% |
| Host 3 | dense | 9 | 100 | 85% |
| Host 4 | default | 50 | 140 | 78% |
| Host 5 | dense | 36 | 140 | 51% |

- The VMs on hosts 1 to 5 use VMXNET3 adapters. All VMs run normal business workloads, and Net.NetSplitRxMode is at its default on every host.

On which hosts does ESX implement the dense mode optimizations at 14:00?

- A. Host 1 only.
- B. Host 1 and host 5.
- C. Host 1, host 3 and host 5.
- D. Host 1, host 3, host 4 and host 5.
- E. Host 1, host 4 and host 5.

## Likely wrong answer
D or E: the option /Net/NetTuneHostMode is read as the switch, or high CPU utilization alone is read as enough. Or C: the number of VMs is not checked.

## Expected key points
- Answer: B.
- Dense mode (host-wide performance tuning) makes ESX watch three values: the number of VMs, the number of vCPUs and the total CPU utilization. The optimizations (more aggressive batching of network packets) are implemented only while all three exceed their thresholds: numVMs >= numPCPUs, numvCPUs >= 2 x numPCPUs, and CPUUtil >= 50%. Setting the option makes the host eligible; it does not start the optimizations.
- Host 1: 44 VMs and 130 vCPUs pass both ratios whether numPCPUs is read as 16 cores or 32 logical processors (44 >= 32; 130 >= 64), and 62% is above 50%. The optimizations are implemented.
- Host 5: 36 VMs (>= 32), 140 vCPUs (>= 64) and 51% utilization pass. The optimizations are implemented.
- Host 2 fails only on utilization (49% is below 50%, although 70 VMs and 180 vCPUs pass). Host 3 has the highest utilization of the dense hosts (85%) and enough vCPUs, but only 9 VMs, below 16 on either reading: a few large VMs are not a high consolidation ratio. Host 4 meets all three thresholds with its numbers but is not set to dense, so nothing is implemented.
- The vendor note: even with dense mode activated, the optimizations run only when the consolidation ratio and the CPU utilization reach the thresholds. The vendor also warns that batching raises the latency of individual requests, and that at low CPU utilization or with VMs that take a disproportionate share of network throughput, dense mode can lower system-wide throughput; it recommends dense mode only on hosts where the trade-off pays.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "Host-Wide Performance Tuning" (page 54), including the NOTE after the setting values. https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices (read 2026-11-13 from the saved PDF, revision 20260624).
- Why one answer: the document gives the three conditions with their numbers and the note that the setting alone does not start the optimizations. The table decides each host by arithmetic.
- Debatable risk: the document does not define numPCPUs (cores or logical processors). Every host is built so that the result is the same on both readings (see the key). The condition CPUUtil >= 50% is the vendor's; host 5 at 51% and host 2 at 49% avoid a dispute about rounding or the exact equality. The document does not say how the host CPU utilization is measured, so the prompt gives one number per host.
- Rewritten 2026-11-13 to raise difficulty: from one host to a five-host table where the three thresholds, the option value and the VM-count condition each exclude a different host; the exact thresholds are not known without the vendor document.

## Metadata
```yaml
id: "0294"
title: Dense mode below the CPU threshold
product: [vsphere]
technology: [cpu, network]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [esxi, cluster]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/configuration/host-wide-dense-mode
knowledge_main: vsphere/technology/cpu/configuration/host-wide-dense-mode
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [D, E]
misconception_type: []
status: draft
```
