---
id: foundations/units
type: concept
scope: vendor-neutral
resources: [cpu, memory, storage, network]
related: [vsphere/network/distinctions, vsphere/cpu/distinctions]
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections:
  - "2026-11-02: 1 GiB = 1024 MiB; 1 GB = 1000 MB. Uploaded document says KiB/KB; author has fixed the book."
review_notes: []
status: draft
---

# Units

## CPU frequency
- Decimal: 1 GHz = 1000 MHz.

## Memory and disk space
- Binary prefix: 1 GiB = 1024 MiB. [author-correction 2026-11-02]
- Decimal prefix: 1 GB = 1000 MB. [author-correction 2026-11-02]
- Mixing binary and decimal prefixes causes apparent mismatches between tools.

## Storage throughput
- Measured in bytes/second, not bits/second. See `foundations/resource-nature`.

## Same metric, different unit per tool
- Tools can show the same metric in different units.
- vSphere example: esxtop shows network in megabits; vSphere Client shows kilobytes. See `vsphere/network/distinctions`.

## Values above 100%
- A metric computed by summation (not average) can exceed 100%.
- vSphere example: VM CPU Ready, and many VM-level values in esxtop. See `vsphere/cpu/distinctions`.
