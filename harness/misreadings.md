# Level 300 misreadings

Up-front block for the agent (switch `agent_primer.rules`, off until the benchmark shows a gain). Each line is a correction to what public Internet text misteaches. It documents the correct understanding. Not knowledge: not indexed, so search never returns this summary instead of the file. Built by `harness/primer.py`.

## Misreadings Correction

- A VM is just the virtual motherboard layer. A VM does not include the Guest OS running above the motherboard. Guest OS is a separate layer. A counter belongs to the layer that produces it, not to the object that stores it. See `vsphere/architecture/vm-vs-guest-os`.
- Metrics with identical name, but on different objects, may not have the same meaning. For example, Linux CPU Usage, VM CPU Usage and ESXi CPU Usage differ in formula and meaning. Check the `same_name` links before answering. See `vsphere/technology/cpu/metrics/virtual-motherboard/usage`.
- ESXi CPU Utilization is the metric for ESXi capacity, not ESXi Core Utilization, nor ESXi CPU Usage.
- Saturation is simply high utilization. It is not a peer to utilization. High Utilization may lead to contention but not always, so saturation and contention are 2 different metrics. Performance problem only happens when contention happens. See `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`.
- Provider and consumer see from different perspective. ESXi supplies, the VM consumes; CPU Ready applies to the VM, never to ESXi. The values at provider is just an aggregation of its consumers. See `vsphere/architecture/provider-consumer`.
- CPU Latency is not always a problem: lower frequency raises it without any actual contention. Memory Latency and Disk Latency do mean the VM waits. See `vsphere/technology/cpu/metrics/virtual-motherboard/latency`.
- High CPU Used or Usage but low CPU Run is not a reason to add vCPUs. See `vsphere/technology/cpu/troubleshooting/run-vs-used-gap`.
- Memory is a cache: high Consumed is normal and is not demand; Active is not a capacity counter.
- Ballooned, Zipped, Swapped are past tense. Above 0 does not mean pressure now; memory contention decides. See `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`.
- Consumed stays high once pages are touched; it is not demand. Size a Guest OS from Guest OS counters. See `sp5-framework/capacity/rightsizing`.
- A CPU summation counter is milliseconds per sample. Convert it with the sample interval and the vCPU count. See `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.
- A threshold holds only for its object, its level within the object, and its sample interval. A 5-minute average hides 20-second peaks. See `vcf-operations/features/peak-20-second-metrics`.
- vSphere Cluster Admission control counts reservations, not usage. A host at low usage can refuse a power-on. See `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`.
- CPU overcommit ratios are per thread, not per core. A vCPU runs on a physical thread; 4:1 per thread is 8:1 per core.
