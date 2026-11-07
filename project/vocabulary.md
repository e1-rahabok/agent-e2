# Writing vocabulary

How the knowledge files are written: the dimensions not to mix, and the words to avoid when writing. For writers and lint, not for Agent E2; not indexed. The agent's vocabulary (synonyms, defined terms, confusable pairs) is `knowledge/glossary.md`. Repository terms: `project/terms.md`.

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
- Metric: a measured value with name, unit and formula, for one object type. Counter: the raw source counter (`cpu.ready.summation`); a metric may use several. Property: a configuration or inventory attribute, not measured over time.
- Trap: a wrong conclusion from a true observation. Format: `KNOWLEDGE-ENGINEERING.md`, section 4.
- Level 400: mechanism, where the reading misleads, what to check instead. Level 300: a metric and a common threshold at face value.
- Thread (physical): a hardware thread, a provider. Thread (software): an OS thread, a consumer.

## Words to avoid
When the author corrects a wording mistake, add it here. A word users also say goes into the Synonyms table of `knowledge/glossary.md` too, so search maps it.

| Avoid | Use instead | Why |
|---|---|---|
| utilization above physical capacity | demand above physical capacity | Utilization measures what happens and cannot pass 100%; demand includes unmet demand (author, Q067). |
| KPI target | KPI baseline (standard expectation) | A target is not reached yet; a KPI is what is maintained as standard (author, Q067). |
| demand overcommit | overcommit (of allocation) | Only allocation can be overcommitted. Demand, usage and utilization are results, not settings (author, Q069). |
| VM rightsizing | Guest OS sizing (internal, Guest OS counters) or VM footprint (external, vSphere counters) | Two different jobs with two formulas. Author's other book, VM Footprint and Guest OS Sizing. |
| VM metric (for a Guest OS counter such as Run Queue, Disk Queue, Processor Time) | Guest OS metric | The VM is a virtual motherboard; the Guest OS is a separate layer. Author correction, 2026-11-03. |
| virtual machine, thought of as a complete machine | virtual motherboard (VM) | A VM has no OS of its own. Author's book. |
| need, want, wish (for a vCPU or VM) | demands runtime; the kernel decides how much it gets | A vCPU is a thread in the scheduler. It has no intent. |
| "uses only X% of what it needs" | "is charged X%" or "gets X% of the runtime it demands" | Same reason. |
| object (for vCPU, Guest OS) | instance (vCPU), layer (Guest OS) | vCPU and Guest OS are not vSphere object types. |
| kind (as a field name) | retriever_guide | "kind" does not say what the field is for. |
| Utilization (ESXi CPU, when threads are meant) | Thread Utilization | Plain "Utilization" is easily confused with Core Utilization. Author correction, Q008. |
| architecture (for settings) | configuration | Architecture means the big picture, not individual settings. |
| interpretation (as a folder) | diagnosis | Interpretation is the purpose of every metric file. |
| Imbalance (for vCPU usage) | Usage Disparity | Imbalance implies the vCPUs should be balanced. |
| guest physical memory, guest physical page, machine page, machine memory | VM pages, ESXi pages | Only ESXi manages physical memory. Keep the vendor term once in parentheses for retrieval. |
