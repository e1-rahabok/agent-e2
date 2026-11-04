# Naming patterns

A metric name does not reliably tell what the metric measures.
Two metrics can share a name and differ. Two names can mean the same thing.
The patterns below classify the ways names mislead.

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
- trap: treating both "queue" counters as the same kind of count.

### Windows "Task Manager"
- pattern: incorrect-name
- The Windows kernel has no "task" concept. The closest Windows concept is a Job: a group of processes managed as one.
- What runs on top of the kernel are processes. "Process Manager" would match the concept.

## Metadata
```yaml
id: foundations/naming-patterns
retriever_guide: metric-meaning
scope: vendor-neutral
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product: []
internal_derive: []
related:
- glossary
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/technology/network/metrics/comparisons/esxtop-vs-vsphere-client-units
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections:
- '2026-11-02: Windows queue counters. Processor Queue Length excludes running threads; Current Disk Queue Length includes IOs being processed. Uploaded document states the disk part reversed.'
review_notes: []
status: draft
```
