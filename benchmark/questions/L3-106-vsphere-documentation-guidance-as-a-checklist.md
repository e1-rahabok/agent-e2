# vSphere documentation guidance as a checklist

## Prompt
- A new team lead turns the performance chart guidance of the vSphere 9.1 documentation into the team's weekly checklist and applies it to last week's findings:
  - Datastore DS-AF03, on an all-flash array whose own latency is normally 0.3-0.6 ms: esxtop on the hosts that use it shows DAVG/cmd 8-10 ms and KAVG/cmd 0.1 ms from 07:00 to 10:00 on Monday. The lead marks it healthy: under the documentation's 15 ms.
  - Host esx-22: at the busy hour most of its VMs show CPU Ready of 6-9% per vCPU. The lead proposes setting the CPU shares of every VM in the cluster to High.
  - VM web-07 (2 vCPUs): about 2,000 receive packets dropped per hour at its virtual switch port; inside the guest both vCPUs run at 100% at those times. The lead plans to raise the vNIC receive ring size, as the documentation advises for such drops.
  - VM rpt-11: 16 vCPUs, of which the guest keeps 2 busy. The lead leaves it as is: "idle vCPUs cost nothing".

Which statements are correct?

- A. DS-AF03 is healthy: a device latency of 8-10 ms stays under the 15 ms the documentation gives for it.
- B. On an array that normally answers in under 1 ms, DAVG at 8-10 ms with KAVG at 0.1 ms points to the array, the fabric or the HBA.
- C. With High shares on every VM of the cluster, the VMs on esx-22 wait less, so their CPU Ready falls.
- D. The documentation's thresholds are out of date as a whole, so the checklist should use none of them.
- E. Both of web-07's vCPUs are at 100%, so a larger ring would only delay the drops; check the vCPU that drains the ring first.
- F. rpt-11's 14 idle vCPUs cost the host no CPU at all, since a vCPU with no work is never scheduled.
- G. For DS-AF03 the documentation's remedy comes first: move the busiest virtual disk to a volume with more spindles behind it, then watch DAVG.
- H. The vSphere Client offers a network latency chart for web-07's vNIC, so the team can confirm the drops slow its traffic there.

## Likely wrong answer
A: "8-10 ms is under the documentation's 15 ms, so the datastore is fine." D is the over-correction; C and G are the wrong actions the documentation text invites.

## Expected key points
- Answer: B, E.
- A is wrong: the documentation's 15 ms for device latency dates from spinning-disk arrays; a flash array runs far lower, so DAVG is compared with the array's own baseline. 8-10 ms is more than ten times this array's normal latency.
- B is correct: DAVG is the time below the ESXi kernel. High DAVG with low KAVG points to the array; if the array's own latency stays low, to the fabric or the HBA configuration.
- C is wrong: shares are relative. With every VM at High the proportions stay the same, and shares give one VM more chances to run only at the cost of the others: they add no CPU, so a host short of CPU keeps its total Ready.
- D is wrong: the over-correction. The guidance is a generic starting point; several readings hold, and contention metrics confirm a problem before acting.
- E is correct: the documentation advises a larger ring for drops at the virtual switch port; when the vCPU that drains the ring is starved, a larger ring only delays the drops (Broadcom KB 312565), so the guest CPU, Ready and Co-stop of that vCPU are checked first.
- F is wrong: idle vCPUs still cost host CPU, since the hypervisor maintains them; right-size to the vCPUs the workload runs.
- G is wrong: the spindle remedy belongs to spinning-disk arrays; the first step is to locate the latency (array, fabric or HBA) against the array's own statistics.
- H is wrong: vSphere has no network latency counter; the documentation points to an external tool.

## Notes
- vSphere 9.1 documentation, vSphere Monitoring and Performance, Chart Analysis and Troubleshoot and Enhance Performance (pp. 2033-2123). Broadcom KB 312565, https://knowledge.broadcom.com/external/article/312565.

## Metadata
```yaml
id: "0469"
title: "vSphere documentation guidance as a checklist"
product: [vsphere]
technology: [storage, cpu, network]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [datastore, esxi, vm]
tool: [esxtop, vcenter]
knowledge:
  - vsphere/tools/vsphere-client/performance-guidance
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/tools/vsphere-client/performance-guidance
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/tools/vsphere-client/performance-guidance"
answer: [B, E]
misconception: [A]
misconception_type: [threshold-transplanted]
status: draft
```
