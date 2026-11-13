# The VCF Operations report suite

## Reports as a set
- The reports were designed together, with as little overlap as possible, so none stands alone. Run them as a set.
- Inventory, configuration and capacity together give full coverage:
  - inventory is about count: which sizes and types exist and which are common; the goal is to know the variation;
  - configuration is about the settings of the object;
  - capacity is about size, often as a line chart to show change over time.

## Example: VM configured size
- Inventory: how many sizes exist and which are most common; are they larger or smaller than expected? Pie chart: relative distribution and the number of variations.
- Configuration: sizes in order, to focus on monster VMs. Bar chart whose buckets filter out the small VMs.
- Capacity: undersized and oversized VMs. Bar chart with buckets undersized, rightsized, oversized; a table of the top 10 VMs to act on for detail.

## Example: ESXi host
- Inventory: relative distribution by vendor, server type (blade, rack mount) and server generation.
- Configuration: absolute distribution by ESXi version, CPU model and CPU generation.
- Capacity: absolute distribution by CPU size and memory size.

## Example: vSphere cluster
- Inventory: bar chart of clusters grouped by number of VMs; you set the value of each bar.
- Configuration: bar chart of clusters grouped by number of ESXi hosts. The VM count is not cluster configuration.
- Capacity: bar chart of clusters grouped by size, such as 5 buckets of total memory capacity.

## Three report sets
- Executive Summary: one summary report, presented by someone who knows the environment, not read alone by IT leaders. The big picture to support decisions on major initiatives; no detail.
- Operations Management: one set of reports covering inventory, capacity, performance and configuration; run as a set.
- Spreadsheet export: one CSV export per vSphere object type, run as needed.

## Executive report
- Starts with key inventory: the readers may not know the environment.
- No technical terms, unless the plain word causes confusion.
- No detail: no names of VMs, clusters or datastores.
- If the context allows, put what needs their approval at the top, such as budget for refreshing ageing hardware.

## Operations management reports
- The 4 reports share one table of contents: consumer (VM), then the providers (compute, storage, network). By page count, parts can be split or combined.
- Each section is technically a dashboard and can span pages:

| Report | Consumer | Provider |
|---|---|---|
| Inventory | VM Inventory | vSphere Inventory |
| Performance | VM Performance | vSphere Compute Performance; vSphere Storage Performance |
| Capacity | VM Capacity; Reclaimable Capacity | vSphere Compute Capacity; vSphere Storage Capacity |
| Configuration | Guest OS Configuration; VM Configuration; VM Size Distribution | ESXi Hardware Configuration; ESXi Software Configuration; vSphere Cluster Configuration; vSphere Network Configuration |

## Misconceptions
- "Run one report on its own" → the suite avoids overlap; one report alone misses what another holds.
- "VM count is cluster configuration" → configuration groups clusters by host count; VM count is inventory.
- "Executives read the summary report alone" → it is designed to be presented by someone who knows the environment.
- "Name the problem VMs in the executive report" → no individual objects; detail goes to the operations reports.
- "Inventory and capacity of VM size are the same report" → inventory counts the variation of sizes; capacity shows under- and oversized VMs.

## Metadata
```yaml
id: vcf-operations/report-suite
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- performance
- security
- capacity
product:
- vcf-operations
- vsphere
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive:
- sp5-framework/outputs/report-design
- sp5-framework/outputs/reports-vs-dashboards
related:
- sp5-framework/outputs/it-leaders-dashboards
- sp5-framework/capacity/rightsizing
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Reports > Functional Considerations (the reports as a set; Overall Design: Executive Report, Operations Management)'
corrections: []
review_notes:
- 'To check: Report names: whether VCF Operations 9.1 still ships them (VCF Operations 9.1 documentation).'
status: draft
```
