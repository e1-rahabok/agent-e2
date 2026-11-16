# Latency Sensitivity High with Hyperthreading on a Java service

## Prompt
- ESXi 9.1 host esx-21: 2 sockets of 24 cores, base clock 2.0 GHz, Hyper-Threading on (96 logical processors).
- pricing-api-01: a Java pricing service, 16 vCPUs, virtual hardware version 21, full memory reservation.
- Last week its Latency Sensitivity was changed from Normal to High with Hyperthreading.
- Since then the p99 response time rose from 4 ms to 7 ms.
- vCenter, host, last 24 hours: Core Utilization 40%, Utilization 30%.
- esxtop CPU panel: the 16 vcpu worlds of pricing-api-01 run on PCPUs 0-15; most of PCPUs 16-95 are idle.

Which statements are correct?

- A. The 16 vCPUs share 8 cores: vCPUs 0 and 1 on the two threads of one core, 2 and 3 on the next.
- B. Each vCPU is locked to its thread, so the scheduler cannot move it to one of the idle cores.
- C. High with Hyperthreading gives any workload more performance, because the guest sees the thread topology.
- D. Performance Best Practices advises this setting only for workloads known to use the thread topology.
- E. Setting the VM to High needs the same CPU reservation it holds now, 16 GHz on this 2.0 GHz host.
- F. Holding half as many cores costs the VM nothing as long as the rest of the host stays mostly idle.
- G. Turn Hyper-Threading off in the host's BIOS, so that each vCPU of the VM gets a whole core.
- H. Core Utilization of 40% shows that the host lacks CPU for this VM: move it to another host.
- I. A full CPU reservation guarantees the VM exclusive threads every time it powers on, on any host.

## Likely wrong answer
"High with Hyperthreading is High at half the price: the guest sees the topology and the host is mostly idle, so nothing is lost (C, F)." C and F are the misconceptions.

## Expected key points
- Answer: A, B, D.
- A is correct: High with Hyperthreading gives each vCPU exclusive access to one hyper-thread, and consecutive vCPU pairs share one core. ESX numbers the two logical processors of a core next to each other, so PCPUs 0-15 are cores 0-7.
- B is correct: locking vCPUs to specific hyper-threads can stop ESX from scheduling them on otherwise idle cores, which limits performance; here 8 cores carry 16 busy threads while most of the host idles.
- C is wrong: only the few workloads that use awareness of the hyper-threading topology benefit; for most there is no gain and possibly a loss.
- D is correct: Performance Best Practices for vSphere 9.1 recommends it only for workloads known to be aware of, and to benefit from, the topology.
- E is wrong: the reservation under High with Hyperthreading is (16 / 2) × 2.0 GHz = 16 GHz; High gives each vCPU a whole core and needs 16 × 2.0 GHz = 32 GHz.
- F is wrong: each busy vCPU shares its core with a busy sibling vCPU, so it gets less than a whole core's throughput, where High would give it the whole core; the idle cores do not help, since the vCPUs are locked to their threads.
- G is wrong: it removes Hyper-Threading for every VM on the host, which Performance Best Practices recommends keeping on; High already gives each vCPU of this VM a whole core.
- H is wrong: the host has many idle cores; the VM is held on 8 cores by its own setting.
- I is wrong: even with a full CPU reservation the VM might not get exclusive cores if no NUMA node has enough non-exclusive cores at power-on.

## Metadata
```yaml
id: "0449"
title: "Latency Sensitivity High with Hyperthreading on a Java service"
product: [vsphere]
technology: [cpu]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/technology/cpu/configuration/latency-sensitivity
  - vsphere/technology/cpu/concepts/hyper-threading
  - vsphere/object-types/esxi/configuration/bios-settings
knowledge_main: vsphere/technology/cpu/configuration/latency-sensitivity
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/cpu/configuration/latency-sensitivity (High with Hyperthreading)"
answer: [A, B, D]
misconception: [C, F]
misconception_type: [frequency-and-hyper-threading]
status: draft
```
