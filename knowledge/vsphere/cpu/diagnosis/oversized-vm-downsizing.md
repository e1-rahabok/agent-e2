# Large VM with low utilization: build the case to downsize

## Checks, in order
1. Utilization over a long window (example: 90 days): Usage (%), Demand, Idle (%).
2. Guest OS: CPU Run Queue and Context Switch.
3. Contention: Co-stop, Ready, Other Wait, Swap Wait.
4. Usage Disparity: Peak among vCPUs, Max - Min.
5. Compare Usage with Run: Usage above 90% with Run below 90% is likely Turbo, not demand.

## How to read the result
- Example: 104-vCPU VM, Usage (%) never above 40% in 90 days, Demand marginally higher, Idle about 20%.
- Guest Run Queue low. Reducing vCPUs raises it, which is worse for performance.
- Context Switch high at times.
- Co-stop max 0.006%, Ready max 0.14%. Downsizing may not lower them, and they are irrelevant here.
- Refund and performance arguments do not work. The remaining argument: how the vCPUs are used (Usage Disparity).
- All vCPUs balanced and low: the application cannot use even one vCPU. Questions the vendor's sizing and license cost.
- Imbalanced: some vCPUs saturated. Shows real demand on few vCPUs.

## Traps
- "Low utilization alone convinces the owner" → owners who paid do not care. Show vCPU usage disparity.
- "Usage above 90%, so upsize" → Turbo inflates Usage. Check Run.

## Metadata
```yaml
id: vsphere/cpu/diagnosis/oversized-vm-downsizing
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
pillar:
- capacity
- value
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- vsphere/cpu/metrics/virtual-machine/usage-disparity
- vsphere/cpu/metrics/virtual-machine/usage
related:
- vsphere/cpu/metrics/virtual-machine/run
- vsphere/cpu/concepts/idle-and-unused-vcpus
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Consumption Metrics > CPU Usage Disparity; Usage vs Net Run > Overall
corrections: []
review_notes: []
status: draft
```
