# VM CPU Run and Used differ

## Checks, in order
1. Check contention metrics first: Ready, Co-stop, Overlap.
2. Check System (ms) and Overlap (ms): they move Used away from Run.
3. Check the host power management policy and actual frequency (esxtop %A/MPERF).
4. Check whether sibling threads are busy (Hyper-Threading).

## How to read the result
| Pattern | Meaning | Next step |
|---|---|---|
| Used higher than Run | Turbo raises Used. System, VMX, MKS and Helper add to VM-level Used. | Check frequency and System. |
| Used lower than Run, little System and Overlap | Power saving and Hyper-Threading lower Used. | Do not add vCPUs. Check power management and SMT. |
| Example: 4-vCPU Ubuntu VM, Used about 44% of Run | Power saving plus SMT. | If Run is far from 100% and the team asks for speed, adding vCPUs is the wrong answer. |
| Example: 1-vCPU VM, 2.095 GHz host, 2 GHz limit | Demand and Usage flat around 1.96 GHz (about 94%). Used about 18,600 ms (93%). Run much lower: Used 41% higher than Run. | Cause: CPU frequency. The VM ran above nominal clock speed because of Turbo Boost. Used grows with frequency; Run is time only. |

- Under a limit, Demand equals Usage: the kernel does not see the limited time as demand.

## Traps
- "Run is low, so the VM has headroom" → check Ready. Under a limit, Run stays low.
- "Add vCPUs to speed up" → when Used is far below Run, the cause is frequency or SMT.

## Metadata
```yaml
id: vsphere/technology/cpu/troubleshooting/run-vs-used-gap
retriever_guide: troubleshooting
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/run
- vsphere/technology/cpu/metrics/virtual-motherboard/used
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/cpu/metrics/virtual-motherboard/demand
- vsphere/technology/cpu/concepts/power-states
- vsphere/technology/cpu/concepts/hyper-threading
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > When Run is lower than Used; When Run is higher than Used
corrections: []
review_notes: []
status: draft
```
