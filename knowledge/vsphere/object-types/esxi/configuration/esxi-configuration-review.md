# ESXi configuration review

## Hardware and versions
- Server hardware: few vendors, models and generations; within one model and generation, few specification differences. Flag models nearing end of support.
- ESXi: outdated versions; too many versions; within a version, consistent update and patch levels.
- BIOS: outdated versions; settings consistent, above all within a cluster.

## CPU
- Old generations and too many variants.
- Architecture: it sets the NUMA size and the workload fit (Intel P-cores and E-cores).
- Hyper-Threading present but disabled. It gives more predictable VM performance at a high price in capacity.
- Low frequency: hurts CPU-intensive applications.

## Memory
- Too many size variants.
- CPU-to-memory ratio fits the workload. Rule of thumb: 4 GB of VM RAM per vCPU, so 64 cores with 128 threads maps to 512 GB (1 vCPU per thread). Per class of service, the RAM that matches the CPU: `sp5-framework/capacity/host-spec-from-class-of-service`.
- Large pages: keep them on when performance matters more than memory savings.

## Power management
- BIOS set to OS controlled, so ESXi manages power; ESXi set to Balanced, unless the workload requires otherwise. Details: `vsphere/technology/cpu/configuration/host-power-management`.

## Availability
- Host quarantined, disconnected from vCenter or cluster, unreachable or unresponsive, or powered off.
- Standalone hosts.
- vMotion disabled.

## Security
- Direct Console UI, SSH or ESXi Shell enabled.
- Encryption not enabled.
- Unused devices (DVD-ROM, USB) not disabled.

## Capacity
- A small host limits large VMs. A 2-socket, 32-core, 64 threads, 128 GB host can run a 30-vCPU, 100 GB VM, but the VM spans NUMA nodes.
- Low core count limits large VMs.
- Low memory and low network capacity: size them with vSAN ESA and NSX included.
- Too many variants of all of the above.

## Advanced settings and management
- Advanced settings: as few as possible, each per the standard. No CPU affinity.
- Configuration profiles used correctly.
- Logs: send to VCF Operations for logs; its VCF-specific fields feed the built-in dashboards and alerts.
- Out-of-band management (iLO and equivalents): configured, and secured.
- Third-party agents installed on ESXi.
- NTP and DNS configured. Wrong time makes logs misleading. Across objects, the order of log entries shows which event started the chain: the oldest event is the likely root cause.

## Storage connectivity
- HBAs configured for redundancy.
- Multipathing policy correct. Single path: no redundancy. Too many paths: more complexity without more benefit (two engines vs four on a plane).
- FC and iSCSI zoning per practice, such as single-initiator zoning.

## Network connectivity
- Physical NICs configured for redundancy.
- Actual speed below configured speed: auto-negotiation lowers speed to keep the link, often after high dropped packets.
- 1 Gb and 10 Gb links: all networks except management should be 25 Gb or faster.
- Static IP addresses, not DHCP.
- Addressing follows a pattern: the host number in the name matches the IP address; consistent across networks on one host and across hosts on one network.
- Enough capacity: an NSX Edge host must carry more than the sum of its Edge VMs plus vMotion and vSAN traffic.
- VMkernel traffic separated: management, vMotion, IP storage, vSAN, vSphere Replication. Those networks stay private and unused by anything else.

## Consistency within a cluster
- Identical: CPU model, generation and frequency; memory size and speed; BIOS and ESXi versions; BIOS and ESXi power management; storage paths (count and policy); hardware drivers and firmware.
- Devices of one type in the same bus or slot on every host: easier automated install, administration and troubleshooting.

## Misconceptions
- "Turn off Hyper-Threading for predictable performance" → it costs a large share of capacity; keep it on unless a workload proves otherwise.
- "The host fits a 30-vCPU VM, so it runs well" → on 16 cores per socket it spans NUMA nodes.
- "The NIC is 25 Gb" → check the negotiated speed; auto-negotiation can drop it.
- "Time drift of a few minutes does not matter" → log order across objects identifies the first event; wrong time points at the wrong root cause.
- "More storage paths, more resilience" → past two, paths add complexity; zero redundancy is the real risk.
- "Hosts in one cluster can differ in BIOS power settings" → inconsistent hosts make the same VM perform differently after vMotion.

## Metadata
```yaml
id: vsphere/object-types/esxi/configuration/esxi-configuration-review
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- availability
- performance
- compliance
- capacity
product:
- vsphere
- vsan
- nsx
- vcf-operations
object:
- HostSystem
internal_derive:
- sp5-framework/concepts/configuration-management
related:
- sp5-framework/capacity/host-spec-from-class-of-service
- vsphere/object-types/esxi/configuration/bios-settings
- vsphere/technology/cpu/configuration/host-power-management
- vsphere/technology/cpu/concepts/numa
- vsphere/object-types/cluster/configuration/cluster-configuration-review
- vsphere/technology/network/configuration/network-configuration-review
- vsphere/technology/storage/configuration/storage-configuration-review
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Configuration Management > Review List > Compute > ESXi; Management; Storage Related; Network Related; ESXi Consistency'
corrections: []
review_notes:
- 'To check: Section ''Memory'': 64 cores, 128 threads, 512 GB at 4 GB per vCPU is 1 vCPU per thread; the Price & SLA example (768 GB) is per core. (Q111).'
- 'To check: Section ''Capacity'': the book says aim for 48 cores to maximize the software license; Price & SLA says 64. VCF 9 is licensed per core with a 16-core minimum per CPU (Broadcom KB 313548). Dropped from the body. (Q111).'
- 'To check: Section ''Capacity'', 30-vCPU VM spanning NUMA: 32 cores read as 2 sockets × 16 cores per socket.'
- 'To check: Misconceptions 5 and 6: derived from the book''s rules, not stated in the book.'
status: draft
```
