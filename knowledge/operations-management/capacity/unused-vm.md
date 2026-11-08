# Unused VM

## Definition
- An unused VM is not idle: it still runs CPU work. It no longer gives business value.
- The application team stopped using it but left it running in case it is wanted later.
- Its activity is IT work, business work, or both.
- The hardest reclamation area: the infrastructure team lacks the business context, and the pattern differs per VM. What identifies VM 00001 may not apply to VM 10000.

## Why its CPU is not low
- IT work: Guest OS upgrade, Guest OS patches, application patches (three workloads, three patterns); VMware Tools updates; antivirus and intrusion detection scans; agent-based backup. High-security estates run many security agents, or agentless scans over the network.
- Business work: batch jobs, reports and monitoring that keep running with no user, such as a report emailed to someone who ignores it. Harder to spot than pure IT work: each case is unique.

## Signs
Each sign alone can be a false positive. Look for VMs that show several.

### Configuration
Configuration is easier to read than utilization: clearer rules.

| Area | Sign |
|---|---|
| Isolation | No virtual NIC connected: it talks to no other machine |
| Guest OS | Old or near-end-of-life Windows, Linux or Kubernetes version: a replacement likely runs elsewhere |
| Guest OS | Expired or temporary license |
| Application | Old or near-end-of-life version |
| Application | Software no longer licensed: power it off with urgency |
| Application | No license, evaluation license or expired license |
| Application | Only base OS and IT security software installed |
| Owner | vCenter folder no longer owned; no tag; no reply to contact; owner left the organization |
| Report | Missing from every report to the owning department (performance, capacity, compliance, chargeback) |
| Location | Cluster, datastore or array due for decommission |
| Location | Folder named old, decommissioned or archived |
| Relationship | Talks to few or no services; its neighbours may be unused too, so this alone is weak |
| Alert | Alerts for the VM disabled |

### Utilization
| Resource | Sign |
|---|---|
| CPU | Busy but always the same work: few context switches; a stable CPU Usage Disparity (%) shows a constant run |
| Memory | Guest OS In Use high but passive: little paging in or out |
| Disk | IOPS and throughput not low, but the file system is stable in size and activity; a repeating long-term pattern |
| Network | Its network is unreachable or isolated; few packets out; talks only to a small, fixed set of servers |
| Network | Its VLAN is due for decommission |
| Log | Far fewer logs or Windows events than its peers; a predictable pattern |

- Applications that hold secure data are often network-restricted by design: few peers is not proof.

### Other signs
| Area | Sign |
|---|---|
| Login | No login to the Guest OS (UI, console, SSH) for a long time, or only brief logins |
| Process | The same set and number of processes; the top CPU process is a system or IT process, not business software |
| Availability | Never rebooted, or rebooted often; a reboot in business hours brings no complaint |
| Performance | A severe performance problem brings no ticket. An owned VM slow for a long time in business hours gets a formal ticket |

- At night a VM can be slow for an hour unnoticed: the performance sign holds only in business hours.

## When unsure
- The VM was announced for deletion repeatedly and nobody claimed it. Powering it off stops running processes and closes open files, and a powered-off VM may not come back cleanly.
- Two safer actions:
  - disconnect it from the network: the application keeps running, and an owner notices;
  - apply a CPU limit: the VM slows down, and an owner complains.
- Mark it: a tag or an "Unused VM" folder. Across several vCenter instances, a VCF Operations custom property. Many of them: a dedicated dashboard.

## Annual stocktake
- For VMs without an identified owner.
- Applies when IT is not profit-oriented, including internal IT with chargeback.
- Starts at day 0, the VM request: an expiry date is mandatory. Temporary VMs get their real end date; permanent VMs get 1 year.
- Beyond 1 year, owners change and contacts are lost. A reorganization can remove the owning team: a permanent VM becomes an unused VM.
- Keep the process simple so every customer agrees to it.
- Owners may not know the VM name. Give them:
  - host name from inside the Guest OS, not the vCenter name;
  - application name;
  - IP address (owners may log in by IP);
  - Guest OS name and version;
  - vCenter folder (the business unit);
  - 95th percentile utilization over the last 3 months;
  - any other context that helps them recognize it.

## Traps
- "CPU is busy, so the VM is in use" → unused VMs keep running IT and batch work; check configuration, owner, login and process signs.
- "One sign is enough to power it off" → each sign can be a false positive; require several, then owner verification.
- "Nobody answered, so power it off" → disconnect the network or apply a CPU limit first; power-off can leave the VM unable to start.
- "Few network peers means unused" → secure data applications are restricted by design.
- "Permanent VMs do not get an expiry date" → give them 1 year; ownership decays.
- "Show owners the vCenter VM name" → they know the Guest OS host name, IP address and application.

## Metadata
```yaml
id: operations-management/capacity/unused-vm
retriever_guide: how-it-works
scope: operations-management
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- capacity
- value
- compliance
product:
- vsphere
- vcf-operations
- windows
- linux
object:
- VirtualMachine
internal_derive: []
related:
- operations-management/capacity/reclamation
- vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
- vsphere/architecture/resource-controls
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Capacity Management > Reclamation > Unused VM (Configuration; Utilization; Other Signs; Annual Stocktake). Pages 118-121.'
corrections: []
review_notes:
- 'Section ''Signs'': several signs read inside the Guest OS (login, process, logs, paging). Kept in operations-management, not guest-os/, because the file spans layers and products.'
status: draft
```
