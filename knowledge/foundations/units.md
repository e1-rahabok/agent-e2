---
id: foundations/units
retriever_guide: how-it-works
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
- vsphere/network/metrics/comparisons/esxtop-vs-vsphere-client-units
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections:
- '2026-11-02: 1 GiB = 1024 MiB; 1 GB = 1000 MB. Uploaded document says KiB/KB; author has fixed the book.'
review_notes: []
status: draft
---

# Units

## CPU frequency
- Decimal: 1 GHz = 1000 MHz.

## Memory and disk space
- Binary prefix: 1 GiB = 1024 MiB.
- Decimal prefix: 1 GB = 1000 MB.
- Mixing binary and decimal prefixes causes apparent mismatches between tools.

## Storage throughput
- Measured in bytes/second, not bits/second. See `foundations/resource-nature`.

## Same metric, different unit per tool
- Tools can show the same metric in different units.
- vSphere example: esxtop shows network in megabits; vSphere Client shows kilobytes. See `vsphere/network/metrics/comparisons/esxtop-vs-vsphere-client-units`.

## Values above 100%
- A metric computed by summation (not average) can exceed 100%.
- vSphere example: VM CPU Ready, and many VM-level values in esxtop. See `vsphere/cpu/metrics/virtual-machine/ready`.
