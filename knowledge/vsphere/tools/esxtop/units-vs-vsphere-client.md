# Network units: esxtop vs vSphere Client

## Meaning
- esxtop shows network throughput in megabits per second (MbTX/s, MbRX/s), per port and per vmnic.
- vSphere Client: VM and host network throughput (Usage, Data receive rate, Data transmit rate) is in kilobytes per second (KBps), one KB being 1,024 bytes. The API stores these counters in KBps, and the Advanced performance chart and its CSV export show the same values.
- The VM and host network charts carry Mbps in their title, but their counters are KBps. Only the two stacked Overview charts (cluster Hosts view, host Virtual Machines view) list megabits per second in the vSphere 9.1 documentation. See [`vsphere/tools/vsphere-client/vcenter-statistics`](../vsphere-client/vcenter-statistics.md), section Units.
- Conversion: esxtop Mbps is about vSphere Client KBps × 8 / 1,000. The two differ by a factor of about 125, because of bits against bytes (8) and mega against kilo (1,000).
- The two tools also differ in interval: esxtop shows the average of its refresh interval (5 seconds by default); the vSphere Client Real-time chart shows 20-second averages. A steady stream gives matching values after conversion; a bursty one does not.

## Misconceptions
- "esxtop shows 125 times more traffic than vCenter, so one tool is wrong" → the units differ: megabits per second in esxtop, kilobytes per second in vCenter.
- "The chart title says Mbps, so the vCenter value is megabits" → the VM and host Usage, Data receive rate and Data transmit rate counters are kilobytes per second.
- "Divide KBps by 1,000 for Mbps" → that skips bits against bytes: the result is 8 times too low.

## Metadata
```yaml
id: vsphere/tools/esxtop/units-vs-vsphere-client
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
- VirtualMachine
metric_class: consumption
internal_derive:
- sp5-framework/observability/units
same_name: []
same_meaning: []
related: []
source:
  document: Knowledge base; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); vSphere Web Services API 9.1.1 reference, Network Counters; Broadcom KB 447068
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; vSphere Monitoring and Performance > Clusters, Hosts and Virtual Machines > Network (Mbps) and Network Rate (Mbps) (pp. 2041, 2078-2082, 2106-2108); esxtop Network Panel (p. 2164)
corrections: []
review_notes:
- 'Section ''Meaning'': whether esxtop counts a megabit as 1,000,000 or 1,048,576 bits (a 5% difference in the conversion). The vSphere 9.1 documentation (Network Panel, p. 2164) defines MbTX/s only as megabits transmitted per second; check against a measured stream or a Broadcom KB.'
status: draft
```
