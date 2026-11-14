# Words to avoid

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). The words to avoid when writing, each with its replacement and reason. For writers and reviewers; not indexed. The dimensions behind the tags (object type, layer, technology, pillar): [metadata.md](metadata.md). Writing rules: [writing.md](writing.md). The agent's vocabulary (one entry per term: meaning, other names, the term it is confused with) is [`knowledge/glossary.md`](../../knowledge/glossary.md). Repository terms: [`project/terms.md`](../terms.md).

## Table
When the author corrects a wording mistake, add it here. A word users also say goes into the Also called line of its entry in [`knowledge/glossary.md`](../../knowledge/glossary.md) too, so search maps it.

| Avoid | Use instead | Why |
|---|---|---|
| utilization above physical capacity | demand above physical capacity | Utilization measures what happens and cannot pass 100%; demand includes unmet demand. |
| A product label reworded ("vSphere's GHz total" for Total Capacity) | The label as the product shows it, then what it measures and the better name: "Total Capacity (GHz) is throughput at base clock; capacity is threads" | The product UI is reality: the operator reads that label. Agent E2 keeps it and corrects the model behind it (author, 2026-11-14, Q203). |
| SLI, SLO, performance SLA | KPI | The SLA is a business contract, not an operations metric; performance is managed by the KPI only (author, 2026-11-11). |
| Cluster Availability as an SLA | the availability of the consumer's VMs and pods | The application team does not care about the infrastructure under its VMs and pods (author, 2026-11-11). |
| KPI target | KPI baseline (standard expectation) | A target is not reached yet; a KPI is what is maintained as standard. |
| code (as the actor: "code decides", "code loads") | Agent E2; name the Harness or the LLM only where the design depends on which part does the work | Code can mean the Agent or the Harness. Agent E2 is one program: LLM, Harness and Agent together. |
| demand overcommit | overcommit (of allocation) | Only allocation can be overcommitted. Demand, usage and utilization are results, not settings. |
| VM rightsizing | Guest OS sizing (internal, Guest OS counters) or VM footprint (external, vSphere counters) | Two different jobs with two formulas. Author's other book, VM Footprint and Guest OS Sizing. |
| VM metric (for a Guest OS counter such as Run Queue, Disk Queue, Processor Time) | Guest OS metric | The VM is a virtual motherboard; the Guest OS is a separate layer. Author correction, 2026-11-03. |
| virtual machine, thought of as a complete machine | virtual motherboard (VM) | A VM has no OS of its own. Author's book. |
| "uses only X% of what it needs" | "is charged X%" or "gets X% of the runtime it demands" | A vCPU is a thread in the scheduler with no intent ([writing.md](writing.md), CPU scheduling language). |
| object (for vCPU, Guest OS) | instance (vCPU), layer (Guest OS) | vCPU and Guest OS are not vSphere object types. |
| trap (for a wrong belief or wrong reading) | misconception | In IT infrastructure a trap is an event notification (SNMP trap, a log message an alert traps) or, in CPU virtualization, a hand-over to the hypervisor (trap-and-emulate). Agent E2 does not set traps for other models; it knows the mechanism (author, 2026-11-11). |
| misreading (for the up-front list) | misconception | One concept, one word: the up-front lines are misconceptions promoted from their files. |
| kind (as a field name) | retriever_guide | "kind" does not say what the field is for. |
| Utilization (ESXi CPU, when threads are meant) | Thread Utilization | Plain "Utilization" is easily confused with Core Utilization. Author correction, Q008. |
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
