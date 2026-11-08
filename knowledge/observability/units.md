# Units

## CPU frequency
- Decimal: 1 GHz = 1000 MHz.

## Memory and disk space
- Binary prefix: 1 GiB = 1024 MiB.
- Decimal prefix: 1 GB = 1000 MB.
- Mixing binary and decimal prefixes causes apparent mismatches between tools.

## 1000 or 1024 per tool
- No single standard. Google uses 1000 for bytes and bits alike; 1 byte = 8 bits.
- Storage vendors sell decimal capacity; Windows shows binary. A 128 GB drive shows about 116 GB in Windows: 9% less.
- Windows: 1024 for storage.
- VCF Operations: 1024 for storage, network and memory; 1000 for CPU (author's tests). It labels binary values KB, MB, GB, not KiB, MiB, GiB.
- vCenter counters: KB = 1,024 bytes; kb (kilobit) = 1,000 bits (`vsphere/tools/vsphere-client/vcenter-statistics`, section Units).
- Binary names (IEC): kibi, mebi, gibi, tebi, pebi; symbols Ki, Mi, Gi. 1 KiB = 1,024 bytes = 1.024 KB. 1 GiB = 1,073,741,824 bytes.

## Bit or byte
- Disk space and disk throughput: bytes, the amount read or written.
- Network line rate: bits, the data moving on the cable. Pearson uses 1024 for disk space and 1000 for transmission speed; no standard exists.
- Converting a VCF Operations network rate: 30.81 MBps × 1024 = 31,549 KBps, not 30,810, because VCF Operations uses 1024.

## Storage throughput
- Measured in bytes/second, not bits/second. See `observability/resource-nature`.

## Same metric, different unit per tool
- Tools can show the same metric in different units.
- vSphere example: esxtop shows network in megabits; vSphere Client shows kilobytes. See `vsphere/tools/esxtop/units-vs-vsphere-client`.

## Values above 100%
- A metric computed by summation (not average) can exceed 100%.
- vSphere example: VM CPU Ready, and many VM-level values in esxtop. See `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.

## Traps
- "The 128 GB drive shows 116 GB, so 12 GB is lost" → the vendor counts 1000, Windows counts 1024.
- "30 MBps in VCF Operations is 30,000 KBps" → VCF Operations uses 1024 for network: about 31,550 KBps.
- "KB in VCF Operations means 1,000 bytes" → it means 1,024 bytes, labelled KB, not KiB.

## Metadata
```yaml
id: observability/units
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
- vsphere/tools/esxtop/units-vs-vsphere-client
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections:
- '2026-11-02: 1 GiB = 1024 MiB; 1 GB = 1000 MB. Uploaded document says KiB/KB; author has fixed the book.'
review_notes:
- 'Sections ''1000 or 1024 per tool'' and ''Bit or byte'': PART 3 - Counters.docx, Metric Mastery > Units (author update, 2026-11-08).'
status: draft
```
