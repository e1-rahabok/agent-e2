# Units

## CPU frequency
- Decimal: 1 GHz = 1000 MHz.

## Memory and disk space
- Binary prefix: 1 GiB = 1024 MiB.
- Decimal prefix: 1 GB = 1000 MB.
- Mixing binary and decimal prefixes causes apparent mismatches between tools.

## 1000 or 1024 per tool
- No single standard. Google uses 1000 for bytes and bits alike; 1 byte = 8 bits.
- Storage vendors sell decimal capacity; Windows shows binary. A 128 GB drive shows about 119 GB in Windows: 7% less.
- Windows: 1024 for storage.
- VCF Operations: 1024 for storage, network and memory; 1000 for CPU (tested). It labels binary values KB, MB, GB, not KiB, MiB, GiB.
- vCenter counters: KB = 1,024 bytes; kb (kilobit) = 1,000 bits ([`vsphere/tools/vsphere-client/vcenter-statistics`](../../vsphere/tools/vsphere-client/vcenter-statistics.md), section Units).
- Binary names (IEC): kibi, mebi, gibi, tebi, pebi; symbols Ki, Mi, Gi. 1 KiB = 1,024 bytes = 1.024 KB. 1 GiB = 1,073,741,824 bytes.

## Bit or byte
- Disk space and disk throughput: bytes, the amount read or written.
- Network line rate: bits, the data moving on the cable. Pearson uses 1024 for disk space and 1000 for transmission speed; no standard exists.
- Converting a VCF Operations network rate: 30.81 MBps × 1024 = 31,549 KBps, not 30,810, because VCF Operations uses 1024.

## Storage throughput
- Measured in bytes/second, not bits/second. See [`sp5-framework/observability/resource-nature`](resource-nature.md).

## Same metric, different unit per tool
- Tools can show the same metric in different units.
- vSphere example: esxtop shows network in megabits; vSphere Client shows kilobytes. See [`vsphere/tools/esxtop/units-vs-vsphere-client`](../../vsphere/tools/esxtop/units-vs-vsphere-client.md).

## Values above 100%
- A metric computed by summation (not average) can exceed 100%.
- vSphere example: VM CPU Ready, and many VM-level values in esxtop. See [`vsphere/technology/cpu/metrics/virtual-motherboard/ready`](../../vsphere/technology/cpu/metrics/virtual-motherboard/ready.md).

## Misconceptions
- "The 128 GB drive shows 119 GB, so 9 GB is lost" → the vendor counts 1000, Windows counts 1024.
- "30 MBps in VCF Operations is 30,000 KBps" → VCF Operations uses 1024 for network: about 31,550 KBps.
- "KB in VCF Operations means 1,000 bytes" → it means 1,024 bytes, labelled KB, not KiB.

## Metadata
```yaml
id: sp5-framework/observability/units
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
- vsphere/tools/esxtop/units-vs-vsphere-client
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections:
- '2026-11-02: 1 GiB = 1024 MiB; 1 GB = 1000 MB. Uploaded document says KiB/KB.'
review_notes: []
status: draft
```
