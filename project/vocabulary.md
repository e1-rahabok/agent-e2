# Writing vocabulary

How the knowledge files are written: the dimensions not to mix, and the words to avoid when writing. For writers and lint, not for Agent E2; not indexed. The agent's vocabulary (one entry per term: meaning, other names, the term it is confused with) is `knowledge/glossary.md`. Repository terms: `project/terms.md`.

## Dimensions (do not mix)
- Object type: a kind of managed object (VirtualMachine, HostSystem). Not a component inside an object (vCPU, vmnic).
- Object: one named instance of an object type ("db01"). Not a metric or a layer.
- Instance (metric): a sub-component a metric is reported for (vCPU 0, vmnic1, vmhba0). Tag `instance`. Not an object type.
- Layer: a level of the stack: guest-os, virtual-motherboard, hypervisor, physical. Guest OS is a layer, not an object type.
- Vantage point: the layer or object a metric is observed from (consumer VM vs provider ESXi). Expressed through `object` and `layer`.
- Perspective (book): technology, pillar of operations, product. Not a layer.
- Technology: cpu, gpu, memory, storage, network, system (the box as a whole). Not a product.
- Pillar: availability, performance, security, capacity, value. Not a technology.
- Metric class: contention, consumption, context. Not a pillar.
- Metric: a measured value with name, unit and formula, for one object type. Counter: the raw source counter (`cpu.ready.summation`); a metric may use several. Property: an attribute set by configuration or capability (configured hosts, maximum VMs), not produced at an interval. A count of inventory (VMs in a cluster) and a state (power state) are metrics: `knowledge/foundations/input-types`.
- Misconception: a wrong conclusion from a true observation or a public rule of thumb, held with confidence at Level 300, with the mechanism that corrects it. One concept, two homes: `## Misconceptions` in the file, and the widest-reaching ones up front in `knowledge/misconceptions.md`. `KNOWLEDGE-ENGINEERING.md`, section 4.
- Level 400: mechanism, where the reading misleads, what to check instead. Level 300: a metric and a common threshold at face value.
- Thread (physical): a hardware thread, a provider. Thread (software): an OS thread, a consumer.

## Words to avoid
When the author corrects a wording mistake, add it here. A word users also say goes into the Also called line of its entry in `knowledge/glossary.md` too, so search maps it.

| Avoid | Use instead | Why |
|---|---|---|
| utilization above physical capacity | demand above physical capacity | Utilization measures what happens and cannot pass 100%; demand includes unmet demand. |
| SLI, SLO, performance SLA | KPI | The SLA is a business contract, not an operations metric; performance is managed by the KPI only (author, 2026-11-11). |
| Cluster Availability as an SLA | the availability of the consumer's VMs and pods | The application team does not care about the infrastructure under its VMs and pods (author, 2026-11-11). |
| KPI target | KPI baseline (standard expectation) | A target is not reached yet; a KPI is what is maintained as standard. |
| code (as the actor: "code decides", "code loads") | Agent E2; name the Harness or the LLM only where the design depends on which part does the work | Code can mean the Agent or the Harness. Agent E2 is one program: LLM, Harness and Agent together. |
| demand overcommit | overcommit (of allocation) | Only allocation can be overcommitted. Demand, usage and utilization are results, not settings. |
| VM rightsizing | Guest OS sizing (internal, Guest OS counters) or VM footprint (external, vSphere counters) | Two different jobs with two formulas. Author's other book, VM Footprint and Guest OS Sizing. |
| VM metric (for a Guest OS counter such as Run Queue, Disk Queue, Processor Time) | Guest OS metric | The VM is a virtual motherboard; the Guest OS is a separate layer. Author correction, 2026-11-03. |
| virtual machine, thought of as a complete machine | virtual motherboard (VM) | A VM has no OS of its own. Author's book. |
| need, want, wish (for a vCPU or VM) | demands runtime; the kernel decides how much it gets | A vCPU is a thread in the scheduler. It has no intent. |
| "uses only X% of what it needs" | "is charged X%" or "gets X% of the runtime it demands" | Same reason. |
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
