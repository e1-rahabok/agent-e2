# Level 300 misconceptions

The misconceptions with the widest reach, given to the agent before every question (up-front block `rules`, switch `agent_primer.rules`, off until the benchmark shows a gain). Built by `harness/primer.py`. Not indexed (`harness/kb.py`, `NOT_INDEXED`), so search never returns this summary instead of the file.

What belongs here:
- A misconception a frontier model applies with confidence, so it never looks it up: what is a problem, which metric decides, what to add or size by. Level 300: a VMware administrator who knows the basics still holds it.
- Promoted from a file: each line is also a misconception in the `## Misconceptions` section of the file it names, where the mechanism and the user's own words live. This list only makes sure the correction is in place before the model reasons.
- Chosen by reach: a misconception that changes the verdict on many questions (layer, provider and consumer, utilization vs contention, memory as cache), not one that matters for a single counter.
- Not a definition, and not two terms swapped: those are entries of `knowledge/glossary.md` (Not to confuse with).
- One line: the correct understanding, then `See` the file that holds the mechanism.

## Corrections

- A VM is just the virtual motherboard layer. A VM does not include the Guest OS running above the motherboard. Guest OS is a separate layer. A counter belongs to the layer that produces it, not to the object that stores it. See `vsphere/architecture/vm-vs-guest-os`.
- Metrics with identical name, but on different objects, may not have the same meaning. For example, Linux CPU Usage, VM CPU Usage and ESXi CPU Usage differ in formula and meaning. Check the `same_name` links before answering. See `vsphere/technology/cpu/metrics/virtual-motherboard/usage`.
- ESXi CPU Utilization, read per thread, is the metric for ESXi capacity, not ESXi Core Utilization, nor ESXi CPU Usage. See `vsphere/technology/cpu/metrics/host/utilization`.
- Saturation is simply high utilization. It is not a peer to utilization. High utilization may lead to contention but not always, so saturation and contention are two different metrics. A performance problem happens only when contention happens. See `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`.
- Provider and consumer see from different perspectives. ESXi supplies, the VM consumes; CPU Ready applies to the VM, never to ESXi. A value at the provider is just an aggregate of its consumers. See `vsphere/architecture/provider-consumer`.
- CPU Latency is not always a problem: lower frequency raises it without any actual contention. Memory Latency and Disk Latency do mean the VM waits. See `vsphere/technology/cpu/metrics/virtual-motherboard/latency`.
- High CPU Used or Usage but low CPU Run is not a reason to add vCPUs. See `vsphere/technology/cpu/troubleshooting/run-vs-used-gap`.
- Memory is a cache: Consumed stays high once pages are touched; that is normal and is not demand. Active is not a capacity counter. Size a Guest OS from Guest OS counters. See `sp5-framework/capacity/rightsizing`.
- Ballooned, Zipped, Swapped are past tense. Above 0 does not mean pressure now; memory contention decides. See `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`.
- A threshold holds only for its object, its level within the object, and its sample interval. A 5-minute average hides 20-second peaks. See `vcf-operations/features/peak-20-second-metrics`.
- vSphere Cluster Admission control counts reservations, not usage. A host at low usage can refuse a power-on. See `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`.
- CPU overcommit ratios are per thread, not per core. A vCPU runs on a physical thread; 3:1 per thread is 6:1 per core. See `sp5-framework/capacity/class-of-service-planning`.
