# Configuration management

## Purpose
- Configuration management prevents issues caused by wrong settings: the actual value must match the intended value, and the hardware and software configuration must match the documented architecture.
- Quantify it to track it over time: 100% when every configuration rule is met, 0% when none is.
- Wrong configuration hits six areas: availability, performance, capacity, cost, security, compliance. Choose each trade-off with all six in mind.
- Configuration is a means to an end, not a pillar: `operations-management/sp5-framework/overview`.

## Approach
- Start with a plan: which settings suit which objects, documented as corporate standards. The standards follow the architecture and security policy and change over the years; keep them documented.
- Compare reality with the standard on a dashboard. If they differ, one of the two is wrong: fix the setting or fix the standard.
- Standards simplify operations and are often required for compliance.
  - Example: one VMware Tools version is the standard, two older versions are allowed while upgrades run. A pie chart of Tools versions should show three slices. More slices means reality differs from the standard.
- The plan reaches beyond VCF, because of dependencies. Jumbo frames must be configured end to end, every physical switch included.
- Check the whole stack, lower layers first: a problem in a layer hits every layer above it.
- Conflicting requirements and constraints (cost, capacity) force compromises, such as several classes of service in one cluster. Compromises make configuration management more necessary, not less.
- It never ends: versions and product end-of-life keep moving.
- VCF product settings to review:
  - licenses: the right amount of each type;
  - certificates: the parts of VCF expire on different dates;
  - configuration maximums: reached in very large deployments;
  - users and roles: service accounts, local accounts, password management;
  - logs: ESXi, vCenter and NSX send the right log types;
  - compatibility: patching and upgrading make it a cycle.

## Three review dimensions
- Thousands of settings exist. Review by impact on Day 2 operations, not by product feature: features that look related can affect operations differently.
- VCF Operations reviews configuration by impact, not grouped by feature or object.
- Use all three dimensions; each catches what the others miss.
![Time: correct it? → update it? → simplify it? → optimize it? Architecture: consumer objects (Guest OS, VM, Kubernetes pod, namespace) and provider objects (ESXi, resource pool, datastore, vSAN, NSX); server, storage, network. Operations: availability → performance → security → capacity → cost](images/configuration-review-time-architecture-operations-dimensions-diagram.png)
- **Time**: the most pressing first, and checked most often. Four steps:
  1. Correct it: settings that are incorrect, insecure, against the corporate standard or against best practice. The most urgent.
  2. Update it: correct settings on old versions. Start with the oldest, above all those out of support. Fixes often exist only in later versions; components too far behind cause support and upgrade problems; old hardware costs more rack space, cooling and UPS. Each component can be current and still not be compatible or supported with the others.
  3. Simplify it: correct and current, but complicating IaaS operations. Set a policy to minimize them. A missing standard is a common cause. Flexible VM vCPU and memory sizes do not count: their permutations are not managed.
  4. Optimize it: cost and capacity, once nothing is wrong. Maximize resource use and minimize cost.
- **Architecture**:
  - consumer objects (Guest OS, VM, Kubernetes pod and namespace) and provider objects (ESXi, resource pool, datastore, vSAN, NSX) matter equally: customers see the consumer; one provider affects many consumers;
  - by infrastructure: server (CPU, GPU, memory), storage (from the Guest OS partition and virtual disk down through the ESXi storage stack, datastore, RDM, vVols, vSAN), network.
- **Operations** (pillars), in order:
  - availability first: if it is down, nothing else matters. Hardware gets it from redundant components; software from clustering, with two load balancers in front of the nodes;
  - performance: up is not fast;
  - security and audit: fast is not secure;
  - then capacity, cost and sustainability.

## Four types of check
- Two families: a value check compares one item with a desired value; multi-object checks compare items with each other (consistency, compatibility, variance).
- **Value check** against:
  - a standard: naming convention; logging standard for Windows, Linux, ESXi, VCF appliances, NSX Edge. For critical VMs, log the errors that never become metrics (Windows events, parsed into the log tool);
  - a version: at least vendor-supported; aim for N and N-1 only;
  - a date: end of warranty, end of support, certificate expiry;
  - a threshold: absolute (a configuration maximum, which varies with the combination of features) or relative to the parent (a large container on a Kubernetes node hurts its neighbours and itself).
- **Consistency check** (identical values):
  - against peers: all ESXi hosts in a cluster configured identically;
  - against the partner across a connection: ESXi MTU matches the distributed switch MTU.
- **Compatibility check** (values differ but must work together): what works with what, when and where.
  - Mixed vendors do not work equally well in every combination; minor version numbers matter.
  - Upgrading one component often forces upgrades of adjacent ones.
  - What suits development may not suit production; what suited production last year may not suit it this year.
- **Variance check** (number of variants): flexibility adds variants, and each variant adds complexity in security, capacity, compliance, performance and daily operations. Count variants of Guest OS, VM, ESXi, server BIOS, cluster, storage and network.
  - Some variance costs nothing operationally: free VM sizing. T-shirt sizes waste resources and save little overhead.
- Review the names before the settings: naming conventions are often not followed.

## Security: configuration vs activity
- Configuration issues are easy: compare a setting with an expected value.
- Activity issues depend on context. Three kinds:
  - by a human: delete commands typed on an ESXi console;
  - by a system: excessive broadcast or multicast from a VM, where traffic should be unicast. Monitor at the VM; troubleshoot inside Windows or Linux, the source;
  - by an AI agent acting as a digital employee: identified by its own employee ID, reporting to a human employee.
- Checks for the security team, across VCF:
  - root: minimize its use on ESXi and VCF appliances; define the allowed scenarios; log and analyze the commands typed, with a log dashboard that traps commands such as mv and rm;
  - timeouts for the ESXi Shell and user logins;
  - access to vCenter limited.

## Review lists by object
- A setting has several sides (NFS security is storage, datastore and security). The lists group by object; a setting can appear under two objects.
- Guest OS: `guest-os/system/concepts/guest-os-configuration-review`.
- VM and VMware Tools: `vsphere/object-types/vm/configuration/vm-configuration-review`.
- Shares, reservations, limits, resource pools: `vsphere/object-types/vm/configuration/resource-settings-guidance`.
- ESXi: `vsphere/object-types/esxi/configuration/esxi-configuration-review`.
- Cluster: `vsphere/object-types/cluster/configuration/cluster-configuration-review`.
- Storage: `vsphere/technology/storage/configuration/storage-configuration-review`.
- Network: `vsphere/technology/network/configuration/network-configuration-review`.

## Traps
- "Reality differs from the standard, so fix the setting" → one of the two is wrong; the standard may be outdated.
- "Every component runs the latest version, so the stack is fine" → each can be current and the combination still unsupported. Check compatibility, not only version.
- "Jumbo frames are set on ESXi and the distributed switch, so they work" → every physical switch in the path must match; check end to end.
- "Allow every VM size so customers are flexible; it adds variance" → VM size variants are not managed permutations and add no operational complexity.
- "Group the review by product feature" → review by Day 2 impact: correct, update, simplify, optimize.
- "All ESXi hosts are on supported versions, so no action" → aim for N and N-1; more variants add complexity even when each is supported.
- "Security review means checking settings" → activity (human, system, AI agent) needs context and logs as well.
- "Broadcast storm from a VM: fix it in vSphere" → the VM shows it; the cause is inside the Guest OS.

## Metadata
```yaml
id: operations-management/sp5-framework/configuration-management
retriever_guide: how-it-works
scope: operations-management
technology:
- system
pillar:
- availability
- performance
- compliance
- capacity
- cost
product:
- vsphere
- vsan
- nsx
- vcf-operations
- kubernetes
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
- Datastore
internal_derive:
- operations-management/sp5-framework/overview
related:
- operations-management/sp5-framework/health-risk-efficiency
- guest-os/system/concepts/guest-os-configuration-review
- vsphere/object-types/vm/configuration/vm-configuration-review
- vsphere/object-types/vm/configuration/resource-settings-guidance
- vsphere/object-types/esxi/configuration/esxi-configuration-review
- vsphere/object-types/cluster/configuration/cluster-configuration-review
- vsphere/technology/storage/configuration/storage-configuration-review
- vsphere/technology/network/configuration/network-configuration-review
images:
  - path: images/configuration-review-time-architecture-operations-dimensions-diagram.png
    product: [vsphere, vsan, nsx, kubernetes]
    object: [VirtualMachine, HostSystem, ResourcePool, Datastore]
    topic: 'Three configuration review dimensions: time, architecture, operations'
    image_type: diagram
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Configuration Management (opening); Approach (Review Approach, Time-based Approach, The 4 Types of Check); Review List (opening, Security) (pp. 129-133, 148-149)'
corrections: []
review_notes:
- 'Section ''Four types of check'': the book announces 4 types and lists 2 bullets (value, multi-object); the subsections are value, consistency, compatibility, variance. Written as the four subsections. Q113.'
- 'Section ''Security'': the book writes Log Insight; written as the log tool (VCF Operations for logs). Q113.'
- 'Folder: no configuration pillar folder; kept in performance/ with the other cross-pillar files (Q094).'
status: draft
```
