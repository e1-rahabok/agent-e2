# ESXi CPU Wait

## Meaning
- Sum of the Wait of the VMs on the host. vSphere Web Services API 9.1 defines `cpu.wait` as total CPU time spent in wait state, for VirtualMachine and HostSystem alike.
- Example: a host with 2 VMs shows Wait equal to the sum of the 2 VM Wait values.
- A physical thread runs or is halted; it does not wait. The host value is therefore a sum of consumer values, not a provider state ([`vsphere/architecture/provider-consumer`](../../../../architecture/provider-consumer.md)).
- Each VM's Wait is Idle + Swap Wait + Other Wait, and Idle is most of it on a VM that does not run at 100%. The host sum is therefore mostly idle time ([`vsphere/technology/cpu/metrics/virtual-motherboard/wait`](../virtual-motherboard/wait.md), section Sub-metrics).
- Relevance for operations: none. It mixes idle time into one host total; read VM CPU Swap Wait and VM CPU Other Wait per VM for waits that matter.

## Misconceptions
- "High host Wait means the host waits for IO" → it is the sum of VM Wait, mostly idle. Read VM CPU Other Wait and VM CPU Swap Wait per VM.
- "Host Wait rose, so the host got slower" → host Wait grows with the number of powered-on VMs and their idle vCPUs, with no change in contention. Check VM CPU Ready and Co-stop.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/wait
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- HostSystem
metric_class: context
internal_derive:
- vsphere/technology/cpu/concepts/vcpu-states
- vsphere/architecture/provider-consumer
same_name:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
- vsphere/technology/cpu/metrics/host/idle
source:
  document: Knowledge base; vSphere Web Services API 9.1 reference, CPU Counters
  path: CPU > ESXi > Wait Metric; https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/cpu_counters.html, wait
corrections: []
review_notes: []
status: draft
```
