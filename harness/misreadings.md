# Level 300 misreadings

Up-front block for the agent (switch `agent_primer.rules`, off until the benchmark shows a gain). Each line is a reading that public Internet text teaches, corrected in one sentence, with the knowledge file that holds the mechanism. Not knowledge: not indexed, so search never returns this summary instead of the file. Built by `harness/primer.py`. Author to review.

## Misreadings
- A VM is a virtual motherboard; the Guest OS is a separate layer. A counter belongs to the layer that produces it, not to the object that stores it. See `vsphere/foundations/vm-vs-guest-os`.
- The same label on another object is another metric: VM CPU Usage and ESXi CPU Usage differ in formula and meaning. Check the `same_name` links before answering. See `vsphere/technology/cpu/metrics/virtual-motherboard/usage`.
- Saturation is not contention. High utilization is not a performance problem; contention is (Ready, Co-stop, memory latency, disk latency, dropped packets). See `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`.
- Provider and consumer see different things. ESXi supplies, the VM consumes; Ready applies to the VM, never to ESXi. See `vsphere/foundations/provider-consumer`.
- CPU Latency is not always a problem: lower frequency raises it without any wait. Memory Latency and Disk Latency do mean the VM waits. See `vsphere/technology/cpu/metrics/virtual-motherboard/latency`.
- Hyper-Threading and frequency move Used and Usage; Run is time only. Used far below Run is not a reason to add vCPUs. See `vsphere/technology/cpu/troubleshooting/run-vs-used-gap`.
- Ballooned, Zipped, Swapped are past tense. Above 0 does not mean pressure now; memory contention decides. See `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`.
- Consumed stays high once pages are touched; it is not demand. Size a Guest OS from Guest OS counters. See `operations-management/capacity/rightsizing`.
- A CPU summation counter is milliseconds per sample. Convert it with the sample interval and the vCPU count. See `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.
- A threshold holds only for its object, its source and its sample interval. A 5-minute average hides 20-second peaks. See `vsphere/tools/vcf-operations/peak-20-second-metrics`.
- Admission control counts reservations, not usage. A host at low usage can refuse a power-on. See `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`.
- Contention on one host while the others are idle points to a DRS blocker; on every host, to cluster capacity or shares. See `vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster`.
