# Words to avoid

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). The words to avoid when writing, each with its replacement and reason. For writers and reviewers; not indexed. The dimensions behind the tags (object type, layer, technology, pillar): [metadata.md](metadata.md). Writing rules: [writing.md](writing.md). The agent's vocabulary (one entry per term: meaning, other names, the term it is confused with) is [`knowledge/glossary.md`](../../knowledge/glossary.md). Repository terms: [`project/terms.md`](../terms.md).

## Table
- When the author corrects a wording mistake, add it here. A word users also say goes into the Also called line of its entry in [`knowledge/glossary.md`](../../knowledge/glossary.md) too, so search maps it.

| Avoid | Use instead | Why |
|---|---|---|
| "A problem because it is orange" (a colour as the reason a value is a problem, or fine) | What the consumers waited for, in the metric's own unit; how broad; how long. The colour only as a label after the value | The limits set the colour from the value, so the colour restates the value and explains nothing. A KPI colour is a weighted mix: one red among greens and many yellows both read orange. |
| Warm-up (for NVMe reads on a tiered host) | Pages fetched back from NVMe when they become active | Warm-up means an application filling its cache on purpose. NVMe reads are ESXi fetching back pages the guest touches; neither the guest nor the application knows. Cold pages move to NVMe once DRAM consumed reaches about 80%, not because a quiet period passes. |
| Colour levels, colour bands, KPI levels, band values (for the numbers of a catalog line) | Limits: best, green, yellow, orange, zero-at | The five limits and the colour bands between them are one fact. A limit is where a band ends: green runs from best to the green limit. Two names made one fact read like two formats, and Cluster Risk was handled apart from the KPIs. The terms are the VCF vCommunity Adapter's. |
| Memory Latency (for the memory row of the KPIs) | Memory Wait | The memory row is Memory Contention plus NVMe wait. Memory Latency names the counter that leaves NVMe out, so a KPI row with that name hides the NVMe wait. |
| Tier 0, Tier 1 (for the memory tiers) | DRAM, NVMe | Tier-0 and Tier-1 also name NSX gateways. Keep the tier number only inside a counter or `memstats` field name. |
| ESXi Memory Consumed in DRAM (the Cluster Consumption row) | ESXi DRAM Consumed | Memory Consumed is a raw vCenter metric; its meaning is not ours to change. On a tiered host it covers DRAM and NVMe and is against both, as vSphere counts host memory. DRAM in use is a separate metric with its own name. |
| utilization above physical capacity | demand above physical capacity | Utilization measures what happens and cannot pass 100%; demand includes unmet demand. |
| Throughput for a capacity figure ("Nominal CPU Throughput" for Total Capacity (GHz)) | Total Base Capacity (GHz) | Throughput is activity, the work done; capacity is capability (Q-E2-236). |
| Claimed, for memory a VM or host holds ("VM Memory Claimed") | Consumed, or the product label | Claim reads as reclamation, the opposite (Q-E2-236). |
| A product label reworded ("vSphere's GHz total" for Total Capacity) | The label as the product shows it, then what it measures and the better name: "Total Capacity (GHz) is the capacity at base clock (Total Base Capacity); space for vCPUs is threads" | The product UI is reality: the operator reads that label. Agent E2 keeps it and corrects the model behind it (Q-E2-203). |
| "the book", "the source document" (in a knowledge file or its metadata) | Nothing: state the fact. For a vendor document, its name and version | The knowledge base is a superset of the author's material; its sources are stated once, in KNOWLEDGE-ENGINEERING.md section 2. "The source document" tells a reader nothing. |
| "the KPI" for a named score ("the KPI fell", "KPI change level") | The score's name as the page shows it: Cluster Performance (%), VM Performance (%), Cluster Risk (%); "change level" | The industry stretches KPI to mean any number. The name is exact. KPI stays the concept against SLA (glossary, KPI). |
| SLI, SLO, performance SLA | KPI | The SLA is a business contract, not an operations metric; performance is managed by the KPI only. |
| Cluster Availability as an SLA | the availability of the consumer's VMs and pods | The application team does not care about the infrastructure under its VMs and pods. |
| KPI target | KPI baseline (standard expectation) | A target is not reached yet; a KPI is what is maintained as standard. |
| code (as the actor: "code decides", "code loads") | Agent E2; name the Harness or the LLM only where the design depends on which part does the work | Code can mean the Agent or the Harness. Agent E2 is one program: LLM, Harness and Agent together. |
| demand overcommit | overcommit (of allocation) | Only allocation can be overcommitted. Demand, usage and utilization are results, not settings. |
| VM rightsizing | Guest OS sizing (internal, Guest OS counters) or VM footprint (external, vSphere counters) | Two different jobs with two formulas. Author's other book, VM Footprint and Guest OS Sizing. |
| VM metric (for a Guest OS counter such as Run Queue, Disk Queue, Processor Time) | Guest OS metric | The VM is a virtual motherboard; the Guest OS is a separate layer. Author correction. |
| virtual machine, thought of as a complete machine | virtual motherboard (VM) | A VM has no OS of its own. Author's book. |
| "uses only X% of what it needs" | "is charged X%" or "gets X% of the runtime it demands" | A vCPU is a thread in the scheduler with no intent ([writing.md](writing.md), CPU scheduling language). |
| object (for vCPU, Guest OS) | instance (vCPU), layer (Guest OS) | vCPU and Guest OS are not vSphere object types. |
| trap (for a wrong belief or wrong reading) | misconception | In IT infrastructure a trap is an event notification (SNMP trap, a log message an alert traps) or, in CPU virtualization, a hand-over to the hypervisor (trap-and-emulate). Agent E2 does not set traps for other models; it knows the mechanism. |
| misreading (for the up-front list) | misconception | One concept, one word: the up-front lines are misconceptions promoted from their files. |
| kind (as a field name) | retriever_guide | "kind" does not say what the field is for. |
| Planning parameter (for a metric Agent E2 computes) | metric | A value Agent E2 computes is a metric like any other and needs no other name. Its name and its unit are separate parts ([`sp5-framework/observability/naming-patterns`](../../knowledge/sp5-framework/observability/naming-patterns.md), section Six parts of a metric). |
| Utilization (ESXi CPU, when threads are meant) | Thread Utilization | Plain "Utilization" is easily confused with Core Utilization. Author correction, Q-E2-008. |
| Peak CPU Queue (the VCF Operations metric) | Peak vCPU Queue: Guest\|Peak vCPU Queue within collection cycle | The value is per vCPU. CPU and vCPU differ by the whole vCPU count on a large VM. Author correction (Q-E2-232). |
| architecture (for settings) | configuration | Architecture means the big picture, not individual settings. |
| interpretation (as a folder) | troubleshooting | Interpretation is the purpose of every metric file. |
| foundations (as a folder) | a name for what the folder holds: observability, architecture | The content was neither basic (Level 100-200) nor lower stack; the word said nothing. |
| triage (for a troubleshooting flow) | flow, troubleshooting flow | A troubleshooting file is a flow; one word. |
| diagnosis, diagnose | troubleshooting | Diagnosis is a medical word for one step of troubleshooting; one word for the why. |
| what to monitor | health check | Lazy term: what is monitored is health; the health check gives order and verdict. |
| verification (of an object's state) | health check | A third word for the same thing. |
| KPI (for capacity, risk, availability) | model | KPI is strictly performance: the P in KPI. Capacity, risk, availability and security are models. |
| Imbalance (for vCPU usage) | Usage Disparity | Imbalance implies the vCPUs should be balanced. |
| guest physical memory, guest physical page, machine page, machine memory | VM pages, ESXi pages | Only ESXi manages physical memory. Keep the vendor term once in parentheses for retrieval. |
