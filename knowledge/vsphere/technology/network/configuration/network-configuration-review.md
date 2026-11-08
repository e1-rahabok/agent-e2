# Network configuration review

## Scope
- Every network component of VCF: distributed switches and port groups, NSX, physical switches and general settings. One list, for the discussion with the network team.
- Host-side links (NIC redundancy, negotiated speed, VMkernel separation, addressing): `vsphere/object-types/esxi/configuration/esxi-configuration-review`.

## Distributed switch and port groups
- Version: outdated switch versions.
- Network I/O Control configured.
- Unused port groups: a security risk. They tend not to be monitored, yet anyone can use the path.
- Traffic shaping used where it fits.
- Shares per traffic type set correctly: `operations-management/performance/noisy-neighbour`.
- Limits: can shares replace them? Shares are more flexible for contention.
- MTU mismatch hurts performance.
- Jumbo frames: on the right networks, end to end. For segments outside your control, detect changes with a discovery protocol (CDP or LLDP).
- Security policy: Forged Transmits, Promiscuous Mode and MAC Address Changes set to Reject.

## Other components
- Top-of-rack switch: firmware compatible with the ESXi NICs it connects; speed not negotiated down.
- Firewall: ports open for services such as syslog, NTP and vSphere HA.
- NSX: version compatible with the other components; NSX Manager redundancy as planned; Edge configuration per practice.
- Encryption: vMotion and similar networks encrypted; hardware offload such as AES-NI used.

## Traps
- "An unused port group is harmless" → nobody watches it, and it is still a path into the network.
- "Jumbo frames set on the switch, so the path uses them" → every hop must match, including switches outside your control.
- "Limit the noisy VM's network" → shares handle contention without wasting idle bandwidth.
- "The DVS security policy defaults are fine everywhere" → check each port group is still on Reject; an override opens it.

## Metadata
```yaml
id: vsphere/technology/network/configuration/network-configuration-review
retriever_guide: what-to-set
scope: vsphere
technology:
- network
pillar:
- availability
- performance
- compliance
product:
- vsphere
- nsx
object:
- VmwareDistributedVirtualSwitch
- DistributedVirtualPortgroup
- HostSystem
internal_derive:
- operations-management/sp5-framework/configuration-management
related:
- vsphere/object-types/esxi/configuration/esxi-configuration-review
- operations-management/performance/noisy-neighbour
- vsphere/object-types/esxi/configuration/bios-settings
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Configuration Management > Review List > Network (Distributed Switch & Port Group, Others) (pp. 147-148)'
corrections: []
review_notes:
- 'Section ''Distributed switch'': the book names Cisco Discovery Protocol; LLDP added by Claude.'
- 'Section ''Other components'': the book says ensure the redundancy for both NSX Controller and Manager; NSX-T merged the controller into the Manager cluster. Written as NSX Manager. Q113.'
status: draft
```
