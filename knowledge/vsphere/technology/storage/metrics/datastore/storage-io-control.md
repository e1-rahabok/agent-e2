# Datastore Storage I/O Control metrics

## Meaning
- Datastore-wide counters computed by Storage I/O Control (SIOC). They span all hosts and VMs on the datastore, unlike the host datastore counters.
- All show 0 when SIOC is deactivated on the datastore.
- Statistics level 3. Not stored at the default level 1.
- Storage I/O Control components are deprecated as of VCF 9.0. The counters still appear in the vSphere 9.1 charts.

| Counter | Chart label | Unit, rollup | Meaning |
|---|---|---|---|
| sizeNormalizedDatastoreLatency | Storage I/O Control Normalized Latency | µs, Average | Weighted device response time across all hosts and VMs. |
| datastoreIops | Storage I/O Control Aggregate IOPs | Number, Average | IOPS on the datastore, summed over all hosts and VMs. |
| siocActiveTimePercentage | Storage I/O Control Activity | %, Average | Share of time SIOC actively throttled to control latency. |
| datastoreVMObservedLatency | VM observed latency per Datastore | µs, Latest | Average datastore latency as the VMs see it. |

## Formula
```text
Normalized Latency = sum(device latency x IO count) / sum(IO count), adjusted for IO size, over all hosts and VMs
```

## Includes / excludes
- Normalized Latency includes: device-level latency only.
- Normalized Latency excludes: queuing in the hypervisor storage stack (kernel) and inside the VM.
- Normalized Latency discounts high latency caused by large IOs, so large-block workloads do not make the datastore look slower than it is.
- VM observed latency includes what sits between the VM and the device, so it is higher than Normalized Latency on a congested host.

## Why
- SIOC detects congestion from the device latency of the whole datastore, not of one host. One host cannot see the IO of the others.
- Weighting by IO count stops an idle host with a few slow IOs from dominating the value.
- When congestion crosses the SIOC threshold, SIOC lowers the device queue depth of each host by shares. Host Maximum Queue Depth per datastore then changes over time. See `vsphere/technology/storage/metrics/host/datastore`.
- Activity above 0 means SIOC was throttling. Shares decided which VMs got the IO; a VM with low shares sees its own latency rise.

## Traps
- "Normalized Latency is low, so VMs see low latency" → it excludes kernel queuing. Compare with VM observed latency.
- "Normalized Latency equals the host DAVG" → it is size-adjusted and weighted over all hosts.
- "All SIOC charts at 0, so no congestion" → check whether SIOC is enabled and the statistics level is 3 or higher.
- "Aggregate IOPs from one host's chart" → one host shows only its own share; this counter covers all hosts.

## Metadata
```yaml
id: vsphere/technology/storage/metrics/datastore/storage-io-control
retriever_guide: metric-meaning
scope: vsphere
technology:
- storage
pillar:
- performance
product:
- vsphere
object:
- Datastore
instance:
- aggregate
metric_class: contention
internal_derive:
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
same_name: []
same_meaning: []
related:
- vsphere/technology/storage/metrics/host/datastore
- vsphere/technology/storage/metrics/virtual-motherboard/datastore
- vsphere/technology/storage/troubleshooting/host-storage-latency
- vsphere/tools/vsphere-client/vcenter-statistics
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: vSphere Monitoring and Performance > Overview Performance Charts > Datastores and Datastore Clusters > Storage I/O Control Normalized Latency, Aggregate IOPs, Activity, Maximum Queue Depth per Host, Virtual Machine Observed Latency per Datastore (pp. 2048-2052)
corrections: []
review_notes:
- 'Section ''Meaning'': SIOC deprecation from the vSphere 9.1 documentation, vSphere Resource Management > Manage Storage I/O Resources with vSphere (p. 1886).'
- 'Whole file: from the vSphere 9.1 documentation, not the book.'
- 'Section ''Formula'': the plain-text formula restates the documentation text (IO count as weight, adjusted for IO size). The exact size adjustment is not published.'
- 'To check: Section ''Why'': SIOC lowers per-host device queue depth by shares when the congestion threshold is crossed; the documentation says only that queue depth can change over time when congestion is detected at the array.'
- 'To check: Section ''Includes / excludes'': VM observed latency is higher than Normalized Latency on a congested host, inferred from the two definitions. It may explain the gap the book leaves unexplained in vsphere/technology/storage/metrics/host/datastore.'
status: draft
```
