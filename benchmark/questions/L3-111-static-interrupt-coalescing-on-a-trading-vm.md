# Static interrupt coalescing on a trading VM

## Prompt
- VM mkt-gw-02 runs Linux with 8 vCPUs and one VMXNET3 adapter. It relays market data and orders, about 6,000 packets per second each way during trading hours.
- Since it moved from a physical server, the application team measures 1 to 3 ms more round-trip time to the exchange gateway.
- Same hours, vCenter: VM CPU Ready below 0.5% per vCPU, no dropped packets on the adapter, host CPU Utilization about 40%.
- The VM's advanced configuration holds `ethernet0.coalescingScheme = "static"` and `ethernet0.coalescingParams = "64"`, set two years ago to lower CPU use.
- The team wants to change the setting before tomorrow's market open.

Which statements are correct?

- A. Here ESX holds up to 64 packets before it interrupts the VM or transmits, for at most 4 ms.
- B. Coalescing delays are microseconds, so the setting cannot account for 1 to 3 ms of extra delay.
- C. The `disabled` scheme typically lowers latency, at the cost of more interrupts and CPU use.
- D. Under the static scheme, a larger queue size lowers latency, as the VM is interrupted sooner.
- E. A new value takes effect after the VM restarts or the adapter is disconnected and reconnected.
- F. Removing both entries restores the rate-based default of 4,000 interrupts per second.
- G. Coalescing should be turned off on every VM of the host, since all it does is add latency.
- H. The static scheme batches only received packets; packets the VM sends leave at once.
- I. The adaptive scheme raises the interrupt rate when the host is busy, to keep latency low under load.

## Answers
A, C, E, F

## Explanation
- A is correct: the static scheme queues a set number of packets (1 to 64, here 64) before it interrupts the VM or transmits, and ESX waits no longer than 4 ms. Other events, such as the VM going idle, can trigger the interrupt earlier.
- B is wrong: the misconception. Coalescing can add from a few hundred microseconds to a few milliseconds of network latency, depending on the workload.
- C is correct: with coalescing disabled, the VM gets more interrupts and uses more CPU, and network latency is typically lower. Workloads with a low packet rate or few active threads are the ones that might gain.
- D is wrong: a larger queue makes ESX wait for more packets before the interrupt; it reduces context switches and CPU use, not latency.
- E is correct: a coalescing change applies after a VM restart or a disconnect and reconnect of the vNIC, not live; plan it before the open.
- F is correct: the rate-based scheme is the default when `coalescingScheme` is absent, and its default rate is 4,000 interrupts per second.
- G is wrong: the over-correction. Many workloads are not affected by the added latency, coalescing saves CPU so more VMs fit on a host, and workloads with many outstanding network requests can lose performance with it disabled.
- H is wrong: the static scheme queues packets before interrupting the VM or before transmitting; both directions are batched.
- I is wrong: the adaptive scheme lowers the interrupt rate at high load and raises it at low load.
- Misconception: "Coalescing costs microseconds, it cannot be our milliseconds" (B). Or the opposite rule of thumb: "coalescing only adds latency, turn it off everywhere" (G).

## Metadata
```yaml
id: "0459"
title: "Static interrupt coalescing on a trading VM"
product: [vsphere]
technology: [network]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/cpu/configuration/latency-sensitivity
knowledge_main: vsphere/technology/network/configuration/rss-and-interrupt-coalescing
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/network/configuration/rss-and-interrupt-coalescing"
misconception: [B, G]
misconception_type: []
status: draft
```
