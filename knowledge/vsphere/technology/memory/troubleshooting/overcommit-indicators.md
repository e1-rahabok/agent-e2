# Overcommit indicators

## Principle
- The point where overcommitment starts to affect a workload depends on the workload.
- Some workloads show impact earlier than others.
- Check the indicators in the order below.

## Step a: ballooning
- Menu path: Monitor, Performance, Advanced. In the drop-down at the upper right, select Memory. Read Ballooned memory (Average).
- No ballooning: ESX is not under heavy memory pressure. Overcommitment is not affecting this VM.
- The indicator is valid only if the balloon driver is installed in the VM and is not prevented from working.
- Some ballooning is normal. It is not a sign of a problem by itself.

## Step b: consumed vs active
- Menu path: Monitor, Performance, Advanced. Select Memory. Compare Consumed memory with Active memory.
- Consumed above Active: the guest is currently getting all the memory it requires for best performance.

## Step c: host-level swapping and compression
- Menu path: Monitor, Utilization. Expand the Guest Memory pane. Read Swapped and Compressed.
- Non-zero Swapped or Compressed: host-level swapping or compression is active. This is a sign of more significant memory pressure.

## Step d: guest OS swap
- Check for swap activity inside the guest OS.
- Possible meanings:
  - ballooning might be starting to affect performance,
  - the guest OS has another issue unrelated to the host,
  - the guest memory size is too small.

## Traps
- "Ballooned memory above zero means the VM is short of memory now" → some ballooning is normal, and ballooning can reflect earlier reclamation. See `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`.
- "No ballooning means no memory problem" → the indicator is valid only when the balloon driver works. Check Swapped and Compressed too.
- "Guest swap activity proves host overcommitment" → guest swap can have other causes. Check the host indicators first.

## Metadata
```yaml
id: vsphere/technology/memory/troubleshooting/overcommit-indicators
retriever_guide: troubleshooting
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- vsphere/technology/memory/concepts/host-memory-states
- vsphere/technology/memory/configuration/host-level-swapping
- vsphere/technology/memory/metrics/virtual-motherboard/usage
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Memory Considerations > Memory Overcommit Techniques > steps a-d (p. 34)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Page 34 unchanged. Menu paths unchanged in 9.1.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Menu paths are unchanged in the 9.1 document (p. 34).
status: draft
```
