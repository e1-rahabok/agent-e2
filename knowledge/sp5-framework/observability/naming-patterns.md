# Naming patterns

A metric name does not reliably tell what the metric measures.
Two metrics can share a name and differ. Two names can mean the same thing.
The patterns below classify the ways names mislead.

## Six parts of a metric
A metric in VCF Operations has six parts. Keep them apart: the patterns below come from reading one part as another.

| Part | What it is | Example (Cluster CPU Overcommit Ratio) |
|---|---|---|
| Group | Where the metric belongs | Cluster Risk, Allocation |
| Name | The text shown to the user. It is translated (internationalization), so the same metric reads differently per language | CPU Overcommit Ratio |
| Key | What the API uses. Typically English only, and the same in every language | the key in the pack's adapter; a native example: `cpu\|usage_average` (VM CPU Usage) |
| Unit | One of the finite set of units VCF Operations defines. Use only those; never make one up. The UI shows it in brackets after the name | number |
| Value | The number | 1.66 |
| Description | One line saying what the metric measures | The sum of the vCPUs of all running VMs divided by the usable physical threads of the cluster |

- What a ratio divides by belongs in the description, not in the unit or the name. A ratio's unit is number.
- Match a metric on its key, not its name: the name changes with the language.

## Pattern catalogue

| Pattern | Meaning |
|---|---|
| same-object-same-metric-different-name | One measurement, two labels, on the same object. |
| same-name-same-object-different-formula | Same name, same object type, but the formula depends on the level inside the object where it is measured. |
| same-name-same-purpose-different-formula | Same name and purpose on different object types, but different formula per object. |
| same-name-different-meaning | Identical name, different meaning. Misinterpretation risk. |
| same-name-different-behaviour | Same name, but the value behaves differently (e.g. capped vs not capped). |
| same-purpose-different-name | Same purpose, different label. Often because the vantage point differs. |
| confusing-name | Name suggests a different meaning than the metric has. |
| incorrect-name | Name contradicts the underlying concept. |
| mixing-terminology | Name combines two different concepts. |

- vSphere examples of each pattern are in the vSphere distinction files listed in `related`.

## Vendor-neutral examples

### OpenTelemetry: Usage vs Utilization
- pattern: same-object-same-metric-different-name
- OpenTelemetry uses "Usage" for an absolute amount (e.g. GB) and "Utilization" for a fraction (%).
- Example: Kubernetes Pod memory has Memory Usage (GB) and Memory Utilization (%), not "Memory Usage (GB)" and "Memory Usage (%)".
- OpenTelemetry definitions:
  - usage: an instrument that measures an amount used out of a known total (limit) amount. Named `entity.usage`.
  - utilization: an instrument that measures the fraction of usage out of its limit. Named `entity.utilization`.

### Kubernetes Request vs vSphere Reservation
- pattern: same-purpose-different-name
- Kubernetes "Request" and vSphere "Reservation" serve the same purpose.
- Stated reason (from Google Borg): the persona differs. The developer is requesting a reservation.

### Windows CPU consumption: three tools, three names
- pattern: same-purpose-different-name
- Performance Monitor: Processor Time.
- Task Manager: CPU Utilization.
- Resource Monitor: CPU Usage.

### Windows queue counters
- pattern: same-name-different-behaviour
- Processor Queue Length: counts only threads waiting. Excludes threads currently running.
- Current Disk Queue Length: includes IOs being processed, not only IOs waiting.

### Windows "Task Manager"
- pattern: incorrect-name
- The Windows kernel has no "task" concept. The closest Windows concept is a Job: a group of processes managed as one.
- What runs on top of the kernel are processes. "Process Manager" would match the concept.

## Misconceptions
- "The unit of an overcommit ratio is vCPU per physical thread" → the unit is number; what is divided by what is the description.
- "A metric is identified by its name" → by its key; the name is translated and can change.
- "Processor Queue Length and Current Disk Queue Length count the same thing: work waiting" → Processor Queue Length counts only threads waiting, not the running ones; Current Disk Queue Length also counts IOs being processed. A disk queue above 0 can be IOs in service, not waiting.
- "Two tools show the same metric name, so the values match" → a name does not fix the formula: the same name can differ by object, by level inside the object, and by capping. Check which naming pattern applies (section Pattern catalogue) and read the file of each metric.

## Metadata
```yaml
id: sp5-framework/observability/naming-patterns
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- glossary
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/tools/esxtop/network-units-vs-vsphere-client
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
