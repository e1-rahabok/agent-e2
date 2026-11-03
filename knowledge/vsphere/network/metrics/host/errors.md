# ESXi Network Error Packets and Unknown Protocol Frames

## Meaning
- Two contention metrics besides dropped packets: error packets (receive, transmit) and unknown protocol frames.
- Unknown: ESXi cannot decode the packet, so does not know its type. Disabled by default in VCF Operations; enable it.
- Expect error, unknown and dropped packets to be 0 at all times.
- Fleet view in VCF Operations: vSphere \ ESXi Bad Network Packets.
![vCenter ESXi network error counters](../../images/vcenter-esxi-network-error-counters-table.png)

## Detail with esxcli
```text
watch esxcli network nic stats get -n vmnic#
```
- Counters are cumulative: the problem may be in the past.
- vCenter shows totals. The book believes vCenter error counters are Total receive errors and Total transmit errors.

| esxcli counter | Meaning |
|---|---|
| Total receive errors, Total transmit errors | Sum of the errors below, including checksum errors (not reported separately). |
| Checksum errors (csumerr, driver private stats) | Layer 3: hardware, typically cabling. Layer 4: encapsulated packets (VXLAN, overlay). Receive rate too high for hardware checksum: passed to ESXi, counted as error. |
| Receive length errors | Actual packet size differs from the size in the header. |
| Receive over errors | Packets discarded by the NIC hardware buffer. Includes CRC errors. |
| Receive CRC errors | CRC calculated by ESXi differs from the FCS field. |
| Receive FIFO errors, Transmit FIFO errors | NIC cannot process: ring buffer full. |
| Receive missed errors | NIC cannot store or process packets: hardware limits. |
| Receive frame errors; Transmit aborted, carrier, heartbeat, window errors | Listed without description. |

## Observations
- Hosts with receive errors spanned clusters, hardware models and ESXi builds. No correlation with other packet types.
- Receive error counters showed irregular collection, while transmit error collection was regular.

## Traps
- "esxcli shows errors, so the problem is now" → counters are cumulative.

## Metadata
```yaml
id: vsphere/network/metrics/host/errors
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
- availability
product:
- vsphere
- vcf-operations
object:
- HostSystem
metric_class: contention
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/network/metrics/host/packets-dropped
images:
  - path: ../../images/vcenter-esxi-network-error-counters-table.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Network Error Packets', 'ESXi Network Unknown Protocol Frames']
    image_type: table
source:
  document: PART 3 - Counters.docx
  path: Network > ESXi > Contention Metrics > Error Metrics; esxcli
corrections: []
review_notes:
- 'KB from the book: https://knowledge.broadcom.com/external/article?articleNumber=341594 (not read; descriptions are the book''s summary).'
status: draft
```
