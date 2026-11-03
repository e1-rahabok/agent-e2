# VM Network Packets Dropped

## Meaning
- The only VM network contention metric.
- Received packets are dropped before reaching the Guest OS. Transmitted packets are dropped after leaving the Guest OS. So values do not match Guest OS counters.
- ESXi drops packets not destined for the guest or violating security settings.
- TCP retransmits dropped packets: the application sees higher latency.

## Formula (VCF Operations)
```text
dropped   = Received Packets Dropped + Transmitted Packets Dropped
delivered = Packets Received + Packets Transmitted
Packets Dropped (%) = dropped / (dropped + delivered) × 100
```

## Behaviour
- Receive drops are far higher than transmit drops: 3,938 VMs, 1 month, about 35 million data points. Receive drops are left out of the SLA for this reason.
- Drops are short and spiky: the 99th percentile was 35x smaller than the maximum.
![VM network dropped: 99th percentile vs maximum, list view](../../images/vm-network-dropped-99th-percentile-vs-max-list-view.png)
- Packets Dropped (%) can jump above 95% for under 15 minutes. Driven by low throughput and high receive drops.
![Receive vs transmit drops across 3,938 VMs](../../images/vm-network-receive-vs-transmit-dropped-across-vms.png)
![Dropped % spike with low throughput and high receive drops](../../images/vm-network-dropped-percent-spike-at-low-throughput.png)

## Profile transmit drops
- Columns: 99th percentile of drop %; sum of transmitted dropped packets; 99th percentile of the maximum dropped in any 300 seconds.
- Millions of transmit drops a month need investigation with the network team. Nobody complains because TCP retransmits.
- Rare huge spikes: example above 100 million packets in 5 minutes, about 333 MB/s for 300 s at 1 KB per packet.
- Regular patterns (example: about 3,800 packets every 5 minutes) are worth raising with the network team.
![VM network transmit dropped: regular spikes of about 3,800 packets every 5 minutes](../../images/vm-network-transmit-dropped-regular-spike-pattern.png)
![Transmit drop profile per VM](../../images/vm-network-transmit-dropped-profile.png)

## Known causes
- False positive transmit drops: NSX firewall rejects outgoing packets (Broadcom KB 322462).
- VMXNET3 packet loss in very high traffic bursts, even VM freezes: not enough receive and transmit buffer, or speed-constrained receive traffic (KB 2039495).

## Traps
- "Packets Dropped (%) at 95% means an outage" → short spikes at low throughput, driven by receive drops.
- "No complaints, so transmit drops are harmless" → TCP hides them through retransmits.

## Metadata
```yaml
id: vsphere/network/metrics/virtual-machine/packets-dropped
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
metric_class: contention
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/network/metrics/comparisons/vm-network-metrics
- vsphere/network/metrics/virtual-machine/packets
images:
  - path: ../../images/vm-network-dropped-99th-percentile-vs-max-list-view.png
    product: [vcf-operations]
    object: [VirtualMachine]
    metric: ['VM Network Packets Dropped']
    image_type: table
    sample: '4,060 VMs'
  - path: ../../images/vm-network-receive-vs-transmit-dropped-across-vms.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM Network Receive Packets Dropped', 'VM Network Transmit Packets Dropped']
    image_type: table
    sample: '3,938 VMs, 1 month'
  - path: ../../images/vm-network-dropped-percent-spike-at-low-throughput.png
    product: [vcf-operations]
    object: [VirtualMachine]
    metric: ['VM Network Packets Dropped (%)', 'VM Network Usage Rate']
    image_type: timeline
  - path: ../../images/vm-network-transmit-dropped-regular-spike-pattern.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM Network Transmit Packets Dropped']
    image_type: timeline
    sample: '1 VM'
  - path: ../../images/vm-network-transmit-dropped-profile.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM Network Transmit Packets Dropped']
    image_type: distribution
source:
  document: PART 3 - Counters.docx
  path: Network > VM > Contention Metrics
corrections: []
review_notes:
- 'Section ''Profile transmit drops'': the book says 1 thousand packets × 1.5 KB = 1,500 MB within 300 seconds. 1,000 × 1.5 KB = 1.5 MB. Open question in docs/author-questions.md.'
- 'KBs from the book: https://knowledge.broadcom.com/external/article?articleNumber=322462 and https://kb.vmware.com/s/article/2039495 (not read).'
status: draft
```
