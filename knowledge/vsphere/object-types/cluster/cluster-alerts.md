# Cluster alerts

## Coverage and receivers
- A cluster is a provider: its alerts go to the infrastructure team.
- Alerted: CPU contention and consumption, memory contention and consumption.
- Every value (threshold, population, wait) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file.
- Contention is read on the cluster's VMs, consumption on its ESXi hosts. Both alerts fire on a share of the members, not on a cluster average, which hides the victim ([`sp5-framework/outputs/alert-design`](../../../sp5-framework/outputs/alert-design.md), section Application team vs infrastructure team).
- Datacenter gets no alert: its clusters can serve different purposes.

## Cluster CPU contention
- Detects: a share of the cluster's VMs did not get the CPU time they asked for: a burst (VM Peak vCPU Ready) and sustained contention (VM CPU Contention) together.
- Measured on its VMs, which is closer to the application. Aggregating from the ESXi hosts is less accurate.
- Remediation: [`vsphere/object-types/cluster/troubleshooting/cluster-vm-contention`](troubleshooting/cluster-vm-contention.md).

## Cluster CPU consumption
- Detects: a share of the cluster's ESXi hosts meet the ESXi CPU consumption condition ([`vsphere/object-types/esxi/esxi-alerts`](../esxi/esxi-alerts.md), section ESXi CPU consumption).
- A share of hosts, not the cluster average, which hides the hosts that run out first.

## Cluster memory contention
- Detects: a share of the cluster's VMs waited for memory pages: the 20-second peak (VM Peak Memory Contention) and the 5-minute value (VM Memory Contention) together.
- Measured on its VMs, closer to the application; aggregating from the ESXi hosts is less accurate.
- Remediation: [`vsphere/object-types/cluster/troubleshooting/cluster-vm-contention`](troubleshooting/cluster-vm-contention.md).

## Cluster memory consumption
- Detects: a share of the cluster's ESXi hosts meet the ESXi memory consumption condition (ballooning with high Consumed).
- The share of hosts is larger than for CPU. Most clusters have fewer than 20 hosts, and memory works as a cache, so high consumption does not mean slow.

## Not alerted
- Disk contention and network contention: not yet in the set.
- Disk and network consumption: the daily check or the NOC screen serves better.

## Misconceptions
- "Cluster CPU contention from host averages" → measure the cluster's VMs; host aggregation is less accurate.
- "A cluster alert fires when one VM suffers" → it looks at the population: a share of the VMs.
- "Cluster memory alert at 25% of hosts, like CPU" → memory needs a larger share of hosts: memory is a cache.
- "Alert on the datacenter too" → its clusters can serve different purposes.

## Metadata
```yaml
id: vsphere/object-types/cluster/cluster-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/object-types/esxi/esxi-alerts
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/cpu/metrics/virtual-motherboard/contention
related:
- vsphere/object-types/cluster/troubleshooting/cluster-vm-contention
- vsphere/object-types/vm/vm-alerts
- vsphere/object-types/resource-pool/resource-pool-alerts
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > CPU Alerts (Infrastructure Contention, Infrastructure Consumption); Memory Alerts (Infrastructure Contention, Infrastructure Consumption); Alerts Planning > Design (alert count table)'
corrections: []
review_notes:
- 'To check after 1.0 (VCF Operations alert definitions): the catalog reads the cluster''s VMs as children; in VCF Operations a VM is a descendant of the cluster (through its hosts).'
- 'To check: Section ''Cluster CPU consumption'': the reason for a share of hosts instead of the average is not stated in the source for consumption.'
status: draft
```
