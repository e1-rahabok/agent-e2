# Distributed Power Management (DPM)

## Purpose
- DPM conserves power when hosts in a cluster are underutilized.
- Mechanism:
  - consolidates VMs onto a subset of the hosts in the cluster,
  - puts the remaining hosts into standby mode.
- DPM keeps enough hosts powered on to meet the demand of the VMs in the cluster.
- When demand increases, DPM powers on additional hosts and migrates VMs to them. Load is then balanced across the powered-on hosts.

## Suitable clusters
- Most appropriate: clusters where the composite VM demand varies significantly over time.
- Example: demand is higher during the day and much lower at night.
- Clusters with consistently high demand relative to cluster capacity have little opportunity to standby hosts.

## Demand inputs
- Starting with vSphere 7.0, DPM calculates VM memory demand from granted memory.
- Granted memory is typically stable over time.
- DPM considers both CPU and memory demand, but it mostly responds to changes in CPU demand.

## Relation to DRS
- DPM uses DRS. Most DRS best practices also apply to DPM. See [`vsphere/object-types/cluster/concepts/drs-overview`](drs-overview.md).

## DPM vs host power management
- DPM powers off hosts to save power.
- Host power management reduces power on hosts that stay powered on. See [`vsphere/technology/cpu/configuration/host-power-management`](../../../technology/cpu/configuration/host-power-management.md).
- DPM and host power management can be used together for the best power conservation.
- Host power management policies allow efficient use of the hosts that remain on. Using both together can save more power than either alone.

## Automation levels
- Hosts in a DPM-activated cluster inherit the automation level set at the cluster level.
- The automation level can also be set per host. A host-level setting overrides the inherited level.
- Manual DPM: vCenter asks for user approval before it puts a host into standby or takes it out of standby.
- Automatic DPM: the most flexibility and the most power savings.
- DPM prefers hosts in automatic mode over hosts in manual mode.
- DPM can be deactivated for individual hosts, even when DPM is active for the cluster.
- Example: deactivate DPM for hosts running mission-critical VMs. VM/Host affinity rules then keep those VMs from being migrated away from those hosts.

## DPM Threshold
- Set in the cluster settings menu, as DPM Threshold.
- Controls how aggressively DPM recommends migrations, and how aggressively it puts hosts into and out of standby.
- Default: 3 (medium aggressiveness).

## Demand history and excess capacity
- DPM considers historical demand when it decides how much capacity to keep powered on.
- DPM keeps some excess capacity for increases in demand.
- DPM powers on additional hosts when demand of existing VMs rises unexpectedly, or to admit new VMs.
- A host is put into standby only if the VM memory demand in the cluster is low.
- Starting with vSphere 7.0, memory demand is low only if the granted memory is low.

## Minimum capacity variables
- For clusters with frequent unexpected demand spikes, two advanced options set the minimum capacity that DPM keeps powered on:
  - `MinPoweredOnCpuCapacity`: default 1 MHz.
  - `MinPoweredOnMemCapacity`: default 1 MB.

## Power-on lag
- Without predictions, DPM is reactive: it powers on a standby host only after the demand on the powered-on hosts has risen above its target range. The historical demand it considers sizes the spare capacity it keeps; it does not forecast a daily ramp.
- A standby host takes minutes to return: power on through IPMI, iLO or Wake-on-LAN, boot ESXi, reconnect to vCenter, start the HA agent. DRS then needs further minutes of vMotion to move VMs onto it.
- When the load ramps faster than hosts return, the VMs on the powered-on hosts contend (VM CPU Ready rises) until enough hosts carry load. The contention repeats every time the ramp repeats.
- Signature of power-on lag: contention only while the number of powered-on hosts climbs, and normal VM CPU Ready once all hosts are on. A cluster that contends with all hosts powered on is short of capacity instead.
- Adding hosts does not fix power-on lag: DPM puts the new hosts in standby during the quiet hours as well.
- Ways to have the hosts on before a known ramp: a Scheduled Task that deactivates DPM before the ramp (this powers on all standby hosts) and activates it after; Predictive DRS with VCF Operations predictions; a higher `MinPoweredOnCpuCapacity`; a more conservative DPM Threshold; or no DPM on a cluster whose users cannot accept the lag.
- After the change, check that VM CPU Ready stays low across the whole ramp window, not only in the hourly or daily average.

## Scheduling
- Advanced option `DPMPowerOffInterval` (introduced in vSphere 7.0): minimum time DPM waits between calculations of whether hosts should go into standby.
- Default: 30 minutes. Maximum: 12 hours. Configured independently for each cluster.
- DPM can be activated or deactivated on a schedule with Scheduled Tasks in vCenter Server.
- Deactivating DPM with Scheduled Tasks powers on all standby hosts in the cluster.
- Use case: reduce the delay in responding to load spikes that occur at set times of the day.
- Restarting the vCenter Server or the vCenter vpxd service powers on all standby ESX hosts managed by that vCenter Server.

## Predictive DRS and predictive DPM
- Needs Predictive DRS on in the cluster's DRS settings, and VCF Operations (formerly vRealize Operations, 6.4 or later) registered with the vCenter as its Predictive DRS data provider.
- With predictive DRS configured to receive predictions, DPM can bring hosts back from standby before demand increases.
- Example: if demand rises every morning at 9 am, DPM can bring hosts out of standby by 8 am.

## HA interaction
- DPM respects vSphere HA settings. It accounts for them when it recommends standby or power-on.
- In a cluster with HA active, DPM keeps excess powered-on capacity to meet HA requirements.
- Effect: fewer hosts can go into standby than in a cluster without HA.
- Effect: additional VMs might not be admitted even when the cluster seems to have available resources. HA reserves this capacity.
- If HA is active and one or more VMs are powered on, DPM keeps at least two hosts powered on. This applies even when HA admission control is deactivated.

## Misconceptions
- "DPM saves power with no effect on capacity" → DPM keeps excess capacity and HA capacity powered on. Fewer hosts go into standby than the raw load suggests.
- "Scheduled DPM deactivation keeps standby hosts off" → deactivating DPM with Scheduled Tasks powers on all standby hosts.
- "DPM learns the daily pattern and wakes hosts before the morning load" → only with Predictive DRS predictions; otherwise it powers on after demand has risen, and boot plus vMotion take minutes.
- "VMs contend every morning in a DPM cluster, so buy more hosts" → check VM CPU Ready with all hosts powered on; if it is normal, the cause is power-on lag, and new hosts would also go into standby.

## Metadata
```yaml
id: vsphere/object-types/cluster/concepts/dpm
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
pillar:
- value
- availability
product:
- vsphere
object:
- ClusterComputeResource
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/object-types/cluster/concepts/drs-overview
- vsphere/object-types/cluster/configuration/drs-migration-levels
- vsphere/technology/cpu/configuration/host-power-management
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: VMware Distributed Power Management (DPM) (pp. 80-81)
corrections: []
review_notes:
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: Section ''Power-on lag'': reactive power-on and the return sequence of a standby host (vSphere 9.1 Resource Management, Managing Power Resources, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-resource-management.html).'
- 'To check: Predictive DRS and predictive DPM: the source requires VMware vRealize Operations 6.4 or later, an old product version; whether the feature still applies in vSphere 9.0 and VCF Operations.'
status: draft
```
