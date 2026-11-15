# Network configuration review

## Scope
- Every network component of VCF: distributed switches and port groups, NSX, physical switches and general settings. One list, for the discussion with the network team.
- Host-side links (NIC redundancy, negotiated speed, VMkernel separation, addressing): [`vsphere/object-types/esxi/configuration/esxi-configuration-review`](../../../object-types/esxi/configuration/esxi-configuration-review.md).

## Distributed switch and port groups
- Version: outdated switch versions.
- Network I/O Control configured.
- Unused port groups: a security risk. They tend not to be monitored, yet anyone can use the path.
- Traffic shaping used where it fits.
- Shares per traffic type set correctly: [`sp5-framework/performance/noisy-neighbour`](../../../../sp5-framework/performance/noisy-neighbour.md).
- Limits: can shares replace them? Shares are more flexible for contention.
- MTU mismatch hurts performance.
- Jumbo frames: on the right networks, end to end. For segments outside your control, detect changes with a discovery protocol (CDP or LLDP).
- Security policy: Forged Transmits, Promiscuous Mode and MAC Address Changes set to Reject.

## MTU test with vmkping
- Test the path MTU of a VMkernel port from the host with `vmkping -I <vmk> -d -s <size> <target IP>` (Broadcom KB 344313).
- The vmkping `-d` flag sets the IPv4 don't-fragment bit, so a packet larger than the MTU of any hop is discarded at that hop instead of being fragmented (Broadcom KB 344313, KB 419088).
- The vmkping `-s` size is the ICMP payload: the MTU minus 28 bytes, the 20-byte IPv4 header and the 8-byte ICMP header. 1472 fills a 1,500-byte MTU; 8972 fills a 9,000-byte MTU (Broadcom KB 344313, KB 451658, KB 313061).
- A vmkping with `-d -s 1473` fails on any path that still has a 1,500-byte hop, often a physical switch port left at its default (Broadcom KB 313061).
- The vmkping error `sendto() failed (Message too long)` is local: the packet is larger than the MTU of the host's own virtual switch or VMkernel port, so it never left the host (Broadcom KB 419088).
- A vmkping with no reply and no error means the packet left the host and was lost on the way: a hop between the host and the target has a smaller MTU, or the target does not answer ping (Broadcom KB 419088).
- Raise the MTU on the physical path first (switch ports, routers, the storage or target ports), then on the virtual switch, then on the VMkernel ports (Broadcom KB 419088).
- On IP storage, an MTU mismatch passes small frames and drops large ones. Symptoms: LUNs visible as storage devices while their datastores are missing or cannot be used, a slow host boot that hangs at Activating: system storage, and a standard-size vmkping that passes while a full-size one fails (Broadcom KB 448714).
- iSCSI discovery and login exchange small frames, so sessions can log in and paths can show Active while the large data frames are dropped.

## Other components
- Top-of-rack switch: firmware compatible with the ESXi NICs it connects; speed not negotiated down.
- Firewall: ports open for services such as syslog, NTP and vSphere HA.
- NSX: version compatible with the other components; NSX Manager redundancy as planned; Edge configuration per practice.
- Encryption: vMotion and similar networks encrypted; hardware offload such as AES-NI used.

## Misconceptions
- "An unused port group is harmless" → nobody watches it, and it is still a path into the network.
- "Jumbo frames set on the switch, so the path uses them" → every hop must match, including switches outside your control.
- "Limit the noisy VM's network" → shares handle contention without wasting idle bandwidth.
- "The DVS security policy defaults are fine everywhere" → check each port group is still on Reject; an override opens it.
- "The iSCSI sessions log in and the paths are Active, so the MTU is fine" → login and discovery use small frames; an MTU mismatch drops only the large ones. Test with vmkping `-d` at the full payload size.
- "vmkping -s 9000 tests a 9,000-byte MTU" → `-s` is the ICMP payload; use 8972, as 28 bytes of IPv4 and ICMP headers fill the rest.
- "vmkping timed out, so vmk1 cannot send jumbo frames" → a local MTU limit fails at once with Message too long; a time-out means the packet left the host and a hop on the path dropped it.

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
- security
product:
- vsphere
- nsx
object:
- VmwareDistributedVirtualSwitch
- DistributedVirtualPortgroup
- HostSystem
internal_derive:
- sp5-framework/concepts/configuration-management
related:
- vsphere/object-types/esxi/configuration/esxi-configuration-review
- sp5-framework/performance/noisy-neighbour
- vsphere/object-types/esxi/configuration/bios-settings
- vsphere/technology/network/concepts/nic-teaming
source:
  document: Knowledge base; Broadcom KB 344313 (Testing VMkernel network connectivity with the vmkping command); Broadcom KB 313061 (Testing jumbo frame pings from ESXi over the network); Broadcom KB 419088 (Risks and potential impacts of changing the MTU on a virtual switch); Broadcom KB 451658 (End-to-End MTU Validation for VMware HCX and vSphere Networks); Broadcom KB 448714 (iSCSI storage connectivity issues or slow boot due to MTU mismatch on ESXi)
  path: 'Configuration Management > Review List > Network (Distributed Switch & Port Group, Others); MTU test with vmkping: the Broadcom KB articles'
corrections:
- 'Section ''MTU test with vmkping'': Broadcom KB 313061 calls the 28 bytes "layer 1 and layer 2 overhead". They are the 20-byte IPv4 header and the 8-byte ICMP header, which the MTU includes (Broadcom KB 451658: IP and ICMP headers).'
review_notes:
- 'Section ''MTU test with vmkping'': the Broadcom KB articles list ESXi 7.x, 8.x and 9.0, none 9.1; check against the vSphere 9.1 networking documentation. https://knowledge.broadcom.com/external/article/344313, https://knowledge.broadcom.com/external/article/313061, https://knowledge.broadcom.com/external/article/419088, https://knowledge.broadcom.com/external/article/451658, https://knowledge.broadcom.com/external/article/448714'
status: draft
```
