# VM CPU Contention or Latency is high

## Checks, in order
1. Contention low: stop. Ready, Co-stop, power management and CPU overcommit are all accounted for in it.
2. Contention high (above 37.5%): check Guest OS Run Queue, Guest OS Context Switch, Guest OS CPU Usage, VM Ready and VM Co-stop.
3. All of step 2 low: the cause is frequency scaling and Hyper-Threading.
4. Step 2 not low: check the VM CPU limit and CPU shares.
5. Check ESXi power management. Set to maximum: frequency scaling is ruled out; Hyper-Threading remains. Otherwise both can be at play.
6. Check CPU overcommit at the time of the issue. More vCPUs than physical cores on the host: Hyper-Threading can be the cause. Otherwise it is not.

## How to read the result
- Frequency-sensitive application: set power management to maximum.
- Hyper-Threading cuts per-thread CPU time by 37.5%. Applications rarely notice: it is transparent, and a CPU 37.5% faster makes up for it.
- Latency near 0% with high Ready: a limit (Latency excludes Max Limited).
- Contention rises when Demand rises and Usage falls: the VM demanded more CPU than it got.

## Traps
- "Contention above 37.5% means CPU starvation" → it can be Hyper-Threading and frequency alone. Check Ready and Co-stop.
- "Use Latency as the SLA" → too volatile. Use Ready.

## Metadata
```yaml
id: vsphere/cpu/diagnosis/vm-cpu-contention-high
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- vsphere/cpu/metrics/virtual-machine/contention
- vsphere/cpu/metrics/virtual-machine/latency
- vsphere/cpu/metrics/comparisons/vm-contention-metrics
related:
- vsphere/cpu/metrics/virtual-machine/ready
- vsphere/cpu/metrics/virtual-machine/co-stop
- vsphere/cpu/concepts/power-states
- vsphere/cpu/concepts/cpu-efficiency
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Contention Metrics > Latency
corrections: []
review_notes:
- 'Section ''Checks'': the 37.5% value is from the book.'
status: draft
```
