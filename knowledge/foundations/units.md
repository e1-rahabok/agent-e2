---
id: foundations/units
type: concept
scope: vendor-neutral
resources: [cpu, memory, storage, network]
related: [vsphere/network/distinctions, vsphere/cpu/distinctions]
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes:
  - "Uploaded document says '1 GiB = 1024 KiB and 1 GB = 1000 KB'. Written here as GiB = 1024 MiB and GB = 1000 MB. Please confirm."
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
- vSphere example: esxtop shows network in megabits; vSphere Client shows kilobytes. See `vsphere/network/distinctions`.

## Values above 100%
- A metric computed by summation (not average) can exceed 100%.
- vSphere example: VM CPU Ready, and many VM-level values in esxtop. See `vsphere/cpu/distinctions`.
